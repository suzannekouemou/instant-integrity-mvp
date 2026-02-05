from app.core.email import get_email_sender
from app.core.config import get_settings


async def send_verification_email(to_email: str, token: str) -> bool:
    """Send email verification link to user."""
    settings = get_settings()
    sender = get_email_sender()
    
    verification_url = f"http://localhost:8000/api/v1/auth/verify-email?token={token}"
    
    subject = "Verify your email - Instant Integrity"
    html_body = f"""
    <html>
        <body>
            <h2>Welcome to Instant Integrity!</h2>
            <p>Please verify your email address by clicking the link below:</p>
            <p><a href="{verification_url}">Verify Email</a></p>
            <p>This link will expire in {settings.VERIFICATION_TOKEN_EXPIRY_HOURS} hours.</p>
            <p>If you didn't create an account, please ignore this email.</p>
        </body>
    </html>
    """
    
    plain_body = f"""
    Welcome to Instant Integrity!
    
    Please verify your email address by visiting:
    {verification_url}
    
    This link will expire in {settings.VERIFICATION_TOKEN_EXPIRY_HOURS} hours.
    
    If you didn't create an account, please ignore this email.
    """
    
    return await sender.send_email(to_email, subject, html_body, plain_body)
