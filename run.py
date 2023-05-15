import requests
import json
import mongodb.data_process as data_process
headers = {
  'Content-Type': 'application/json',

}

response = requests.get(url= 'http://127.0.0.1:5000/updateCategory')
print(response.text)

