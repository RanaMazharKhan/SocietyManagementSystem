#!/usr/bin/env python
"""
Email Configuration Diagnostic Script
Tests if email is properly configured in Django
"""
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.getcwd())

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'societymanagementsystem.settings')

try:
    import django
    django.setup()
    print("✅ Django imported successfully")
except Exception as e:
    print(f"❌ Failed to import Django: {e}")
    sys.exit(1)

from django.conf import settings
from django.core.mail import send_mail

print("\n" + "="*70)
print("EMAIL CONFIGURATION DIAGNOSTIC")
print("="*70)

# Check settings
print("\n📋 EMAIL SETTINGS:")
print(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"  EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD)} (length: {len(settings.EMAIL_HOST_PASSWORD)})")

# Check if password is valid
if len(settings.EMAIL_HOST_PASSWORD) < 5:
    print("\n⚠️  WARNING: Password seems too short!")
    print("   Make sure you've set a valid Gmail App Password")

print("\n" + "="*70)
print("TESTING EMAIL SEND TO: ranamazhar214@gmail.com")
print("="*70)

try:
    # Send test email
    result = send_mail(
        subject='[TEST] Django Email Configuration',
        message='If you received this email, your Django email configuration is working correctly!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['ranamazhar214@gmail.com'],
        fail_silently=False,
    )
    
    print(f"\n✅ SUCCESS!")
    print(f"   Email sent successfully (result: {result})")
    print(f"   Check your Gmail inbox for the test email")
    
except Exception as e:
    print(f"\n❌ ERROR SENDING EMAIL")
    print(f"   Exception Type: {type(e).__name__}")
    print(f"   Exception Message: {str(e)}")
    print(f"\nFull error details:")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
