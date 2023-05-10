from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from scrapy.crawler import CrawlerProcess
import subprocess
import linkTolink

app = Flask(__name__)
CORS(app)


# @app.route('/testGet', methods = ['Get', 'POST'])
# def testGet():
#     if request.method == 'POST':
#         # Xử lý đăng nhập ở đây
#         return json.dumps({'lệnh':'Đăng nhập thành công'})
#     else:
#         return 'hello'
    
#gui yeu cau cap nhat lai co so du lieu
#Muon chay crawl local crawl 
#proxy
@app.route('/updateCategory', methods = ['GET'])
def updateCate():
    process = subprocess.Popen(['scrapy', 'crawl', 'PhongVuCrawler'])
    return_code = process.wait()
    API_ENDPOINT = "https://mmt-main-dbserver.vercel.app/api/category" #MongoDB server api
    linkTolink.updateProductToServer(API_ENDPOINT=API_ENDPOINT) #update to Server
    return json.dumps({'result':'UpdateDB success'}), 200

@app.route('/updateDB', methods =['GET'])
def updateDB():
    process = subprocess.Popen(['scrapy', 'crawl', 'google'])
    return_code = process.wait()
    process = subprocess.Popen(['scrapy', 'crawl', 'sosanhgia'])
    return_code = process.wait()

    API_ENDPOINT = "https://mmt-main-dbserver.vercel.app/api/product" #MongoDB server api
    linkTolink.updateProductToServer(API_ENDPOINT=API_ENDPOINT) #update to Server
    return json.dumps({'result':'UpdateDB success'}), 200

@app.route('/',  methods = ['GET'])
def sayHello():
    data = {"'Eric'": "'m la con ga'"}
    response = jsonify(data)
    response.headers['Content-Type'] = 'application/json'
    return response, 200

if __name__ == '__main__':
    app.run(debug=True)