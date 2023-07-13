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

def getUrl(endpoint, host):
    header = env('HEADER')
    port = env('IOL_PORT')
    url = header+"://" + host + ":" + port + "/" + endpoint
    print("url -"+url)
    return url


# def getUrl(endpoint):
#    # iOLHost = get_object_or_404(IOLHost)
#     host = iOLHost.host
#     port = iOLHost.port
#     url = "http://" + host + ":" + port + "/" + endpoint
#     print("url -"+url)
#     return url
