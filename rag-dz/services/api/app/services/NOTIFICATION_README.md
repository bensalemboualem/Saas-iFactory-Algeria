# Notification Service - Automated Welcome Emails

## Overview

The Notification Service automatically sends profile-specific welcome emails when users register, complete with a **100 free token gift** and a comprehensive Quick Start Guide.

---

## Features

### 1. Profile-Specific Templates

**Geneva Psychologist (iafactory.ch)**:
- Subject: "Your Private AI Assistant is Ready | IA Factory Switzerland 🇨🇭"
- Focus: Security, confidentiality, time-saving
- Highlights: Stress Detection, nLPD Compliance, Clinical Summaries
- Color scheme: Red gradient (#ef4444 → #b91c1c)

**Algeria Education (iafactoryalgeria.com)**:
- Subject: "Welcome to the Future of Education | IA Factory Algeria 🇩🇿"
- Focus: Innovation, bilingual support, knowledge capture
- Highlights: Personal Lexicon, Bilingual Summaries FR/AR, Knowledge Extraction
- Color scheme: Green gradient (#22c55e → #15803d)

### 2. Welcome Token Gift

Each new user receives:
- **100 free tokens** to test the system
- Unique redeem code (format: `WELCOME-XXXX-XXXX-XXXX`)
- Auto-generated and included in welcome email

### 3. Quick Start Guide (3 Steps)

Every email includes:
1. **Record**: Click the central pulse microphone
2. **Analyze**: Stop to receive instant transcription
3. **Export**: Download summary or copy to other systems

### 4. Multi-Language Support

- **Psychologist**: English (Swiss professional standards)
- **Education**: French + Arabic (Algerian bilingual education)

---

## Configuration

### Environment Variables

Add to `.env`:

```bash
# SMTP Configuration for Email Notifications
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@iafactory.pro

# Optional: If not configured, emails will be logged instead of sent
```

### Gmail Setup (Recommended)

1. Enable 2-Factor Authentication on your Google Account
2. Generate an App Password:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Enter "IA Factory Notifications"
   - Copy the 16-character password
3. Use this password for `SMTP_PASSWORD`

---

## Usage

### Automatic Sending (Registration)

Emails are automatically sent when users register via `/api/auth/register`.

The system:
1. Detects user profile from domain (origin/host header)
2. Generates a unique welcome code
3. Sends profile-specific email
4. Logs result (success or failure with manual code)

### Manual Sending (API)

```python
from app.services.notification_service import get_notification_service
from app.prompts import UserProfile, DomainContext

# Get service
notification_service = get_notification_service()

# Send welcome email
result = notification_service.send_welcome_email(
    to_email="user@example.com",
    user_name="Dr. Smith",
    profile=UserProfile.PSYCHOLOGIST,
    domain_context=DomainContext.SWITZERLAND,
    tenant_id="814c132a-1cdd-4db6-bc1f-21abd21ec37d"
)

# Check result
if result["success"]:
    print(f"Email sent! Redeem code: {result['redeem_code']}")
else:
    print(f"Email failed: {result['error']}")
    print(f"Manual code for user: {result['redeem_code']}")
```

---

## Email Templates

### Location

```
backend/rag-compat/app/templates/emails/
├── psychologist_welcome.html    # Geneva Psychologist (HTML)
├── psychologist_welcome.txt     # Geneva Psychologist (Plain text)
├── education_welcome.html       # Algeria Education (HTML)
└── education_welcome.txt        # Algeria Education (Plain text)
```

### Template Variables

All templates support these variables:

- `{{user_name}}` - User's full name
- `{{redeem_code}}` - Unique welcome code (e.g., WELCOME-A1B2-C3D4-E5F6)
- `{{token_amount}}` - Number of free tokens (default: 100)
- `{{current_year}}` - Current year (e.g., 2025)
- `{{tagline}}` - Profile-specific tagline
- `{{focus}}` - Profile focus area
- `{{flag}}` - Country flag emoji
- `{{support_email}}` - Support email address
- `{{dashboard_url}}` - Dashboard URL
- `{{privacy_note}}` - (Psychologist only) Privacy compliance note
- `{{innovation_note}}` - (Education only) Innovation focus note
- `{{feature1}}`, `{{feature2}}`, `{{feature3}}` - Profile-specific features

### Customization

To customize templates:

1. Edit the HTML/TXT files directly
2. Use `{{variable_name}}` for dynamic content
3. Test with `notification_service.send_welcome_email()`
4. Templates are auto-detected by profile

---

## Testing

### Test Email Sending (No SMTP)

If SMTP is not configured, emails are logged to console:

```
[EMAIL] Would send to user@example.com: Your Private AI Assistant is Ready | IA Factory Switzerland
[EMAIL] Redeem code in body
```

### Test with Real SMTP

```python
from app.services.notification_service import NotificationService
from app.prompts import UserProfile, DomainContext

# Create service with SMTP credentials
service = NotificationService(
    smtp_host="smtp.gmail.com",
    smtp_port=587,
    smtp_user="your-email@gmail.com",
    smtp_password="your-app-password",
    from_email="noreply@iafactory.pro"
)

# Send test email
result = service.send_welcome_email(
    to_email="test@example.com",
    user_name="Test User",
    profile=UserProfile.PSYCHOLOGIST,
    domain_context=DomainContext.SWITZERLAND,
    redeem_code="WELCOME-TEST-1234-5678"  # Optional: use custom code
)

print(result)
```

---

## Additional Features

### Token Low Reminder

Send reminder when user's balance is low:

```python
service = get_notification_service()

result = service.send_token_low_reminder(
    to_email="user@example.com",
    user_name="Dr. Smith",
    current_balance=50,
    profile=UserProfile.PSYCHOLOGIST
)
```

### Welcome Code Generation

Generate secure codes without sending email:

```python
service = get_notification_service()

# Generate with default prefix (WELCOME)
code = service.generate_welcome_code()
# Result: WELCOME-A1B2-C3D4-E5F6

# Generate with custom prefix
code = service.generate_welcome_code(prefix="PROMO")
# Result: PROMO-X9Y8-Z7W6-V5U4
```

---

## Production Checklist

Before deploying to production:

- [ ] Configure SMTP credentials in `.env`
- [ ] Test email delivery to both Gmail and Outlook
- [ ] Verify profile detection from domain headers
- [ ] Test both HTML and plain text rendering
- [ ] Set up SPF/DKIM records for your domain
- [ ] Monitor email delivery logs
- [ ] Test welcome code redemption flow
- [ ] Verify token balance updates after code redemption

---

## Troubleshooting

### Emails Not Sending

1. **Check SMTP credentials**: Verify `SMTP_USER` and `SMTP_PASSWORD`
2. **Check firewall**: Ensure port 587 is open
3. **Check logs**: Look for error messages in console
4. **Test SMTP manually**: Use telnet to verify SMTP server

### Emails in Spam

1. **Add SPF record**: Authorize your sending domain
2. **Set up DKIM**: Add email signing
3. **Check content**: Avoid spam trigger words
4. **Use professional email**: Don't use personal Gmail

### Wrong Template Sent

1. **Check domain detection**: Verify `origin` or `host` headers
2. **Check template files**: Ensure files exist in `templates/emails/`
3. **Check profile mapping**: Verify `get_user_profile_from_domain()` logic

---

## Future Enhancements

Planned features:

- [ ] Email queuing system (Celery/Redis)
- [ ] Email analytics (open rate, click rate)
- [ ] Transactional email tracking
- [ ] Custom template editor (admin UI)
- [ ] A/B testing for email content
- [ ] Multi-language template support (i18n)
- [ ] SMS notifications (Twilio integration)
- [ ] Push notifications (Firebase)

---

## Support

For issues or questions:
- Email: support@iafactory.pro
- Documentation: `/docs/notifications`
- GitHub Issues: https://github.com/iafactory/rag-dz/issues

---

**Built with ❤️ for IA Factory - Privacy & Precision (🇨🇭) | Shaping the Future (🇩🇿)**
