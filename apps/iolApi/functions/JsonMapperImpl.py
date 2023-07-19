import json
import environ
import requests

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
from apps.iolApi.functions.iol_server_interface import postIolServerData, getUrl


class JsonMapperImpl:
    def postJsonMapper(self, requests, instance):
        try:
            config_url = instance.config_url
            endpoint = env('MAPPER_CONFIG')
            host_name = env('CONTAINER_MAPPER_CONFIG')
            url = getUrl(endpoint, host_name)
            payload = json.dumps({
                "metadata_config_url": config_url
            })
            response = postIolServerData(requests, payload, url)
            print(response.status_code)
            if response.status_code == 200:
                return response
            else:
                return ""
        except Exception as e:
            print(e)
            return ""

    def getAndRefresh(self):
        try:
            endpoint = env('GET_MAPPER_CONFIG')
            host_name = env('CONTAINER_MAPPER_CONFIG')
            url = getUrl(endpoint, host_name)
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                return response.json()
            else:
                return ""
        except Exception as e:
            print(e)
            return ""
