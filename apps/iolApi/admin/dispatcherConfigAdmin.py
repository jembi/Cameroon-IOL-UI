

from django.contrib import admin

from ..functions.DispatcherConfigImpl import DispatcherConfigImpl
from ..models import DispatcherConfig
import requests
from django.dispatch import receiver
from django.db.models.signals import post_save


class DispatcherConfigAdmin(admin.ModelAdmin):
    list_display = ('app_id', 'dhis2_host', 'dhis2_port', 'dhis2_username', 'date_created', 'date_changed',)
    search_fields = ('app_id',)
    list_per_page = 15

    def has_add_permission(self, request):
        count = DispatcherConfig.objects.all().count()
        if count == 0:
            return True
        return False

    def get_queryset(self, request):
        dispatcherConfigInit()
        query = super(DispatcherConfigAdmin, self).get_queryset(request)
        return query


def dispatcherConfigInit():
    jsonData = DispatcherConfigImpl().getAndRefreshDispatcherConfig()
    if jsonData:
        dispatcherConfig = DispatcherConfig.objects.filter()
        app_id = jsonData.get("AppID")
        dhis2_host = jsonData.get("DHIS2_IP")
        dhis2_port = jsonData.get("DHIS2_port")
        dhis2_username = jsonData.get("DHIS2_Username")
        dhis2_password = jsonData.get("DHIS2_Password")

        if app_id and dispatcherConfig:
            DispatcherConfig.objects.filter().update(app_id=app_id, dhis2_host=dhis2_host, dhis2_port=dhis2_port,
                                                     dhis2_username=dhis2_username, dhis2_password=dhis2_password)
        elif app_id and not dispatcherConfig:
            jsonMapper_obj = DispatcherConfig.objects.create(app_id=app_id, dhis2_host=dhis2_host,
                                                             dhis2_port=dhis2_port, dhis2_username=dhis2_username,
                                                             dhis2_password=dhis2_password)
            jsonMapper_obj.save()
    else:
        print()
        return ""

    @receiver(post_save, sender=DispatcherConfig)
    def dispatcherConfigPostRequest(sender, **kwargs):
        instance = kwargs.get("instance")
        response = DispatcherConfigImpl().postDispatcherConfigImpl(requests, instance)


admin.site.register(DispatcherConfig, DispatcherConfigAdmin)

