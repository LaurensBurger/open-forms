import base64
import json

from django.core.exceptions import SuspiciousOperation
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import gettext_lazy as _

from zgw_consumers.client import build_client

from openforms.formio.components.utils import to_multiple
from openforms.formio.dynamic_config import rewrite_formio_components
from openforms.formio.typing import Component
from openforms.forms.utils import form_variables_to_json_schema
from openforms.submissions.logic.datastructures import DataContainer
from openforms.submissions.models import (
    Submission,
    SubmissionFileAttachment,
    SubmissionValueVariable,
)
from openforms.typing import JSONObject, JSONValue
from openforms.variables.constants import FormVariableSources

from ...base import BasePlugin  # openforms.registrations.base
from ...registry import register  # openforms.registrations.registry
from .config import JSONDumpOptions, JSONDumpOptionsSerializer


@register("json_dump")
class JSONDumpRegistration(BasePlugin):
    verbose_name = _("JSON dump registration")
    configuration_options = JSONDumpOptionsSerializer

    # TODO: add JSONDumpResult typed dict to properly indicate return value
    def register_submission(
        self, submission: Submission, options: JSONDumpOptions
    ) -> dict:
        state = submission.load_submission_value_variables_state()

        # Generate values
        all_values: JSONObject = {
            **state.get_static_data(),
            **state.get_data(),  # dynamic values from user input
        }
        values = {
            key: value
            for key, value in all_values.items()
            if key in options["variables"]
        }

        # Generate schema
        schema = form_variables_to_json_schema(submission.form, options["variables"])

        # Post-processing
        self.post_processing(submission, values, schema)

        # Send to the service
        data = json.dumps({"values": values, "schema": schema}, cls=DjangoJSONEncoder)
        service = options["service"]
        with build_client(service) as client:
            if ".." in (path := options["path"]):
                raise SuspiciousOperation("Possible path traversal detected")

            result = client.post(path, json=data)
            result.raise_for_status()

        return {"api_response": result.json()}

    def check_config(self) -> None:
        # Config checks are not really relevant for this plugin right now
        pass

    @staticmethod
    def post_processing(
        submission: Submission, values: JSONObject, schema: JSONObject
    ) -> None:
        """Post-processing of values and schema.

        File components need special treatment, as we send the content of the file
        encoded with base64, instead of the output from the serializer. Also, Radio,
        Select, and SelectBoxes components need to be updated if their data source is
        set to another form variable.

        :param submission: Submission
        :param values: JSONObject
        :param schema: JSONObject
        """
        state = submission.load_submission_value_variables_state()

        for key in values.keys():
            variable = state.variables.get(key)
            if (
                variable is None
                or variable.form_variable.source == FormVariableSources.user_defined
            ):
                # None for static variables, and processing user defined variables is
                # not relevant here
                continue

            component = get_component(variable, submission)
            assert component is not None

            match component["type"]:
                case "file":
                    encoded_attachments = [
                        {
                            "file_name": attachment.original_name,
                            "content": encode_attachment(attachment),
                        }
                        for attachment in submission.attachments
                        if attachment.form_key == key
                    ]

                    base_schema = {
                        "title": component["label"],
                        "type": "object",
                        "properties": {
                            "file_name": {"type": "string"},
                            "content": {"type": "string", "format": "base64"},
                        },
                        "required": (
                            ["file_name", "content"]
                            if len(encoded_attachments) != 0
                            else []
                            # No required properties when there are no attachments
                        ),
                        "additionalProperties": False,
                    }

                    match (
                        component.get("multiple", False),
                        n_attachments := len(encoded_attachments),
                    ):
                        case False, 0:
                            value = None

                            base_schema = {"title": component["label"], "type": "null"}
                        case False, 1:
                            value = encoded_attachments[0]
                        case True, int():
                            value = encoded_attachments

                            base_schema = to_multiple(base_schema)
                        case False, int():  # pragma: no cover
                            raise ValueError(
                                f"Cannot have multiple attachments ({n_attachments}) "
                                "for a single file component."
                            )
                    values[key] = value
                    schema["properties"][key] = base_schema
                case "radio":
                    data_src = component.get("openForms", {}).get("dataSrc")
                    if data_src != "variable":
                        # Only components where another variable is used as a data
                        # source need to be processed, so skip this one
                        continue

                    choices = [options["value"] for options in component["values"]]
                    choices.append("")  # Take into account an unfilled field
                    schema["properties"][key]["enum"] = choices
                case "select":
                    data_src = component.get("openForms", {}).get("dataSrc")
                    if data_src != "variable":
                        # Only components where another variable is used as a data
                        # source need to be processed, so skip this one
                        continue

                    choices = [
                        options["value"] for options in component["data"]["values"]
                    ]
                    choices.append("")  # Take into account an unfilled field

                    if component.get("multiple", False):
                        schema["properties"][key]["items"]["enum"] = choices
                    else:
                        schema["properties"][key]["enum"] = choices
                case "selectboxes":
                    data_src = component.get("openForms", {}).get("dataSrc")

                    # Only components where another variable is used as a data
                    # source need to be processed
                    if data_src == "variable":
                        properties = {
                            options["value"]: {"type": "boolean"}
                            for options in component["values"]
                        }
                        schema["properties"][key].update(
                            {
                                "properties": properties,
                                "required": list(properties.keys()),
                                "additionalProperties": False,
                            }
                        )

                    # If the select boxes component is not filled, set required
                    # properties to empty list
                    if not values[key]:
                        schema["properties"][key]["required"] = list()
                case _:
                    pass


def encode_attachment(attachment: SubmissionFileAttachment) -> str:
    """Encode an attachment using base64

    :param attachment: Attachment to encode
    :returns: Encoded base64 data as a string
    """
    with attachment.content.open("rb") as f:
        f.seek(0)
        return base64.b64encode(f.read()).decode()


def get_component(
    variable: SubmissionValueVariable, submission: Submission
) -> Component | None:
    """Get the component from a submission value variable.

    :param variable: SubmissionValueVariable
    :param submission: Submission
    :return component: None if the form variable has no form definition
    """
    config_wrapper = variable.form_variable.form_definition.configuration_wrapper

    # Update components. This is necessary to update the options for Select,
    # SelectBoxes, and Radio components, which get their options from another form
    # variable.
    state = submission.load_submission_value_variables_state()
    data = DataContainer(state=state)
    config_wrapper = rewrite_formio_components(
        config_wrapper, submission=submission, data=data.data
    )

    component = config_wrapper.component_map[variable.key]

    return component
