from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Test email configuration'

    def add_arguments(self, parser):
        parser.add_argument('--to', type=str, default='ranamazhar214@gmail.com',
                          help='Recipient email address')

    def handle(self, *args, **options):
        recipient = options['to']
        
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('EMAIL CONFIGURATION TEST'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        # Display settings
        self.stdout.write(f"\nEmail Backend: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"Email Host: {settings.EMAIL_HOST}")
        self.stdout.write(f"Email Port: {settings.EMAIL_PORT}")
        self.stdout.write(f"Email TLS: {settings.EMAIL_USE_TLS}")
        self.stdout.write(f"Email User: {settings.EMAIL_HOST_USER}")
        self.stdout.write(f"Email Password: {'*' * len(settings.EMAIL_HOST_PASSWORD)}")
        
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS('SENDING TEST EMAIL...'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        try:
            result = send_mail(
                subject='Test Email from Django SMS',
                message='This is a test email to verify SMTP configuration is working correctly.\n\nIf you received this email, the email configuration is working!',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient],
                fail_silently=False,
            )
            
            if result == 1:
                self.stdout.write(self.style.SUCCESS('\n✅ SUCCESS! Email sent successfully!'))
                self.stdout.write(f"   From: {settings.EMAIL_HOST_USER}")
                self.stdout.write(f"   To: {recipient}")
                self.stdout.write("\n   Check your inbox for the test email!")
            else:
                self.stdout.write(self.style.ERROR(f'\n❌ FAILED! send_mail returned: {result}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ ERROR: {type(e).__name__}'))
            self.stdout.write(self.style.ERROR(f'   Message: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR('\nFull traceback:'))
            self.stdout.write(traceback.format_exc())
        
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
