import json
import environ
import requests


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
from apps.iolApi.functions.iol_server_interface import getUrl, postIolServerData


class JsonMapperImpl:
    def postJsonMapper(self, requests, instance):
        config_url = instance.config_url
        endpoint = env('MAPPER_CONFIG')
        url = getUrl(endpoint)
        payload = json.dumps({
            "metadata_config_url": config_url
        })
        response = postIolServerData(requests, payload, url)
        print(response.status_code)
        if response.status_code == 200:
            return response
        else:
            return ""

    def getAndRefresh(self):
        endpoint = env('GET_MAPPER_CONFIG')
        url = getUrl(endpoint)
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return ""
