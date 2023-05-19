import requests
import json
import mongodb.data_process as data_process
from urllib.parse import quote
text = "Laptop"
headers = {
  'Content-Type': 'application/json',
  'Name-Cate': quote(text)
}


response = requests.post(url= 'http://127.0.0.1:8001/getData', headers=headers)
print(response.json())
# with open('data.json', 'w', encoding='utf-8') as f:
#     f.write(json.dumps(response.json(), ensure_ascii=False, indent=4))
