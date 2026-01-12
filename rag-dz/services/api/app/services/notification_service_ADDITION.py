"""
ADD THIS METHOD TO NotificationService class in notification_service.py
Insert after the send_welcome_email() method (around line 242)
"""

def send_reset_password_email(
    self,
    to_email: str,
    user_name: str,
    reset_url: str,
    profile: UserProfile,
    domain_context: DomainContext,
) -> Dict[str, Any]:
    """
    Send password reset email with secure token link.

    Args:
        to_email: Recipient email address
        user_name: User's name
        reset_url: Complete reset URL with token
        profile: User profile (determines branding)
        domain_context: Domain context (SWITZERLAND, ALGERIA, GENEVA)

    Returns:
        Result dict with success status
    """
    # Get profile metadata for branding
    metadata = get_profile_metadata(profile, domain_context)

    # Determine domain string
    if domain_context == DomainContext.SWITZERLAND:
        domain = "iafactory.ch"
    elif domain_context == DomainContext.ALGERIA:
        domain = "iafactoryalgeria.com"
    else:
        domain = "iafactory.pro"

    # Prepare template variables
    variables = {
        "user_name": user_name,
        "reset_url": reset_url,
        "domain": domain,
        "flag": metadata.get("flag", "🌍"),
        "tagline": metadata.get("tagline", "IA Factory"),
        "gradient": metadata.get("gradient", "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"),
        "primary_color": metadata.get("primary_color", "#667eea"),
    }

    # Load templates from reset_password.html and reset_password.txt
    template_dir = os.path.join(os.path.dirname(__file__), "..", "templates", "emails")

    # Read HTML template
    try:
        html_path = os.path.join(template_dir, "reset_password.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html_template = f.read()
            # Replace variables
            for key, value in variables.items():
                html_template = html_template.replace("{{ " + key + " }}", str(value))
            html_body = html_template
    except Exception as e:
        # Fallback HTML
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2>Réinitialisation de mot de passe</h2>
            <p>Bonjour {user_name},</p>
            <p>Cliquez sur le lien ci-dessous pour réinitialiser votre mot de passe:</p>
            <p><a href="{reset_url}" style="background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; display: inline-block;">Réinitialiser mon mot de passe</a></p>
            <p style="color: #666; font-size: 14px;">Ce lien expire dans 1 heure.</p>
        </body>
        </html>
        """

    # Read text template
    try:
        txt_path = os.path.join(template_dir, "reset_password.txt")
        with open(txt_path, "r", encoding="utf-8") as f:
            txt_template = f.read()
            # Replace variables
            for key, value in variables.items():
                txt_template = txt_template.replace("{{ " + key + " }}", str(value))
            text_body = txt_template
    except Exception as e:
        # Fallback text
        text_body = f"""
Réinitialisation de mot de passe - IA Factory

Bonjour {user_name},

Cliquez sur le lien ci-dessous pour réinitialiser votre mot de passe:
{reset_url}

Ce lien expire dans 1 heure.

Cordialement,
L'équipe IA Factory
        """

    # Send email
    subject = "Réinitialisation de mot de passe | IA Factory"

    try:
        result = self._send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body,
        )

        return {
            "success": True,
            "sent_at": datetime.utcnow().isoformat(),
            "to_email": to_email,
            **result,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
