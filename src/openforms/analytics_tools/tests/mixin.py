from cookie_consent.models import CookieGroup

from openforms.analytics_tools.models import AnalyticsToolsConfiguration


class AnalyticsMixin:
    def setUp(self):
        super().setUp()
        self.config = AnalyticsToolsConfiguration.get_solo()
        self.config.analytics_cookie_consent_group = CookieGroup.objects.get(
            varname="analytical"
        )

        self.addCleanup(lambda: AnalyticsToolsConfiguration.get_solo().delete())
