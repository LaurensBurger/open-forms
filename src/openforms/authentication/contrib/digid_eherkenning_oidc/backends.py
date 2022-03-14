import logging

from digid_eherkenning_oidc_generics.backends import OIDCAuthenticationBackend
from digid_eherkenning_oidc_generics.mixins import (
    SoloConfigDigiDMixin,
    SoloConfigEHerkenningMixin,
)

from .constants import DIGID_OIDC_AUTH_SESSION_KEY, EHERKENNING_OIDC_AUTH_SESSION_KEY

logger = logging.getLogger(__name__)


class OIDCAuthenticationDigiDBackend(SoloConfigDigiDMixin, OIDCAuthenticationBackend):
    """
    Allows logging in via OIDC with DigiD
    """

    session_key = DIGID_OIDC_AUTH_SESSION_KEY


class OIDCAuthenticationEHerkenningBackend(
    SoloConfigEHerkenningMixin, OIDCAuthenticationBackend
):
    """
    Allows logging in via OIDC with DigiD
    """

    session_key = EHERKENNING_OIDC_AUTH_SESSION_KEY
