from flask import Flask, request
from flask_cors import CORS
import json
from EricSpider.spiders.lazada import LazadaSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import subprocess
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return 'Trang chủ'

@app.route('/testGet', methods = ['Get', 'POST'])
def testGet():
    if request.method == 'POST':
        # Xử lý đăng nhập ở đây
        return json.dumps({'lệnh':'Đăng nhập thành công'})
    else:
        return 'hello'
    
#gui yeu cau cap nhat lai co so du lieu
@app.route('/updateDB', methods =['GET'])
def updateDB():
    process = subprocess.Popen(['scrapy', 'crawl', 'lazada'])
    return_code = process.wait()
    return json.dumps({'result':'UpdateDB success'})

# @app.route('/stop')
# def stop():
#     process.stop()
#     return 'Spider stopped'

if __name__ == '__main__':
    app.run(port=8000)