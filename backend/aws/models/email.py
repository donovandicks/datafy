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

        Params
        ------
        obj: dict
            a dictionary containing metadata and data for an email body

        Returns
        -------
        body: Body
            a `Body` object with the given data

        Example
        -------
        ```python
        body = Body.from_dict({
            "content_type": "Text",
            "data": "Hello, world!",
            "charset": "UTF-8",
        })
        ```
        """
        return Body(
            content_type=obj.get("content_type", "Text"),
            data=obj.get("data", ""),
            charset=obj.get("charset", ""),
        )

    def to_dict(self) -> dict:
        """
        Converts a `Body` object to a dictionary

        Returns
        -------
        body: dict
            the body data mapped to a dictionary that SES expects

        Example
        -------
        ```python
        body = Body(
            content_type="Text",
            data="Hello, world!",
            charset="UTF-8",
        )

        body_dict = {
            "Text": {
                "Data": "Hello, world!",
                "Charset": "UTF-8",
            }
        }

        body.to_dict() == body_dict # True
        ```
        """
        return {
            self.content_type: {
                "Data": self.data,
                "Charset": self.charset,
            }
        }


class Subject(BaseModel):
    """
    Data model for an email subject
    """

    data: str
    """The textual content of the email subject"""

    charset: Optional[str]
    """The character set used for the subject content"""

    @classmethod
    def from_dict(cls, obj: dict):
        """
        Creates a `Subject` object from a dictionary

        Params
        ------
        obj: dict
            a dictionary containing metadata and data about the email subject

        Returns
        -------
        subject: Subject
            a `Subject` object with the given data

        Example
        -------
        ```python
        subject = Subject.from_dict({
            "data": "Urgent Alert",
            "charset": "UTF-8",
        })
        ```
        """
        return Subject(
            data=obj.get("data", ""),
            charset=obj.get("charset", ""),
        )

    def to_dict(self) -> dict:
        """
        Converts a `Subject` object to a dictionary

        Returns
        -------
        subject: dict
            the subject data mapped to a dictionary that SES expects

        Example
        -------
        ```python
        subject = Subject(
            data="Urgent Alert",
            charset="UTF-8"
        )

        subject_dict = {
            "Data": "Urgent Alert",
            "Charset": "UTF-8",
        }

        subject.to_dict() == subject_dict # True
        ```
        """
        return {
            "Data": self.data,
            "Charset": self.charset,
        }


class Message(BaseModel):
    """
    A wrapper for a `Subject` and `Body`
    """

    subject: Subject
    """The `Subject` object for the email"""

    body: Body
    """The `Body` object for the email"""

    def to_dict(self) -> dict:
        """
        Converts a `Message` to a dictionary

        Returns
        -------
        message: dict
            the message data mapped to a dictionary that SES expects

        Example
        -------
        ```python
        msg = Message(
            subject=Subject(
                data="Urgent Alert",
                charset="UTF-8"
            ),
            body=Body(
                content_type="Text",
                data="Hello, world!",
                charset="UTF-8",
            )
        )

        msg_dict = {
            "Subject": {
                "Data": "Urgent Alert",
                "Charset": "UTF-8",
            },
            "Body": {
                "Text": {
                    "Data": "Hello, world!",
                    "Charset": "UTF-8",
                }
            }
        }

        msg.to_dict() == msg_dict # True
        ```
        """
        return {
            "Subject": self.subject.to_dict(),
            "Body": self.body.to_dict(),
        }


class Destination(BaseModel):
    """
    A collection of emails for recipients
    """

    to_addresses: list[str]
    """Main addressee emails to send to"""

    cc_addresses: Optional[list[str]]
    """Addressees to be CC'd on the email"""

    bcc_addresses: Optional[list[str]]
    """Addressees to be BCC'd on the email"""

    def to_dict(self) -> dict:
        """
        Converts a `Destination` to a dictionary

        Returns
        -------
        destination: dict
            the destination data mapped to a dictionary that SES expects

        Example
        -------
        ```python
        dest = Destination(
            to_addresses: ["user1@email.com"],
            cc_addresses: ["user2@email.com"],
            bcc_addresses: ["user3@email.com"],
        )

        dest_dict = {
            ToAddresses: ["user1@email.com"],
            CcAddressec: ["user2@email.com"],
            BccAddresses: ["user3@email.com"],
        }

        dest.to_dict() == dest_dict # True
        ```
        """
        return {
            "ToAddresses": self.to_addresses,
            "CcAddresses": self.cc_addresses,
            "BccAddresses": self.bcc_addresses,
        }


class Email(BaseModel):
    """
    Model representing a reduced SES Email
    """

    source: str
    """The email from which the email is sent"""

    destination: Destination
    """The recipients to send the email to"""

    message: Message
    """The message data - subject and body"""

    @classmethod
    def from_dict(cls, obj: dict):
        """
        Converts a dictionary into an Email object.

        Params
        ------
        obj: dict
            a dictionary containing metadata and data about an email

        Returns
        -------
        email: dict
            an `Email` object with the given data

        Example
        -------
        ```python
        email = Email.from_dict({
            source: "sender@email.com",
            to_addresses: ["user1@gmail.com"],
            cc_addresses: ["user2@gmail.com"],
            bcc_addresses: None,
            subject: {
                data: "Urgent Email",
                charset: "UTF-8",
            },
            body: {
                content_type: "Text",
                data: "Hello, world!",,
                charset: "UTF-8",
            },
        })
        ```
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
        """
        Converts an `Email` to a dictionary

        Returns
        -------
        email: dict
            the email data mapped to a dictionary that SES expects

        Example
        -------
        ```python
        email = Email(
            Source="sender@email.com",
            Destination=Destination(
                to_addresses=["user1@gmail.com"],
                cc_addresses=["user2@gmail.com"],
                bcc_addresses=None,
            ),
            Message=Message(
                subject=Subject(
                    data="Urgent Email",
                    charset="UTF-8",
                ),
                body=Body(
                    content_type: "Text",
                    data: "Hello, world!",,
                    charset: "UTF-8",
                ),
            ),
        )

        email_dict = {
            "Source": "sender@email.com",
            "Destination": {
                "ToAddresses": ["user1@email.com"],
                "CcAddresses": ["user2@email.com"],
                "BccAddresses": None,
            },
            "Message": {
                "Subject": {
                    "Data": "Urgent Alert",
                    "Charset": "UTF-8",
                },
                "Body": {
                    "Text": {
                        "Body": "Hello, world!",
                        "Charset": "UTF-8",
                    }
                }
            }
        }

        email.to_dict() == email_dict # True
        ```
        """
        return {
            "Source": self.source,
            "Destination": self.destination.to_dict(),
            "Message": self.message.to_dict(),
        }
