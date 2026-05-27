import asyncio
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from edulafia.config import settings

logger = logging.getLogger(__name__)


def _send_smtp(smtp_server: str, smtp_port: int, smtp_user: str, smtp_password: str, to_email: str, subject: str, body: str) -> bool:
    """Synchronous SMTP send — runs in thread pool to avoid blocking the event loop."""
    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.send_message(msg)
    server.quit()
    logger.info("Email sent successfully to %s", to_email)
    return True


async def send_email_async(to_email: str, subject: str, body: str) -> bool:
    """Send an email using SMTP. Runs in thread pool to avoid blocking. Returns False if SMTP is not configured."""
    smtp_server = settings.SMTP_HOST
    smtp_port = settings.SMTP_PORT
    smtp_user = settings.SMTP_USER
    smtp_password = settings.SMTP_PASSWORD

    if not all([smtp_server, smtp_user, smtp_password]):
        logger.warning(
            "SMTP not fully configured. Email to %s was NOT sent. "
            "Set SMTP_SERVER, SMTP_USER, and SMTP_PASSWORD to enable email.",
            to_email,
        )
        return False

    try:
        await asyncio.to_thread(
            _send_smtp,
            smtp_server, smtp_port, smtp_user, smtp_password,
            to_email, subject, body,
        )
        return True
    except Exception as e:
        logger.error("Failed to send email to %s: %s", to_email, str(e))
        return False