
# importing the requests library
import requests
import json
import threading
from queue import Queue
#API_ENDPOINT = "https://mmt-main-dbserver.vercel.app/api/product"

# def updateProductToServer(API_ENDPOINT):
#     with open('DataFile/items1.json', 'r', encoding="utf-8") as f:
#         data = json.load(f)
#     # data = 
#     headers =  {'Content-Type': 'application/json'}
#     # defining the api-endpoint 
#     # # sending post request and saving response as response object
#     try:
#         for item in data:
#             resp = requests.post(url=API_ENDPOINT, headers=headers, json=item)
#             print(resp.json())
#         # print(data)
#     except Exception as e:
#         print("Something wrong")
#         print(e)



def post_item(API_ENDPOINT, headers, queue):
    while not queue.empty():
        item = queue.get()
        try:
            resp = requests.post(url=API_ENDPOINT, headers=headers, json=item)
            print(resp.json())
        except Exception as e:
            print("Something wrong")
            print(e)
        queue.task_done()

def updateProductToServer(API_ENDPOINT):
    with open('DataFile/items1.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
    headers = {'Content-Type': 'application/json'}
    queue = Queue()
    for item in data:
        queue.put(item)
    num_threads = 10
    for i in range(num_threads):
        t = threading.Thread(target=post_item, args=(API_ENDPOINT, headers, queue))
        t.start()
    queue.join()


def post_cate(API_ENDPOINT, headers, queue):
    while not queue.empty():
        item = queue.get()
        try:
            resp = requests.post(url=API_ENDPOINT, headers=headers, json=item)
            print(resp.json())
        except Exception as e:
            print("Something wrong")
            print(e)
        queue.task_done()

def updateCateToServer(API_ENDPOINT):
    with open('DataFile/output.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
    # data = 
    headers =  {'Content-Type': 'application/json'}
    # defining the api-endpoint 
    # # sending post request and saving response as response object
    queue = Queue()
    for item in data:
        queue.put(item)
    num_threads = 10
    for i in range(num_threads):
        t = threading.Thread(target=post_cate, args=(API_ENDPOINT, headers, queue))
        t.start()