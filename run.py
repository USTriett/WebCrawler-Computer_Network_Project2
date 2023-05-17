import requests
import json
import mongodb.data_process as data_process
headers = {
  'Content-Type': 'application/json',

}

response = requests.post(url= 'https://web-crawler-computer-network-project2.vercel.app/getData', headers=headers)
with open('data.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(response.json(), ensure_ascii=False, indent=4))
