from uuid import UUID

from django.test import TestCase

from jsonschema.validators import Draft202012Validator

from openforms.authentication.constants import AuthAttribute
from openforms.authentication.static_variables.static_variables import (
    Auth,
    AuthBSN,
    AuthContext,
    AuthContextActingSubjectIdentifier,
    AuthContextActingSubjectIdentifierType,
    AuthContextBranchNumber,
    AuthContextLegalSubjectIdentifier,
    AuthContextLegalSubjectIdentifierType,
    AuthContextLOA,
    AuthContextRepresenteeIdentifier,
    AuthContextRepresenteeType,
    AuthContextSource,
    AuthKvK,
    AuthPseudo,
    AuthType,
    LanguageCode,
    SubmissionID,
)
from openforms.authentication.tests.factories import AuthInfoFactory
from openforms.submissions.tests.factories import SubmissionFactory
from openforms.variables.service import get_static_variables


class TestStaticVariables(TestCase):
    def test_auth_static_data(self):
        auth_info = AuthInfoFactory.create(
            plugin="test-plugin",
            attribute=AuthAttribute.bsn,
            value="111222333",
        )

        static_data = {
            variable.key: variable
            for variable in get_static_variables(submission=auth_info.submission)
        }

        expected = {
            "auth": {
                "plugin": "test-plugin",
                "attribute": AuthAttribute.bsn,
                "value": "111222333",
            },
            "auth_bsn": "111222333",
            "auth_kvk": "",
            "auth_pseudo": "",
            "auth_type": "bsn",
        }

        for variable_key, value in expected.items():
            with self.subTest(key=variable_key, value=value):
                self.assertIn(variable_key, static_data)
                self.assertEqual(static_data[variable_key].initial_value, value)

    def test_auth_static_data_no_submission(self):
        static_data = {variable.key: variable for variable in get_static_variables()}

        expected = {
            "auth": None,
            "auth_bsn": "",
            "auth_kvk": "",
            "auth_pseudo": "",
            "auth_type": "",
        }

        for variable_key, value in expected.items():
            with self.subTest(key=variable_key, value=value):
                self.assertIn(variable_key, static_data)
                self.assertEqual(static_data[variable_key].initial_value, value)

    def test_submission_id_variable(self):
        submission = SubmissionFactory.build(
            uuid=UUID("b0a84235-3afe-49ca-8f75-fc2015538b1a")
        )
        static_data = {
            variable.key: variable.initial_value
            for variable in get_static_variables(submission=submission)
        }

        self.assertEqual(
            static_data["submission_id"], "b0a84235-3afe-49ca-8f75-fc2015538b1a"
        )

    def test_language_code_variable(self):
        submission = SubmissionFactory.build(language_code="nl")
        static_data = {
            variable.key: variable.initial_value
            for variable in get_static_variables(submission=submission)
        }

        self.assertEqual(static_data["language_code"], "nl")

    def test_branch_number_variable(self):
        cases = (
            (
                AuthInfoFactory.create(
                    is_digid=True,
                    legal_subject_service_restriction="foo",
                ),
                "",
            ),
            (
                AuthInfoFactory.create(
                    is_digid_machtigen=True,
                    legal_subject_service_restriction="foo",
                ),
                "",
            ),
            (
                AuthInfoFactory.create(
                    is_eh=True,
                    legal_subject_service_restriction="123456789012",
                ),
                "123456789012",
            ),
            (
                AuthInfoFactory.create(
                    is_eh_bewindvoering=True,
                    legal_subject_service_restriction="123456789012",
                ),
                "123456789012",
            ),
            (
                AuthInfoFactory.create(
                    is_eh=True,
                    legal_subject_service_restriction="",
                ),
                "",
            ),
            (
                AuthInfoFactory.create(
                    is_eh_bewindvoering=True,
                    legal_subject_service_restriction="",
                ),
                "",
            ),
        )
        for auth_info, expected in cases:
            with self.subTest(
                attribute=auth_info.attribute,
                service_restriction=auth_info.legal_subject_service_restriction,
            ):
                static_data = {
                    variable.key: variable.initial_value
                    for variable in get_static_variables(
                        submission=auth_info.submission
                    )
                }

                self.assertEqual(static_data["auth_context_branch_number"], expected)


class StaticVariableValidJsonSchemaTests(TestCase):

    validator = Draft202012Validator

    def check_schema(self, properties):
        schema = {
            "$schema": self.validator.META_SCHEMA["$id"],
            **properties,
        }

        self.validator.check_schema(schema)

    def test_submission_id(self):
        schema = SubmissionID.as_json_schema()
        self.check_schema(schema)

    def test_language_code(self):
        schema = LanguageCode.as_json_schema()
        self.check_schema(schema)

    def test_auth(self):
        schema = Auth.as_json_schema()
        self.check_schema(schema)

    def test_auth_type(self):
        schema = AuthType.as_json_schema()
        self.check_schema(schema)

    def test_auth_bsn(self):
        schema = AuthBSN.as_json_schema()
        self.check_schema(schema)

    def test_auth_kvk(self):
        schema = AuthKvK.as_json_schema()
        self.check_schema(schema)

    def test_auth_pseudo(self):
        schema = AuthPseudo.as_json_schema()
        self.check_schema(schema)

    def test_auth_context(self):
        schema = AuthContext.as_json_schema()
        self.check_schema(schema)

    def test_auth_context_source(self):
        schema = AuthContextSource.as_json_schema()
        self.check_schema(schema)

    def test_auth_context_loa(self):
        schema = AuthContextLOA.as_json_schema()
        self.check_schema(schema)

    def test_auth_context_representee_type(self):
        schema = AuthContextRepresenteeType.as_json_schema()
        self.check_schema(schema)

    def test_auth_context_representee_identifier(self):
        schema = AuthContextRepresenteeIdentifier.as_json_schema()
        self.check_schema(schema)

    def test_auth_context_legal_subject_identifier_type(self):
        schema = AuthContextLegalSubjectIdentifierType.as_json_schema()
        self.check_schema(schema)

    def test_auth_context_legal_subject_identifier(self):
        schema = AuthContextLegalSubjectIdentifier.as_json_schema()
        self.check_schema(schema)

    def test_auth_context_branch_number(self):
        schema = AuthContextBranchNumber.as_json_schema()
        self.check_schema(schema)

    def test_auth_context_acting_subject_identifier_type(self):
        schema = AuthContextActingSubjectIdentifierType.as_json_schema()
        self.check_schema(schema)

    def test_auth_context_acting_subject_identifier(self):
        schema = AuthContextActingSubjectIdentifier.as_json_schema()
        self.check_schema(schema)
