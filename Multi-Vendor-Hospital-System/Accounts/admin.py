from django.contrib import admin

from .models import User, Notification

# Register your models here.


class UserAttr(admin.ModelAdmin):
    list_display = ["uuid", "first_name", "gender", "email", "contact_number"]


admin.site.register(User, UserAttr)


class NotificationAttr(admin.ModelAdmin):
    list_display = ["recipient", "notification_head", "content", "is_read"]


admin.site.register(Notification, NotificationAttr)
