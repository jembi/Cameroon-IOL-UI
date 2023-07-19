from django.contrib import admin

from ..functions.NotificationConfigImpl import NotificationConfigImpl
from ..models import DispatcherConfig, NotificationConfig
import requests
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib import messages


class NotificationConfigAdmin(admin.ModelAdmin):
    list_display = ('app_id', 'admin_email', 'host', 'port', 'username', 'date_created', 'date_changed',)
    search_fields = ('admin_email',)
    list_per_page = 15

    def has_add_permission(self, request):
        count = NotificationConfig.objects.all().count()
        if count == 0:
            return True
        return False

    def get_queryset(self, request):
        notificationConfigInit()
        query = super(NotificationConfigAdmin, self).get_queryset(request)
        return query


def notificationConfigInit():
    jsonData = NotificationConfigImpl().getAndRefreshNotificationConfig()
    if jsonData:
        notificationConfig = NotificationConfig.objects.filter()
        app_id = jsonData.get("AppID")
        emails = get_admin_emails(jsonData)
        host = jsonData.get("smtp_config").get("host")
        port = jsonData.get("smtp_config").get("port")
        username = jsonData.get("smtp_config").get("username")
        password = jsonData.get("smtp_config").get("password")

        if app_id and notificationConfig:
            NotificationConfig.objects.filter().update(app_id=app_id, admin_email=emails, host=host, port=port,
                                                       username=username, password=password)
        elif app_id and not notificationConfig:
            notificationConfig_obj = NotificationConfig.objects.create(app_id=app_id, admin_email=emails, host=host,
                                                                       port=port, username=username, password=password)
            notificationConfig_obj.save()
    else:
        print()
        return ""


@receiver(post_save, sender=NotificationConfig)
def notificationConfigPostRequest(sender, **kwargs):
    instance = kwargs.get("instance")
    response = NotificationConfigImpl().postNotificationConfig(requests, instance)


def get_admin_emails(jsonData):
    admin_emails = jsonData.get("admin_emails")
    emails = ''
    for admin_email in admin_emails:
        if emails:
            emails = "," + admin_email
        else:
            emails = admin_email
    return emails


admin.site.register(NotificationConfig, NotificationConfigAdmin)
