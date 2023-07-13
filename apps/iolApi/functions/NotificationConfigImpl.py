import json
import environ
import requests

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
from apps.iolApi.functions.iol_server_interface import postIolServerData, getUrl


class NotificationConfigImpl:
    def postNotificationConfig(self, requests, instance):
        endpoint = env('NOTIFICATION_CONFIG')
        host_name = env('CONTAINER_NOTIFICATION_CONFIG')
        url = getUrl(endpoint, host_name)
        payload = json.dumps({
            "AppID": instance.app_id,
            "admin_emails": [
                instance.admin_email
            ],
            "smtp_config": {
                "host": instance.host,
                "port": instance.port,
                "username": instance.username,
                "password": instance.password
            }
        })
        response = postIolServerData(requests, payload, url)
        if response.status_code == 200:
            return response
        else:
            return ""
    def getAndRefreshNotificationConfig(self):
        endpoint = env('GET_NOTIFICATION_CONFIG')
        host_name = env('CONTAINER_NOTIFICATION_CONFIG')
        url = getUrl(endpoint, host_name)
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return ""
