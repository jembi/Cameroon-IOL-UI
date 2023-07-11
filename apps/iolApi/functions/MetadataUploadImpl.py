import json
import environ

from iol_admin.settings.common import MEDIA_ROOT

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
from apps.iolApi.functions.iol_server_interface import getUrl, postIolServerData


class MetadataUploadAdminImpl:
    def postMetadataUpload(self, requests, instance):
        file = instance.metadata_config_file
        json_data = open(MEDIA_ROOT+"/"+str(file))
        json_metadata = json.load(json_data)  # deserialises it
        payload = json.dumps(json_metadata)
        endpoint = env('META_DATA')
        url = getUrl(endpoint)
        response = postIolServerData(requests, payload, url)
        print(response.status_code)
        if response.status_code == 200:
            return response
        else:
            return ""
