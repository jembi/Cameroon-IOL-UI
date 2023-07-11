from django.contrib import admin

from .functions.DispatcherConfigImpl import DispatcherConfigImpl
from .functions.JsonMapperImpl import JsonMapperImpl
from .functions.MetadataUploadImpl import MetadataUploadAdminImpl
from .functions.NotificationConfigImpl import NotificationConfigImpl
from .models import JsonMapper, DispatcherConfig, NotificationConfig, MetadataUpload, IOLHost
import requests
import json
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_init

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
        count = NotificationConfig.objects.all().count()
        if count == 0:
            return True
        return False


class DispatcherConfigAdmin(admin.ModelAdmin):
    list_display = ('app_id', 'dhis2_host', 'dhis2_port', 'dhis2_username', 'date_created', 'date_changed',)
    search_fields = ('app_id',)
    list_per_page = 15

    def has_add_permission(self, request):
        return False


class MetadataUploadAdmin(admin.ModelAdmin):
    list_display = ('metadata_config_file', 'datetime_created', 'datetime_updated',)
    search_fields = ('metadata_config_file',)
    list_per_page = 15
    fields = ('metadata_config_file',)


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


@receiver(pre_init, sender=JsonMapper)
def JsonMapperInit(sender, **kwargs):
    jsonData = JsonMapperImpl().getAndRefresh()
    if jsonData.get("metadata_config_url"):
        JsonMapper.objects.filter().update(config_url=jsonData.get("metadata_config_url"))
