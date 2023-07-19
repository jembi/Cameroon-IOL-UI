import requests
from django.contrib import admin
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..functions.MetadataUploadImpl import MetadataUploadAdminImpl
from ..models import MetadataUpload


class MetadataUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'metadata_config_file', 'datetime_created', 'datetime_updated',)
    search_fields = ('metadata_config_file',)
    list_per_page = 15
    fields = ('metadata_config_file',)

    def has_add_permission(self, request):
        count = MetadataUpload.objects.all().count()
        if count == 0:
            return True
        return False

    def get_queryset(self, request):
        metadataUploadInit()
        query = super(MetadataUploadAdmin, self).get_queryset(request)
        return query


def metadataUploadInit():
    jsonData = MetadataUploadAdminImpl().getAndRefreshMetadataUpload()
    if jsonData:
        metadataUpload = MetadataUpload.objects.filter()
        print(metadataUpload)
        # MetadataUpload.objects.filter().update(metadata_config_file=ContentFile(jsonData))
        if jsonData and metadataUpload is not None and not metadataUpload:
            MetadataUpload().metadata_config_file.save('meta_data.json', ContentFile(jsonData))
    else:
        print()
        return ""


@receiver(post_save, sender=MetadataUpload)
def metadataUploadPostRequest(sender, **kwargs):
    instance = kwargs.get("instance")
    response = MetadataUploadAdminImpl().postMetadataUpload(requests, instance)


admin.site.register(MetadataUpload, MetadataUploadAdmin)
