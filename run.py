import requests
import json
headers = {
  'Content-Type': 'application/json',

}
data = {
    "Url": "https://phongvu.vn/hp-probook-450-g9-6m0z9pa--s220800857",
    "Name": "Máy tính xách tay/ Laptop HP Probook 450 G9 (6M0Z9PA) (i7-1255U) (Bạc)",
    "Price": 21500000,
    "OriginalPrice": 21500000,
    "NameCategory": "Laptop HP Probook 450 G9",
    "Imgs": [
    ]
}
res = requests.post(url='http://conchoheo4.pythonanywhere.com/updateProduct', headers=headers, json=data)
print(res.text)
