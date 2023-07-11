import json
import environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
from apps.iolApi.functions.iol_server_interface import getUrl, postIolServerData


class NotificationConfigImpl:
    def postNotificationConfig(self, requests, instance):
        endpoint = env('NOTIFICATION_CONFIG')

        url = getUrl(endpoint)
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

        print(payload)
        response = postIolServerData(requests, payload, url)
        print(response.status_code)
        if response.status_code == 200:
            return response
        else:
            return ""
