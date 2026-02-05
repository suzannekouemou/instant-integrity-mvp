from __future__ import annotations

import logging
from typing import Optional

from .config import get_settings

logger = logging.getLogger(__name__)


class EmailSender:
    """Lightweight email sender facade.

    Phase 1 note: provides a safe no-op when email is not configured.
    Real SMTP/SendGrid integration can be added later behind the same
    interface without changing call sites.
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        self.enabled = bool(
            (self.settings.SMTP_HOST and self.settings.SMTP_USER and self.settings.SMTP_PASSWORD)
            or self.settings.SENDGRID_API_KEY
        )

    async def send_email(self, to_email: str, subject: str, html_body: str, plain_body: Optional[str] = None) -> bool:
        if not self.enabled:
            logger.info("Email disabled; pretending to send email to %s (subject=%s)", to_email, subject)
            return True  # No-op success to keep flows moving in dev

        # Placeholder implementation (no network IO in Phase 1 scaffolding)
        logger.info(
            "Email configured but sending is stubbed. Would send to=%s from=%s subject=%s",
            to_email,
            self.settings.FROM_EMAIL,
            subject,
        )
        return True


def get_email_sender() -> EmailSender:
    return EmailSender()
