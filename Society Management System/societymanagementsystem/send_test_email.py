#!/usr/bin/env python
"""Send test activation email to ranamazhar1450@gmail.com"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'societymanagementsystem.settings')
django.setup()

from SMSApp.models import HouseUser
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings

print("=" * 70)
print("CREATING TEST USER AND SENDING ACTIVATION EMAIL")
print("=" * 70)

# Check if user already exists
test_email = 'ranamazhar1450@gmail.com'
try:
    user = HouseUser.objects.get(email=test_email)
    print(f"\n✓ User already exists: {user.name} (ID: {user.id})")
except HouseUser.DoesNotExist:
    print(f"\n✓ Creating new user...")
    user = HouseUser.objects.create(
        name='Test User',
        email=test_email,
        password=make_password('test123456'),
        house_number='A-101',
        phone_number='03001234567',
        is_active=False
    )
    print(f"✓ User created: {user.name} (ID: {user.id})")

print(f"\n📋 User Details:")
print(f"   Name: {user.name}")
print(f"   Email: {user.email}")
print(f"   House Number: {user.house_number}")
print(f"   Phone: {user.phone_number}")
print(f"   is_active: {user.is_active}")

# Send activation email
activation_link = f"http://127.0.0.1:8000/activate/{user.id}/"
print(f"\n📧 Email Configuration:")
print(f"   From: {settings.EMAIL_HOST_USER}")
print(f"   To: {user.email}")
print(f"   Link: {activation_link}")

print(f"\n" + "=" * 70)
print("SENDING EMAIL...")
print("=" * 70)

try:
    result = send_mail(
        subject='Activate Your Account',
        message=f'Click the link to activate your account: {activation_link}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )
    
    if result == 1:
        print(f"\n✅ SUCCESS!")
        print(f"   Email sent to: {user.email}")
        print(f"   Activation link: {activation_link}")
        print(f"\n📌 Please check your email inbox at {user.email}")
        print(f"   (The email should contain the activation link)")
    else:
        print(f"\n⚠️  Result: {result}")
        
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"   Message: {str(e)}")
    import traceback
    print(f"\nFull traceback:")
    traceback.print_exc()

print("\n" + "=" * 70)
