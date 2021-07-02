import dataclasses
from typing import Any, Callable, Mapping, Optional, Union

from djchoices import ChoiceItem
from glom import Assign, glom

from openforms.submissions.models import Submission

NOT_SET = object()
SKIP = object()


@dataclasses.dataclass()
class FieldConf:
    # value from RegistrationAttribute
    attribute: Union[str, ChoiceItem] = None

    # transform value (eg: dates/times etc)
    transform: Optional[Callable[[Any], Any]] = None

    # support attributes from form
    form_field: str = ""

    # support attributes from submission
    submission_field: str = ""

    # default value if data not found in submission
    default: Any = SKIP

    def __post_init__(self):
        assert not (self.attribute and (self.form_field or self.submission_field))
        assert not (self.form_field and self.submission_field)
        assert self.attribute or self.form_field or self.submission_field


def apply_data_mapping(
    submission: Submission,
    mapping_config: Mapping[str, Union[str, FieldConf]],
    component_attribute: str = "registration.attribute",
) -> dict:
    """
    apply mapping to data and build new data structure

    """
    target_dict = dict()

    # build a lookup, also implicitly de-duplicates assigned attributes
    attr_key_lookup = dict()

    for component in submission.form.iter_components(recursive=True):
        key = component.get("key")
        attribute = glom(component, component_attribute, default=None)
        if key and attribute:
            attr_key_lookup[attribute] = key

    # grab submitted data
    data = submission.get_merged_data()

    for target_path, conf in mapping_config.items():
        if isinstance(conf, str):
            # upgrade for code simplicity
            conf = FieldConf(conf)

        # grab value
        value = NOT_SET
        if conf.form_field:
            value = getattr(submission.form, conf.form_field, NOT_SET)
        elif conf.submission_field:
            value = getattr(submission, conf.submission_field, NOT_SET)
        elif data_key := attr_key_lookup.get(conf.attribute):
            value = data.get(data_key, NOT_SET)

        if value is NOT_SET:
            value = conf.default
        if value is SKIP:
            continue

        if conf.transform:
            value = conf.transform(value)
            if value is SKIP:
                continue

        glom(target_dict, Assign(target_path, value, missing=dict))

    return target_dict
