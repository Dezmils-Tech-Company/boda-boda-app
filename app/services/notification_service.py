import re
from typing import Optional

import anyio
from loguru import logger
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from app.core.config import settings

PHONE_NORMALIZATION = re.compile(r"[^0-9+]")


def _normalize_phone(phone: str) -> str:
    if not phone:
        raise ValueError("Phone number is required for SMS notifications")

    text = PHONE_NORMALIZATION.sub("", phone)
    if text.startswith("0"):
        return "+" + text[1:]
    if text.startswith("7") and len(text) == 9:
        return "+254" + text
    if not text.startswith("+"):
        return "+" + text
    return text


def _build_twilio_client() -> Client:
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        raise RuntimeError("Twilio credentials are not configured")
    return Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


async def send_notification(phone: str, message: str, sender: Optional[str] = None) -> dict:
    normalized_phone = _normalize_phone(phone)
    from_phone = sender or settings.TWILIO_FROM_PHONE
    if not from_phone:
        raise RuntimeError("TWILIO_FROM_PHONE is not configured")

    client = _build_twilio_client()

    def send_message_sync() -> dict:
        message_obj = client.messages.create(
            body=message,
            from_=from_phone,
            to=normalized_phone,
        )
        return {
            "sid": message_obj.sid,
            "status": message_obj.status,
            "to": message_obj.to,
            "from": message_obj.from_,
            "error_code": message_obj.error_code,
            "error_message": message_obj.error_message,
        }

    try:
        result = await anyio.to_thread.run_sync(send_message_sync)
        logger.info("Twilio SMS sent", phone=normalized_phone, sid=result["sid"])
        return result
    except TwilioRestException as exc:
        logger.error(
            "Twilio failure",
            phone=normalized_phone,
            status=exc.status,
            code=exc.code,
            msg=str(exc),
        )
        raise
    except Exception as exc:
        logger.error("Unexpected SMS failure", phone=normalized_phone, error=str(exc))
        raise