from django.contrib import admin
from .models import ServiceRequest, Announcement, HouseUser

admin.site.register(HouseUser)
admin.site.register(ServiceRequest)
admin.site.register(Announcement)

# Register your models here.
admin.site.site_header = "S0CIETY MANAGEMENT SYSTEM"
admin.site.site_title = "ADMIN PORTAL"