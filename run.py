import requests
import json
import mongodb.data_process as data_process
headers = {
  'Content-Type': 'application/json',
    'Name-Cate':'RAM%20Laptop%20Samsung%208GB%20DDR4%20Bus%203200%20-%20H%C3%A0ng%20Nh%E1%BA%ADp%20Kh%E1%BA%A9u'
}

response = requests.post(url= 'http://127.0.0.1:5000/getData', headers=headers)
with open('data.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(response.json(), ensure_ascii=False, indent=4))
