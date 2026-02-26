import smtplib
from email.message import EmailMessage
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from apps.admin.repositories.app_setting_repository import AppSettingRepository

async def get_smtp_config(session: AsyncSession) -> dict:
    repo = AppSettingRepository(session)
    settings = await repo.get_all_settings(group="mail")
    
    config = {
        "smtp_host": "",
        "smtp_port": "587",
        "smtp_username": "",
        "smtp_password": "",
        "smtp_from_email": "",
        "smtp_from_name": "FastAPI App"
    }
    
    for setting in settings:
        if setting.key in config:
            config[setting.key] = setting.value
            
    return config

async def send_reset_password_email(email: str, reset_link: str, session: AsyncSession) -> bool:
    config = await get_smtp_config(session)
    
    if not config.get("smtp_host"):
        print("SMTP host not configured. Cannot send email.")
        return False
        
    msg = EmailMessage()
    msg['Subject'] = 'Reset your password'
    msg['From'] = f"{config.get('smtp_from_name')} <{config.get('smtp_from_email')}>"
    msg['To'] = email
    
    msg.set_content(f"""\
Hello,

You have requested to reset your password.
Please click on the link below to reset it:
{reset_link}

If you did not request a password reset, no further action is required.

Regards,
{config.get('smtp_from_name')}
""")

    msg.add_alternative(f"""\
<html>
  <body>
    <p>Hello,</p>
    <p>You have requested to reset your password.</p>
    <p>Please click on the link below to reset it:</p>
    <p><a href="{reset_link}">{reset_link}</a></p>
    <p>If you did not request a password reset, no further action is required.</p>
    <p>Regards,<br>{config.get('smtp_from_name')}</p>
  </body>
</html>
""", subtype='html')

    try:
        # We need to run SMTP in a thread because it's blocking
        import asyncio
        loop = asyncio.get_running_loop()
        
        def send_email_sync():
            port = int(config.get("smtp_port", 587))
            
            # Decide SSL vs TLS based on port usually
            if port == 465:
                with smtplib.SMTP_SSL(config["smtp_host"], port) as smtp:
                    smtp.login(config["smtp_username"], config["smtp_password"])
                    smtp.send_message(msg)
            else:
                with smtplib.SMTP(config["smtp_host"], port) as smtp:
                    smtp.starttls()
                    smtp.login(config["smtp_username"], config["smtp_password"])
                    smtp.send_message(msg)
                    
        await loop.run_in_executor(None, send_email_sync)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
