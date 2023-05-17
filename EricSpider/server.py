from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from scrapy.crawler import CrawlerProcess
import subprocess
import linkTolink
from multiprocessing import Process
import subprocess
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
    p1 = Process(target=run_crawler, args=('LaptopCrawler',))
    p1.start()
    p1.join()
    API_ENDPOINT = "https://web-crawler-computer-network-project2.vercel.app/updateCategory" #MongoDB server api
    linkTolink.updateCateToServer(API_ENDPOINT=API_ENDPOINT) #update to Server
    return json.dumps({'result':'UpdateDB success'}), 200

def run_crawler(crawler_name):
    process = subprocess.Popen(['scrapy', 'crawl', crawler_name])
    return_code = process.wait()
   

@app.route('/updateDB', methods =['GET'])
def updateDB():
    print('updating...')
    p1 = Process(target=run_crawler, args=('google',))
    p2 = Process(target=run_crawler, args=('sosanhgia',))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    # API_ENDPOINT = "https://web-crawler-computer-network-project2.vercel.app/updateProduct" #MongoDB server api
    # linkTolink.updateProductToServer(API_ENDPOINT=API_ENDPOINT) #update to Server
    return json.dumps({'result':'UpdateDB success'}), 400

@app.route('/',  methods = ['GET'])
def sayHello():
    data = {"'Eric'": "'m la con ga'"}
    response = jsonify(data)
    response.headers['Content-Type'] = 'application/json'
    return response, 200

if __name__ == '__main__':
    app.run()