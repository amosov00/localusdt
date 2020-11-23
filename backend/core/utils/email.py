import smtplib
from http import HTTPStatus
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import urlencode
from jinja2 import Environment, select_autoescape, FileSystemLoader

from fastapi import HTTPException
from sentry_sdk import capture_message, capture_exception
import httpx

from config import (
    EMAIL_LOGIN,
    EMAIL_PASSWORD,
    EMAIL_PORT,
    EMAIL_SERVER,
    HOST_URL,
    MAILGUN_MESSAGE_LINK,
    MAILGUN_DOMAIN_NAME,
    MAILGUN_API_KEY
)


__all__ = [
    "Email",
    "MailGunEmail"
]


class Email:
    def __init__(self):
        self.email_from = EMAIL_LOGIN
        self.password = EMAIL_PASSWORD
        self.port = EMAIL_PORT
        self.server = EMAIL_SERVER
        self.mailserver = smtplib.SMTP_SSL(self.server, self.port)

    @staticmethod
    def _get_link(code: str, email: str, method: str) -> str:
        if method == "verification":
            params = {f"{method}_code": code, "email": email}
            return f"{HOST_URL}activate?{urlencode(params)}"
        if method == "recover":
            params = {f"{method}_code": code}
            return f"{HOST_URL}recover?{urlencode(params)}"

    def login(self) -> None:
        try:
            self.mailserver.login(self.email_from, self.password)
            return None
        except Exception as e:
            capture_exception(e)
            raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, "Error while sending email")

    def create_message(self, to: str, body: str) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg["From"] = self.email_from
        msg["Subject"] = "LocalUSDT"
        msg["To"] = to
        msg.attach(MIMEText(body, "html"))
        return msg

    def send_message(self, to: str, text: str):
        try:
            self.mailserver.sendmail(self.email_from, to, text)
            return None
        except Exception as e:
            capture_exception(e)
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Error while sending email")

    async def send_verification_code(self, to: str, code: str) -> None:
        self.login()
        link = Email._get_link(code, to, method="verification")

        msg = self.create_message(
            to,
            "Добрый день! <br>\n"
            'Перейдите по <a href="{}">этой</a> ссылке для регистрации в LocalUSDT<br>\n'
            "Надеемся вам понравится! До встречи!\n"
            "Или нажмите на эту ссылку: ".format(link, link),
        )
        self.send_message(to, msg.as_string())
        self.mailserver.quit()
        return None

    async def send_recover_code(self, to: str, code: str) -> None:
        self.login()
        msg = self.create_message(
            to,
            "Добрый день! <br>\n"
            'Перейдите по <a href="{}">этой</a> ссылке для восстановления пароля в LocalUSDT<br>\n'
            "До встречи!".format(Email._get_link(code, "", method="recover")),
        )
        self.send_message(to, msg.as_string())
        self.mailserver.quit()
        return None


class MailGunEmail:
    def __init__(self):
        self.api_key = MAILGUN_API_KEY
        self.domain = MAILGUN_DOMAIN_NAME
        self.send_message_link = MAILGUN_MESSAGE_LINK
        self.email_from = EMAIL_LOGIN
        self.template_env = Environment(
            loader=FileSystemLoader('templates/'),
            autoescape=select_autoescape(['html'])
        )

    @staticmethod
    def _get_link(**kwargs) -> str:
        method = kwargs.get("method")
        code = kwargs.get("code")
        email = kwargs.get("email")

        if method == "verification":
            params = {f"{method}_code": code, "email": email}
            return f"{HOST_URL}activate?{urlencode(params)}"
        if method == "recover":
            params = {f"{method}_code": code}
            return f"{HOST_URL}recover?{urlencode(params)}"
        if method == "notification":
            return f"{HOST_URL}invoice/{kwargs.get('invoice_id')}"

    def create_message(self, to: str, body_html: str, body: str, method: str) -> dict:
        msg = {
            "from": f"LocalUSDT {method} {self.email_from}",
            "subject": f"LocalUSDT {method} message",
            "to": to,
            "html": body_html,
            "text": body
        }
        return msg

    async def _send_message(self, msg: dict) -> None:
        async with httpx.AsyncClient() as client:
            try:
                email_send = (
                    await client.post(
                        self.send_message_link,

                        auth=("api", self.api_key),
                        data=msg,
                    )
                )
            except Exception as e:
                capture_exception(e)
                raise HTTPException(HTTPStatus.BAD_REQUEST, f"Error while sending email, {e}")

        if email_send and email_send.json().get("message") != "Queued. Thank you.":
            capture_message(f"Error while sending email, response - {str(email_send.json())} ")
            raise HTTPException(HTTPStatus.BAD_REQUEST, f"Error while sending email, {str(email_send.json())}")

        return None

    def _get_template_body(self, msg_type: str, **kwargs):
        return self.template_env.get_template(f"{msg_type}.html").render(
            **kwargs
        )

    async def send_verification_code(self, to: str, code: str) -> None:
        link = MailGunEmail._get_link(code=code, email=to, method="verification")
        msg_body = self._get_template_body('verification', link=link, to=to)

        msg = self.create_message(
            to,
            msg_body,
            msg_body,
            "verification"
        )

        await self._send_message(msg)

        return None

    async def send_recover_code(self, to: str, code: str) -> None:
        link = MailGunEmail._get_link(code=code, method="recover")
        msg_body = self._get_template_body('recover', link=link, to=to)

        msg = self.create_message(
            to,
            msg_body,
            msg_body,
            "recover"
        )

        await self._send_message(msg)

        return None

    async def send_invoice_notification(self, to: str, invoice_id: str) -> None:
        link = MailGunEmail._get_link(invoice_id=invoice_id, method="notification")
        msg_body = self._get_template_body('notification', link=link, to=to)

        msg = self.create_message(
            to,
            msg_body,
            msg_body,
            "notification"
        )

        await self._send_message(msg)

        return None

    async def send_invoice_notification_to_seller(self, to: str, invoice_id: str) -> None:
        link = MailGunEmail._get_link(invoice_id=invoice_id, method="notification")
        msg_body = self._get_template_body('notification_invoice_seller', link=link, to=to)

        msg = self.create_message(
            to,
            msg_body,
            msg_body,
            "invoice notification"
        )

        await self._send_message(msg)

        return None
