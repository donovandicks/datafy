"""Unit Tests for the SES data models"""

from unittest import TestCase

from pydantic.error_wrappers import ValidationError
from pytest import fail, raises

from ..models.email import Body, Email, Message, Subject


class SESTests(TestCase):
    """Test Cases for SES Data Models"""

    def test_invalid_body_content_type(self):
        """Tests that an error is raised if passes an invalid content type"""
        with raises(ValidationError):
            Body(content_type="ABC", data="")

    def test_valid_body_content_type(self):
        """Tests that a Body object is created with valid content type"""
        try:
            Body(content_type="Text", data="")
        except ValidationError as ex:
            fail(msg=f"Test Failed with Exception: {ex}")

    def test_valid_body_data(self):
        """Tests that a Body object is created with valid data"""
        try:
            Body(content_type="Text", data="Hello, world!")
        except ValidationError as ex:
            fail(msg=f"Test Failed with Exception: {ex}")

    def test_invalid_body_data(self):
        """Tests that a Body object is created with valid data"""
        with raises(ValidationError):
            Body(content_type="Text", data=["Hello", "world!"])

    def test_body_from_valid_dict_with_all_params(self):
        self.assertEqual(
            Body(content_type="HTML", data="Hello, world!", charset="unicode"),
            Body.from_dict(
                {
                    "content_type": "HTML",
                    "data": "Hello, world!",
                    "charset": "unicode",
                }
            ),
        )

    def test_body_from_valid_dict_with_req_params(self):
        self.assertEqual(
            Body(content_type="Text", data="Hello, world!", charset=""),
            Body.from_dict(
                {
                    "data": "Hello, world!",
                }
            ),
        )

    def test_body_from_invalid_dict(self):
        with raises(ValidationError):
            Body.from_dict({"content_type": "ABC", "data": ""})

    def test_body_to_dict(self):
        self.assertEqual(
            {
                "Text": {
                    "Data": "Hello, world!",
                    "Charset": None,
                },
            },
            Body(content_type="Text", data="Hello, world!").to_dict(),
        )

    def test_subject_from_valid_dict(self):
        self.assertEqual(
            Subject(data="Hello, world!", charset=""),
            Subject.from_dict({"data": "Hello, world!"}),
        )

    def test_subject_from_invalid_dict(self):
        with raises(ValidationError):
            Subject(data={"text": "Hello, world!"}, charset="")

    def test_subject_to_dict(self):
        self.assertEqual(
            {"Data": "Hello, world!", "Charset": None},
            Subject(data="Hello, world!").to_dict(),
        )

    def test_email_to_dict(self):
        self.assertDictEqual(
            {
                "Source": "test@email.com",
                "Destination": {
                    "ToAddresses": ["recipient1@email.com"],
                    "CcAddresses": ["recipient2@email.com"],
                    "BccAddresses": None,
                },
                "Message": {
                    "Subject": {
                        "Data": "Hello",
                        "Charset": None,
                    },
                    "Body": {
                        "Text": {
                            "Data": "world!",
                            "Charset": None,
                        },
                    },
                },
            },
            Email(
                source="test@email.com",
                destination={
                    "to_addresses": ["recipient1@email.com"],
                    "cc_addresses": ["recipient2@email.com"],
                },
                message=Message(
                    subject=Subject(data="Hello"),
                    body=Body(data="world!"),
                ),
            ).to_dict(),
        )

    def test_email_from_valid_dict(self):
        self.assertEqual(
            Email.from_dict(
                {
                    "source": "test@email.com",
                    "to_addresses": ["recipient1@email.com"],
                    "cc_addresses": ["recipient2@email.com"],
                    "bcc_addresses": None,
                    "subject": {
                        "data": "Hello",
                    },
                    "body": {
                        "data": "world!",
                    },
                }
            ),
            Email(
                source="test@email.com",
                destination={
                    "to_addresses": ["recipient1@email.com"],
                    "cc_addresses": ["recipient2@email.com"],
                },
                message=Message(
                    subject=Subject(data="Hello", charset=""),
                    body=Body(data="world!", charset=""),
                ),
            ),
        )
