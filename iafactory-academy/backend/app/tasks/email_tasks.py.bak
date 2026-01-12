"""
Email tasks using Celery for asynchronous email sending.
"""
from typing import Optional
import logging

# Note: Celery instance should be initialized in a separate celery_app.py file
# This is a placeholder for the actual Celery implementation

logger = logging.getLogger(__name__)


def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: Optional[str] = None
) -> bool:
    """
    Send email using SendGrid (placeholder for actual implementation).
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML email content
        text_content: Plain text email content
        
    Returns:
        bool: True if sent successfully
    """
    # TODO: Implement actual SendGrid integration
    logger.info(f"Sending email to {to_email}: {subject}")
    return True


def send_verification_email(email: str, token: str) -> bool:
    """
    Send email verification link.
    
    Args:
        email: User email
        token: Verification token
        
    Returns:
        bool: True if sent successfully
    """
    subject = "Verify your email - IAFactory Academy"
    verification_url = f"https://iafactory-academy.com/verify-email?token={token}"
    
    html_content = f"""
    <html>
        <body>
            <h2>Welcome to IAFactory Academy!</h2>
            <p>Please verify your email address by clicking the link below:</p>
            <p><a href="{verification_url}">Verify Email</a></p>
            <p>This link will expire in 24 hours.</p>
            <p>If you didn't create an account, please ignore this email.</p>
        </body>
    </html>
    """
    
    text_content = f"""
    Welcome to IAFactory Academy!
    
    Please verify your email address by visiting:
    {verification_url}
    
    This link will expire in 24 hours.
    
    If you didn't create an account, please ignore this email.
    """
    
    return send_email(email, subject, html_content, text_content)


def send_password_reset_email(email: str, token: str) -> bool:
    """
    Send password reset link.
    
    Args:
        email: User email
        token: Reset token
        
    Returns:
        bool: True if sent successfully
    """
    subject = "Reset your password - IAFactory Academy"
    reset_url = f"https://iafactory-academy.com/reset-password?token={token}"
    
    html_content = f"""
    <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>You requested to reset your password. Click the link below to proceed:</p>
            <p><a href="{reset_url}">Reset Password</a></p>
            <p>This link will expire in 1 hour.</p>
            <p>If you didn't request this, please ignore this email.</p>
        </body>
    </html>
    """
    
    text_content = f"""
    Password Reset Request
    
    You requested to reset your password. Visit:
    {reset_url}
    
    This link will expire in 1 hour.
    
    If you didn't request this, please ignore this email.
    """
    
    return send_email(email, subject, html_content, text_content)


def send_enrollment_confirmation_email(
    email: str,
    user_name: str,
    course_title: str,
    course_url: str
) -> bool:
    """
    Send enrollment confirmation email.
    
    Args:
        email: User email
        user_name: User's name
        course_title: Course title
        course_url: Course URL
        
    Returns:
        bool: True if sent successfully
    """
    subject = f"Welcome to {course_title}!"
    
    html_content = f"""
    <html>
        <body>
            <h2>Enrollment Confirmation</h2>
            <p>Hi {user_name},</p>
            <p>You've successfully enrolled in <strong>{course_title}</strong>!</p>
            <p>Start learning now:</p>
            <p><a href="{course_url}">Go to Course</a></p>
            <p>Happy learning!</p>
        </body>
    </html>
    """
    
    text_content = f"""
    Enrollment Confirmation
    
    Hi {user_name},
    
    You've successfully enrolled in {course_title}!
    
    Start learning now: {course_url}
    
    Happy learning!
    """
    
    return send_email(email, subject, html_content, text_content)


def send_certificate_notification_email(
    email: str,
    user_name: str,
    course_title: str,
    certificate_url: str
) -> bool:
    """
    Send certificate generation notification.
    
    Args:
        email: User email
        user_name: User's name
        course_title: Course title
        certificate_url: Certificate download URL
        
    Returns:
        bool: True if sent successfully
    """
    subject = f"🎓 Certificate of Completion - {course_title}"
    
    html_content = f"""
    <html>
        <body>
            <h2>Congratulations, {user_name}! 🎉</h2>
            <p>You've successfully completed <strong>{course_title}</strong>!</p>
            <p>Your certificate of completion is ready:</p>
            <p><a href="{certificate_url}">Download Certificate</a></p>
            <p>Share your achievement on LinkedIn and social media!</p>
            <p>Keep up the great work!</p>
        </body>
    </html>
    """
    
    text_content = f"""
    Congratulations, {user_name}!
    
    You've successfully completed {course_title}!
    
    Your certificate of completion is ready:
    {certificate_url}
    
    Share your achievement on LinkedIn and social media!
    
    Keep up the great work!
    """
    
    return send_email(email, subject, html_content, text_content)


def send_payment_confirmation_email(
    email: str,
    user_name: str,
    course_title: str,
    amount: float,
    currency: str = "USD"
) -> bool:
    """
    Send payment confirmation email.
    
    Args:
        email: User email
        user_name: User's name
        course_title: Course title
        amount: Payment amount
        currency: Payment currency
        
    Returns:
        bool: True if sent successfully
    """
    subject = "Payment Confirmation - IAFactory Academy"
    
    html_content = f"""
    <html>
        <body>
            <h2>Payment Confirmed</h2>
            <p>Hi {user_name},</p>
            <p>Your payment for <strong>{course_title}</strong> has been confirmed.</p>
            <p><strong>Amount:</strong> {amount:.2f} {currency}</p>
            <p>You now have full access to the course.</p>
            <p>Thank you for your purchase!</p>
        </body>
    </html>
    """
    
    text_content = f"""
    Payment Confirmed
    
    Hi {user_name},
    
    Your payment for {course_title} has been confirmed.
    
    Amount: {amount:.2f} {currency}
    
    You now have full access to the course.
    
    Thank you for your purchase!
    """
    
    return send_email(email, subject, html_content, text_content)
