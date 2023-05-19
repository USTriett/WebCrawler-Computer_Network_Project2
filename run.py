import requests
import json
import mongodb.data_process as data_process
headers = {
  'Content-Type': 'application/json',
}

response = requests.post(url= 'http://127.0.0.1:5000/getProducts', headers=headers)
with open('data.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(response.json(), ensure_ascii=False, indent=4))
