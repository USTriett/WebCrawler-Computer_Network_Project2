
# importing the requests library
import requests
import json

#API_ENDPOINT = "https://mmt-main-dbserver.vercel.app/api/product"

def updateProductToServer(API_ENDPOINT):
    with open('DataFile/items.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
    # data = 
    headers =  {'Content-Type': 'application/json'}
    # defining the api-endpoint 
    # # sending post request and saving response as response object
    try:
        for item in data:
            resp = requests.post(url=API_ENDPOINT, headers=headers, json=item)
            print(resp.json())
        # print(data)
    except Exception as e:
        print("Something wrong")
        print(e)

def updateCateToServer(API_ENDPOINT):
    with open('DataFile/category1.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
    # data = 
    headers =  {'Content-Type': 'application/json'}
    # defining the api-endpoint 
    # # sending post request and saving response as response object
    try:
        for item in data:
            resp = requests.post(url=API_ENDPOINT, headers=headers, json=item)
            print(resp.json())
        # print(data)
    except Exception as e:
        print("Something wrong")
        print(e)