import environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

def postIolServerData(requests, payload, url):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response

def getUrl( endpoint):
    host = 'localhost'
    port = '5001'
    url = "http://" + host + ":" + port + "/" + endpoint
    print("url -"+url)
    return url
