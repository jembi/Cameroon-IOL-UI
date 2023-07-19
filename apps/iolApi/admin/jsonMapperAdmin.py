import requests
from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..functions.JsonMapperImpl import JsonMapperImpl
from ..models import JsonMapper


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

    def get_queryset(self, request):
        jsonMapperInit()
        # self.message_user(request, "The message", level=messages.ERROR)

        query = super(JsonMapperAdmin, self).get_queryset(request)
        return query

    class Meta:
        model = JsonMapper


def jsonMapperInit():
    jsonData = JsonMapperImpl().getAndRefresh()
    if jsonData:
        jsonMapper = JsonMapper.objects.filter()
        metadata_config_url = jsonData.get("metadata_config_url")

        if metadata_config_url and jsonMapper:
            JsonMapper.objects.filter().update(config_url=metadata_config_url)
        elif metadata_config_url and not jsonMapper:
            jsonMapper_obj = JsonMapper.objects.create(config_url=metadata_config_url)
            jsonMapper_obj.save()
    else:
        print()
        return ""


admin.site.register(JsonMapper, JsonMapperAdmin)


@receiver(post_save, sender=JsonMapper)
def jsonMapperPostRequest(sender, **kwargs):
    instance = kwargs.get("instance")
    response = JsonMapperImpl().postJsonMapper(requests, instance)
