import os
import re

file_path = 'apps/backend/src/edulafia/modules/auth/service.py'
with open(file_path, 'r') as f:
    content = f.read()

# Add import at top
if 'from edulafia.core.email import send_email_async' not in content:
    content = content.replace('from sqlalchemy.ext.asyncio import AsyncSession\n', 'from sqlalchemy.ext.asyncio import AsyncSession\nfrom edulafia.core.email import send_email_async\nimport asyncio\n')

# Find forgot_password method
old_block = """        # In a real implementation, we would send an email with the reset link
        # For now, we'll just log it (or mock it)
        print(f"Password reset link for {email}: {reset_link}")"""

new_block = """        # Send actual email asynchronously
        body = f\"\"\"
        <p>Hello,</p>
        <p>You requested a password reset for your EduLafia account.</p>
        <p>Please click the link below to reset your password:</p>
        <p><a href="{reset_link}">{reset_link}</a></p>
        <p>If you did not request this, please ignore this email.</p>
        \"\"\"
        asyncio.create_task(send_email_async(
            to_email=email,
            subject="EduLafia - Password Reset Request",
            body=body
        ))"""

content = content.replace(old_block, new_block)

with open(file_path, 'w') as f:
    f.write(content)

print("Patched auth/service.py")
