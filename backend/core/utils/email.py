import smtplib
from http import HTTPStatus
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import urlencode

from fastapi import HTTPException
from sentry_sdk import capture_exception
from tenacity import retry, stop_after_attempt, wait_fixed
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

    @staticmethod
    def _get_link(code: str, email: str, method: str) -> str:
        if method == "verification":
            params = {f"{method}_code": code, "email": email}
            return f"{HOST_URL}activate?{urlencode(params)}"
        if method == "recover":
            params = {f"{method}_code": code}
            return f"{HOST_URL}recover?{urlencode(params)}"

    def _create_message(self, to: str, body: str, subject: str = "LocalUSDT verification message") -> dict:
        msg = {
            "from": f"LocalUSDT {self.email_from}",
            "subject": subject,
            "to": to,
            "html": body,
        }
        return msg

    async def _send_message(self, msg: dict) -> None:
        async with httpx.AsyncClient() as client:
            try:
                resp = (
                    await client.post(
                        self.send_message_link,
                        auth=("api", self.api_key),
                        data=msg,
                    )
                )
            except Exception as e:
                capture_exception(e)
                raise HTTPException(HTTPStatus.BAD_REQUEST, f"Error while sending email, {e}")

        if not resp.text or not resp.json() or resp.json().get("message") != "Queued. Thank you.":
            capture_exception(f"Error while sending email, response - {str(resp.json())}", level="error")

        return None

    async def send_verification_code(self, to: str, code: str) -> None:

        msg = self._create_message(
            to,
            "Добрый день! <br>\n"
            'Перейдите по <a href="{}">этой</a> ссылке для регистрации в LocalUSDT<br>\n'
            "Надеемся вам понравится! До встречи!".format(MailGunEmail._get_link(code, to, method="verification")),
        )

        await self._send_message(msg)

        return None

    async def send_recover_code(self, to: str, code: str) -> None:
        msg = self._create_message(
            to,
            "Добрый день! <br>\n"
            'Перейдите по <a href="{}">этой</a> ссылке для восстановления пароля в LocalUSDT<br>\n'
            "До встречи!".format(MailGunEmail._get_link(code, "", method="recover")),
        )

        await self._send_message(msg)

        return None
