from django.db import models

class HouseUser(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    house_number = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)
    reset_token = models.CharField(max_length=255,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

class ServiceRequest(models.Model):
    CATEGORY_CHOICES = [
        ('PLUMBER', 'Plumber'),
        ('ELECTRICIAN', 'Electrician'),
        ('CLEANING', 'Cleaning'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(HouseUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

# Create your models here.
