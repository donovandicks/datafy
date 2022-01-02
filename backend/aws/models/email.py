"""Code for modeling SES data"""

from typing import Literal, Optional, Union

from pydantic import BaseModel


class Body(BaseModel):
    """The body of an email"""

    content_type: Optional[Union[Literal["Text"], Literal["HTML"]]] = "Text"
    """The type of body object - either raw `Text` or valid `HTML`"""

    data: str
    """The content of the body"""

    charset: Optional[str]
    """The character set for the content of the body"""

    @classmethod
    def from_dict(cls, obj: dict):
        """
        Creates a `Body` object from a dictionary
        """
        return Body(
            content_type=obj.get("content_type", "Text"),
            data=obj.get("data", ""),
            charset=obj.get("charset", ""),
        )

    def to_dict(self) -> dict:
        """Converts a `Body` object to a dictionary"""
        return {
            self.content_type: {
                "Data": self.data,
                "Charset": self.charset,
            }
        }


class Subject(BaseModel):
    """ """

    data: str

    charset: Optional[str]

    @classmethod
    def from_dict(cls, obj: dict):
        """"""
        return Subject(
            data=obj.get("data", ""),
            charset=obj.get("charset", ""),
        )

    def to_dict(self) -> dict:
        """"""
        return {
            "Data": self.data,
            "Charset": self.charset,
        }


class Message(BaseModel):
    """ """

    subject: Subject

    body: Body

    def to_dict(self) -> dict:
        return {
            "Subject": self.subject.to_dict(),
            "Body": self.body.to_dict(),
        }


class Destination(BaseModel):
    """"""

    to_addresses: list[str]
    cc_addresses: Optional[list[str]]
    bcc_addresses: Optional[list[str]]

    def to_dict(self) -> dict:
        return {
            "ToAddresses": self.to_addresses,
            "CcAddresses": self.cc_addresses,
            "BccAddresses": self.bcc_addresses,
        }


class Email(BaseModel):
    """
    Stripped down SES Email data model
    """

    source: str
    """The email from which the email is sent"""

    destination: Destination
    """The recipients to send the email to"""

    message: Message

    @classmethod
    def from_dict(cls, obj: dict):
        """
        Converts a dictionary into an Email object.

        The model expected is as follows:

        ```
        {
            source: str,
            to_addresses: list[str],
            cc_addresses: Optional[list[str]],
            bcc_addresses: Optional[list[str]],
            subject: {
                data: str,
                charset: str,
            }
            body: {
                content_type: Text | HTML,
                data: str,
                charset: str,
            }
        }
        ```

        See type definition for `Body` for expected inputs for the body
        object
        """

        return Email(
            source=obj.get("source", ""),
            destination=Destination(
                to_addresses=obj.get("to_addresses", []),
                cc_addresses=obj.get("cc_addresses", []),
                bcc_addresses=obj.get("bcc_addresses", []),
            ),
            message=Message(
                subject=Subject.from_dict(obj.get("subject", {})),
                body=Body.from_dict(obj.get("body", {})),
            ),
        )

    def to_dict(self) -> dict:
        """"""
        return {
            "Source": self.source,
            "Destination": self.destination.to_dict(),
            "Message": self.message.to_dict(),
        }
