from django.contrib import admin

from .functions.DispatcherConfigImpl import DispatcherConfigImpl
from .functions.JsonMapperImpl import JsonMapperImpl
from .functions.MetadataUploadImpl import MetadataUploadAdminImpl
from .functions.NotificationConfigImpl import NotificationConfigImpl
from .models import JsonMapper, DispatcherConfig, NotificationConfig, MetadataUpload, IOLHost
import requests
from django.core.files.base import ContentFile, File
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_init, pre_save
from django.shortcuts import get_object_or_404

import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

admin.site.site_header = "Jembi IOL Admin Platform"
admin.site.index_title = "Welcome to IOL "
admin.site.site_title = "IOL "
MAX_OBJECTS = 1


class IOLHostAdmin(admin.ModelAdmin):
    list_display = ('host', 'port', 'date_created', 'date_changed',)
    search_fields = ('host',)
    list_per_page = 15

    def has_add_permission(self, request):
        count = JsonMapper.objects.all().count()
        if count == 0:
            return True
        return False

admin.site.register(IOLHost, IOLHostAdmin)


class JsonMapperAdmin(admin.ModelAdmin):
    list_display = ('config_url', 'date_created', 'date_changed',)
    search_fields = ('config_url',)
    list_per_page = 15
    fields = ('config_url',)

    def has_add_permission(self, request):
        JsonMapperInit()
        count = JsonMapper.objects.all().count()
        if count == 0:
            return True
        return False

    class Meta:
        model = JsonMapper
    class Media:
        js = ("/static/s.js",)


admin.site.register(JsonMapper, JsonMapperAdmin)


class NotificationConfigAdmin(admin.ModelAdmin):
    list_display = ('app_id', 'admin_email', 'host', 'port', 'username', 'date_created', 'date_changed',)
    search_fields = ('admin_email',)
    list_per_page = 15

    def has_add_permission(self, request):
        NotificationConfigInit()
        count = NotificationConfig.objects.all().count()
        if count == 0:
            return True
        return False


class DispatcherConfigAdmin(admin.ModelAdmin):
    list_display = ('app_id', 'dhis2_host', 'dhis2_port', 'dhis2_username', 'date_created', 'date_changed',)
    search_fields = ('app_id',)
    list_per_page = 15

    def has_add_permission(self, request):
        DispatcherConfigInit()
        count = DispatcherConfig.objects.all().count()
        if count == 0:
            return True
        return False


class MetadataUploadAdmin(admin.ModelAdmin):
    list_display = ('metadata_config_file', 'datetime_created', 'datetime_updated',)
    search_fields = ('metadata_config_file',)
    list_per_page = 15
    fields = ('metadata_config_file',)


    def has_add_permission(self, request):
        MetadataUploadInit()
        count = MetadataUpload.objects.all().count()
        if count == 0:
            return True
        return False


admin.site.register(NotificationConfig, NotificationConfigAdmin)
admin.site.register(DispatcherConfig, DispatcherConfigAdmin)
admin.site.register(MetadataUpload, MetadataUploadAdmin)


@receiver(post_save, sender=JsonMapper)
def jsonMapperPostRequest(sender, **kwargs):
    instance = kwargs.get("instance")
    response = JsonMapperImpl().postJsonMapper(requests, instance)


@receiver(post_save, sender=NotificationConfig)
def notificationConfigPostRequest(sender, **kwargs):
    instance = kwargs.get("instance")
    response = NotificationConfigImpl().postNotificationConfig(requests, instance)


@receiver(post_save, sender=DispatcherConfig)
def dispatcherConfigPostRequest(sender, **kwargs):
    instance = kwargs.get("instance")
    response = DispatcherConfigImpl().postDispatcherConfigImpl(requests, instance)


@receiver(post_save, sender=MetadataUpload)
def dispatcherConfigPostRequest(sender, **kwargs):
    instance = kwargs.get("instance")
    response = MetadataUploadAdminImpl().postMetadataUpload(requests, instance)



def JsonMapperInit():
    jsonData = JsonMapperImpl().getAndRefresh()
    jsonMapper = JsonMapper.objects.filter()
    metadata_config_url = jsonData.get("metadata_config_url")

    if metadata_config_url and jsonMapper:
        JsonMapper.objects.filter().update(config_url=metadata_config_url)
    elif metadata_config_url and not jsonMapper:
        jsonMapper_obj = JsonMapper.objects.create(config_url=metadata_config_url)
        jsonMapper_obj.save()



def DispatcherConfigInit():
    jsonData = DispatcherConfigImpl().getAndRefreshDispatcherConfig()
    dispatcherConfig = DispatcherConfig.objects.filter()
    app_id = jsonData.get("AppID")
    dhis2_host = jsonData.get("DHIS2_IP")
    dhis2_port = jsonData.get("DHIS2_port")
    dhis2_username = jsonData.get("DHIS2_Username")
    dhis2_password = jsonData.get("DHIS2_Password")


    if app_id and dispatcherConfig:
        DispatcherConfig.objects.filter().update(app_id=app_id, dhis2_host=dhis2_host, dhis2_port=dhis2_port, dhis2_username=dhis2_username, dhis2_password=dhis2_password)
    elif app_id and not dispatcherConfig:
        jsonMapper_obj = DispatcherConfig.objects.create(app_id=app_id, dhis2_host=dhis2_host, dhis2_port=dhis2_port, dhis2_username=dhis2_username, dhis2_password=dhis2_password)
        jsonMapper_obj.save()


def NotificationConfigInit():
    jsonData = NotificationConfigImpl().getAndRefreshNotificationConfig()
    notificationConfig = NotificationConfig.objects.filter()
    app_id = jsonData.get("AppID")
    emails = get_admin_emails(jsonData)
    host = jsonData.get("smtp_config").get("host")
    port = jsonData.get("smtp_config").get("port")
    username = jsonData.get("smtp_config").get("username")
    password = jsonData.get("smtp_config").get("password")

    if app_id and notificationConfig:
        NotificationConfig.objects.filter().update(app_id=app_id, admin_email=emails,  host=host, port=port, username=username, password=password)
    elif app_id and not notificationConfig:
        notificationConfig_obj = NotificationConfig.objects.create(app_id=app_id, admin_email=emails, host=host, port=port, username=username, password=password)
        notificationConfig_obj.save()


def MetadataUploadInit():
    jsonData = MetadataUploadAdminImpl().getAndRefreshMetadataUpload()
    metadataUpload = MetadataUpload.objects.filter()
    print(metadataUpload)
    if jsonData and metadataUpload is not None and metadataUpload:
        MetadataUpload.objects.filter().delete()
        MetadataUpload().metadata_config_file.save('meta_data.json', ContentFile(jsonData))
    elif jsonData and metadataUpload is not None and not metadataUpload:
        MetadataUpload.objects.filter().delete()
        MetadataUpload().metadata_config_file.save('meta_data.json', ContentFile(jsonData))

def get_admin_emails(jsonData):
    admin_emails = jsonData.get("admin_emails")
    emails = ''
    for admin_email in admin_emails:
        if emails:
            emails = "," + admin_email
        else:
            emails = admin_email
    return emails



