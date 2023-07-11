from django.db import models
import uuid
from django.db.models.signals import post_init



# Create your models here.

def _upload_metadata_config_file(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return instance.get_metadata_upload_path(filename)


class IOLHost(models.Model):
    host = models.CharField(max_length=255, unique=True)
    port = models.CharField(max_length=255)
    description = models.CharField(max_length=10240, null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)
    date_changed = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        db_table = "iol_host"
        verbose_name = "IOL Server Host"



class JsonMapper(models.Model):

    config_url = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=10240, null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)
    date_changed = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        db_table = "json_mapper"

    def __str__(self):
        return self.config_url



class NotificationConfig(models.Model):

    app_id = models.CharField(max_length=255,unique=True)
    admin_email = models.CharField(max_length=255, null=True, blank=True)
    host = models.CharField(max_length=255, unique=True)
    port = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now=True)
    date_changed = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        db_table = "notification_config"


class DispatcherConfig(models.Model):
    app_id = models.CharField(max_length=255,unique=True)
    dhis2_host = models.CharField(max_length=255, unique=True)
    dhis2_port = models.CharField(max_length=255)
    dhis2_username = models.CharField(max_length=255)
    dhis2_password = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now=True)
    date_changed = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        db_table = "dispatcher_config"


class MetadataUpload(models.Model):
    metadata_config_file = models.FileField(upload_to=_upload_metadata_config_file, max_length=5000, null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        db_table = "metadata_upload"

    def get_metadata_upload_path(self, filename):
        return filename

