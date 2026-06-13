#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'societymanagementsystem.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 60)
print("EMAIL CONFIGURATION TEST")
print("=" * 60)

# Check settings
print(f"\n✓ EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"✓ EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"✓ EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"✓ EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"✓ EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"✓ EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD)}")

# Test sending email
print("\n" + "=" * 60)
print("TESTING EMAIL SEND...")
print("=" * 60)

try:
    result = send_mail(
        subject='Test Email from Django',
        message='This is a test email to verify SMTP configuration is working correctly.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['ranamazhar214@gmail.com'],
        fail_silently=False,
    )
    
    if result == 1:
        print("\n✅ SUCCESS! Email sent successfully!")
        print(f"   From: {settings.EMAIL_HOST_USER}")
        print(f"   To: ranamazhar214@gmail.com")
        print(f"   Check your Gmail inbox for the test email")
    else:
        print(f"\n❌ FAILED! send_mail returned: {result}")
        
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"   Message: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
