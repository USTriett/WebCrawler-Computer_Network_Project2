import requests

def get_public_url(api_key = '2PeWrXxMRWtRv0GChNfXOHSqIIK_5iqox1sGyRHVsRJibHMi3'):
    headers = {
    "Authorization": f"Bearer {api_key}",
    "Ngrok-Version": "2"
    }
    response = requests.get("https://api.ngrok.com/tunnels", headers=headers)
    tunnel_info = response.json()
    return tunnel_info['tunnels'][0]['public_url']

# requests.get(url=get_public_url() + '/updateDB')