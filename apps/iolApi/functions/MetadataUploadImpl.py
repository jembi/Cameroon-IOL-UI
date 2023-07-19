import json
import environ
import requests

from iol_admin.settings.common import MEDIA_ROOT

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
from apps.iolApi.functions.iol_server_interface import postIolServerData, getUrl


class MetadataUploadAdminImpl:
    def postMetadataUpload(self, requests, instance):
        try:
            file = instance.metadata_config_file
            json_data = open(MEDIA_ROOT+"/"+str(file))
            json_metadata = json.load(json_data)  # deserialises it
            payload = json.dumps(json_metadata)
            endpoint = env('META_DATA')
            host_name = env('CONTAINER_META_DATA')
            url = getUrl(endpoint, host_name)
            response = postIolServerData(requests, payload, url)
            print(response.status_code)
            if response.status_code == 200:
                return response
            else:
                return ""
        except Exception as e:
            print(e)
            return ""


    def getAndRefreshMetadataUpload(self):
        try:
            endpoint = env('GET_META_DATA')
            host_name = env('CONTAINER_META_DATA')
            url = getUrl(endpoint, host_name)
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                return response.text
            else:
                return ""
        except Exception as e:
            print(e)
            return ""
