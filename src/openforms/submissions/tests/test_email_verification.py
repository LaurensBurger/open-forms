"""
Test the email verification flow.
"""

from django.core import mail

from rest_framework import status
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.test import APITestCase

from openforms.forms.tests.factories import FormFactory
from openforms.submissions.models import EmailVerification

from .factories import SubmissionFactory
from .mixins import SubmissionsMixin


class VerificationCreationTests(SubmissionsMixin, APITestCase):
    """
    Test the flow when an email verification is initiated.
    """

    endpoint = reverse_lazy("api:submissions:email-verification")

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.form = FormFactory.create(
            generate_minimal_setup=True,
            formstep__form_definition__configuration={
                "components": [
                    {
                        "type": "email",
                        "key": "emailAddress",
                        "label": "Email address",
                        "openForms": {
                            "requireVerification": True,
                        },
                    }
                ]
            },
        )

    def test_requires_submission_in_session(self):
        submission = SubmissionFactory.create(form=self.form)
        submission_endpoint = reverse(
            "api:submission-detail", kwargs={"uuid": submission.uuid}
        )
        body = {
            "submission": f"http://testserver{submission_endpoint}",
            "componentKey": "emailAddress",
            "email": "openforms@example.com",
        }

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(self.endpoint, body)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(mail.outbox), 0)

    def test_requires_ownership_of_submission(self):
        submission = SubmissionFactory.create(form=self.form)
        other_submission = SubmissionFactory.create(form=self.form)
        self._add_submission_to_session(other_submission)
        submission_endpoint = reverse(
            "api:submission-detail", kwargs={"uuid": submission.uuid}
        )
        body = {
            "submission": f"http://testserver{submission_endpoint}",
            "componentKey": "emailAddress",
            "email": "openforms@example.com",
        }

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(self.endpoint, body)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 0)
        error = response.json()["invalidParams"][0]
        self.assertEqual(error["name"], "submission")
        self.assertEqual(error["code"], "does_not_exist")

    def test_validates_component_key(self):
        submission = SubmissionFactory.create(form=self.form)
        self._add_submission_to_session(submission)
        submission_endpoint = reverse(
            "api:submission-detail", kwargs={"uuid": submission.uuid}
        )
        body = {
            "submission": f"http://testserver{submission_endpoint}",
            "componentKey": "invalidComponentKey",
            "email": "openforms@example.com",
        }

        response = self.client.post(self.endpoint, body)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = response.json()["invalidParams"][0]
        self.assertEqual(error["name"], "componentKey")
        self.assertEqual(error["code"], "not_found")

    def test_valid_verification_creation(self):
        submission = SubmissionFactory.create(form=self.form)
        self._add_submission_to_session(submission)
        submission_endpoint = reverse(
            "api:submission-detail", kwargs={"uuid": submission.uuid}
        )
        body = {
            "submission": f"http://testserver{submission_endpoint}",
            "componentKey": "emailAddress",
            "email": "openforms@example.com",
        }

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(self.endpoint, body)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        email_verification = EmailVerification.objects.get()
        self.assertEqual(email_verification.submission, submission)
        self.assertEqual(email_verification.component_key, "emailAddress")
        self.assertEqual(email_verification.email, "openforms@example.com")
        self.assertNotEqual(email_verification.verification_code, "")
        self.assertIsNone(email_verification.verified_on)

        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.to, ["openforms@example.com"])
        self.assertIn(email_verification.verification_code, str(msg.body))

    def test_multiple_verifications_for_the_same_email(self):
        submission = SubmissionFactory.create(form=self.form)
        self._add_submission_to_session(submission)
        submission_endpoint = reverse(
            "api:submission-detail", kwargs={"uuid": submission.uuid}
        )
        body = {
            "submission": f"http://testserver{submission_endpoint}",
            "componentKey": "emailAddress",
            "email": "openforms@example.com",
        }

        with self.captureOnCommitCallbacks(execute=True):
            # initiate the verification twice
            self.client.post(self.endpoint, body)
            self.client.post(self.endpoint, body)

        self.assertEqual(EmailVerification.objects.count(), 2)
        self.assertEqual(len(mail.outbox), 2)
