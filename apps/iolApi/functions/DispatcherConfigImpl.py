import json
import environ
import requests

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
from apps.iolApi.functions.iol_server_interface import postIolServerData, getUrl


class DispatcherConfigImpl:
    def postDispatcherConfigImpl(self, requests, instance):
        endpoint = env('DISPATCH_CONFIG')
        url = getUrl(endpoint)
        payload = json.dumps({
            "AppID": instance.app_id,
            "DHIS2_IP": instance.dhis2_host,
            "DHIS2_port": instance.dhis2_port,
            "DHIS2_Username": instance.dhis2_username,
            "DHIS2_Password": instance.dhis2_password
        })
        response = postIolServerData(requests, payload, url)
        if response.status_code == 200:
            return response
        else:
            return ""

    def getAndRefreshDispatcherConfig(self):
        endpoint = env('GET_DISPATCH_CONFIG')
        url = getUrl(endpoint)
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return ""
