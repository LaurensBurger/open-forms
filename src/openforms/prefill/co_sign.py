"""
Integrate pre-fill functionality with co-sign authentication flow.

When a user authenticates to co-sign a submission, we need to retrieve information
based on their identifier to get a representation of the co-signer for the UI. This is
done by amending the co-sign data on a submission when the co-sign auth event is
received, see the :mod:`signals` module.
"""
import logging
from typing import Optional

from openforms.authentication.constants import AuthAttribute
from openforms.submissions.models import Submission

from .models import PrefillConfig
from .registry import register

logger = logging.getLogger(__name__)


AUTH_ATTRIBUTE_TO_CONFIG_FIELD = {
    AuthAttribute.bsn: "default_person_plugin",
    AuthAttribute.kvk: "default_company_plugin",
}


def get_default_plugin_for_auth_attribute(auth_attribute: str) -> Optional[str]:
    if not (config_field := AUTH_ATTRIBUTE_TO_CONFIG_FIELD.get(auth_attribute)):
        logger.info("Unsupported auth_attribute '%s'", auth_attribute)
        return

    config = PrefillConfig.get_solo()
    default_plugin = getattr(config, config_field)
    if not default_plugin:
        logger.info(
            "Prefill config is missing a value for '%s', aborting.", config_field
        )
    return default_plugin


def add_co_sign_representation(submission: Submission, auth_attribute: str):
    default_plugin = get_default_plugin_for_auth_attribute(auth_attribute)
    # configuration may be incomplete, do nothing in that case!
    if not default_plugin:
        return

    plugin = register[default_plugin]
    logger.debug(
        "Fetching co-sign representation data for submission %s using plugin %r",
        submission.uuid,
        plugin,
    )

    values, representation = plugin.get_co_sign_values(
        submission.co_sign_data["identifier"]
    )
    submission.co_sign_data["fields"] = values
    submission.co_sign_data["representation"] = representation
    submission.save(update_fields=["co_sign_data"])
