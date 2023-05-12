
from flask import Flask, jsonify, json
from flask_cors import CORS, cross_origin
from flask import request
import json
import requests
import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By


# # Declare browser
# driver = webdriver.Chrome('chromedriver.exe')

# # Open URL
# driver.get("https://www.lazada.vn/laptop/?spm=a2o4n.searchlistcategory.cate_1.3.6a97293cqu0EtU")
# # driver.get("https://www.lazada.vn/dien-thoai-di-dong/?spm=a2o4n.searchlistcategory.cate_1.1.25c3b519wDgrnb")
# sleep(random.randint(5,10))

# # ================================ GET link/title
# elems = driver.find_elements(By.CSS_SELECTOR , ".RfADt [href]")
# title = [elem.text for elem in elems]
# links = [elem.get_attribute('href') for elem in elems]

# # ================================ GET price
# elems_price = driver.find_elements(By.CSS_SELECTOR , ".aBrP0")
# len(elems_price)
# price = [elem_price.text for elem_price in elems_price]

# df1 = pd.DataFrame(list(zip(title, price, links)), columns = ['title', 'price','link_item'])
# df1['index_'] = np.arange(1, len(df1) + 1)

# # ================================GET discount

# # elems_discount = driver.find_elements(By.CSS_SELECTOR , ".WNoq3")
# # discount_all = [elem.text for elem in elems_discount]

# elems_discount = driver.find_elements(By.CSS_SELECTOR , ".WNoq3 ._1m41m")
# discount = [elem.text for elem in elems_discount]

# elems_discountPercent = driver.find_elements(By.CSS_SELECTOR , ".WNoq3 .IcOsH")
# discountPercent = [elem.text for elem in elems_discountPercent]

# discount_idx, discount_percent_list = [], []
# for i in range(1, len(title)+1):
#     try:
#         # discount = driver.find_element("xpath", "/html/body/div[3]/div/div[3]/div[1]/div/div[1]/div[2]/div[{}]/div/div/div[2]/div[4]/span[1]/del".format(i))
#         # discount_list.append(discount.text)
#         discount_percent = driver.find_element("xpath", "/html/body/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div[{}]/div/div/div[2]/div[4]/span".format(i))
#         discount_percent_list.append(discount_percent.text)
#         print(i)
#         discount_idx.append(i)
#     except NoSuchElementException:
#         print("No Such Element Exception " + str(i))

# df2 = pd.DataFrame(list(zip(discount_idx , discount_percent_list)), columns = ['discount_idx', 'discount_percent_list'])

# df3 = df1.merge(df2, how='left', left_on='index_', right_on='discount_idx')

# # ================================ GET location/countReviews

# elems_countReviews = driver.find_elements(By.CSS_SELECTOR , "._6uN7R")
# countReviews = [elem.text for elem in elems_countReviews]

# df3['countReviews'] = countReviews
# df3.to_csv('Thanh.csv', index=False)
# results = df3.to_json(orient='records')
# with open('laptop.txt', 'w') as myfile:
#   json.dump(results, myfile)


# # Khởi tạo Flask Server Backend
# app = Flask(_name_)

# # Apply Flask CORS
# CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

# @app.route('/add', methods=['POST', 'GET'] )
# @cross_origin(origin='*')
# def add_process():
#     a = int(request.args.get('sothunhat'))
#     b = int(request.args.get('sothuhai'))
#     kq = a + b
#     return 'Kết quả là: ' + str(kq)

# @app.route('/senddata')
# @cross_origin(origin='*')
# def senddata_process():
#     with open("data.json", encoding="utf-8") as f:
#         products = json.load(f)
    
#     # domain = "https://mmt-db-doan-2.vercel.app/api/product"
#     # req = requests.post(domain,json = products)
#     return jsonify(results)

# if _name_ == '_main_':
#     app.run(host='0.0.0.0', port='6868')

# df = pd.DataFrame(
#     {'name': ["apple", "banana", "cherry"], 'quant': [40, 50, 60]})

# df.to_csv('Test.csv', index=False)

# res = df.to_json(orient='records')

# datastring = json.dumps(res, indent=4)

# print(datastring)

# data_dict = {
#     "domainname": "gochocit.com",
#     "active": True,
#     "numberposts": 360,
#     "category": ["hardware", "software", "network"],
#     "facebookpage": "https://www.facebook.com/gochocit/",
#     "build": {
#         "language": "php",
#         "cms": "wordpress",
#         "database": "mysql"
#     }
# }


#convert dictionary to json string with sort_keys and indent
# data_string = json.dumps(data_dict, sort_keys=True, indent=4)
# print(data_string)
url = "https://ap-southeast-1.aws.data.mongodb-api.com/app/data-sdewu/endpoint/data/v1/action/find"
payload = json.dumps({
    "collection": "Website",
    "database": "Crawler",
    "dataSource": "Cluster",
    "filter": {}
})
headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': 'wrlShBSJ5hi8V8oFWdt9R131hhLJEx0WdJwtTzQaou0TGQD9ieti9U2j9coWGN9t', 
}
response = requests.request("POST", url, headers=headers, data=payload)
data = response.json()
print(response.json()['documents'])
