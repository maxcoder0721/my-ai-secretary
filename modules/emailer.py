"""Email sender — Gmail SMTP using an App Password."""
from __future__ import annotations

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject: str, html_body: str, plain_fallback: str = "") -> None:
    sender = os.getenv("GMAIL_ADDRESS")
    password = os.getenv("GMAIL_APP_PASSWORD")
    recipient = os.getenv("RECIPIENT_EMAIL", sender)

    if not sender or not password:
        raise RuntimeError(
            "GMAIL_ADDRESS and GMAIL_APP_PASSWORD must be set. "
            "Create a Gmail App Password at https://myaccount.google.com/apppasswords"
        )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    if not plain_fallback:
        plain_fallback = (
            "Your Daily Secretary email is best viewed in an HTML-capable client."
        )

    msg.attach(MIMEText(plain_fallback, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, [recipient], msg.as_string())


if __name__ == "__main__":
    send_email(
        "Daily Secretary — test",
        "<h1>It works!</h1><p>This is a test email.</p>",
        "It works! This is a test email.",
    )
