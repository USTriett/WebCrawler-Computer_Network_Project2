from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import data_process
import get_tunnels
import requests
import time
import threading
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
@app.route('/',  methods = ['GET'])
def sayHello():
    data = {"Chao": "User"}
    
    response = jsonify(data)
    response.headers['Content-Type'] = 'application/json'
    return response, 200

@app.route('/updateCategory', methods = ['POST'])
def updateCate():
    #get header request
    try:
        Content_Type =  request.headers.get('Content-Type')
        if(Content_Type != "application/json"):
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        data = request.get_json()
        if data is None:
            print('Data is invalid')
            return jsonify({'error': 'Invalid data'}), 400
        if(data_process.uploadCate(data) == True):
            return jsonify({'done': data}), 200
        return jsonify({'error': 'Invalid data'}), 400
        
    except Exception as e:
        print(e)
    return jsonify({'error': 'Some Exception throws'}), 400


@app.route('/updateProduct', methods = ['POST'])
def updateProduct():
    #get header request
    try:
        Content_Type =  request.headers.get('Content-Type')
        if(Content_Type != "application/json"):
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        data = request.get_json()
        if data is None:
            print('Data is invalid')
            return jsonify({'error': 'Invalid data'}), 400
        elif (data_process.uploadProduct(data) == True):
            return jsonify({'done': data}), 200
        return jsonify({'error': 'Invalid data'}), 400
        
    except Exception as e:
        print(e)
    return jsonify({'error': 'Some Exception throws'}), 400

@app.route('/updateWebsite', methods = ['POST'])
def updateWeb():
    #get header request
    try:
        Content_Type =  request.headers.get('Content-Type')
        if(Content_Type != "application/json"):
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        data = request.get_json()
        if data is None:
            print('Data is invalid')
            return jsonify({'error': 'Invalid data'}), 400
        if(data_process.uploadWebsite(data) == True):
            return jsonify({'done': data}), 200
        return jsonify({'error': 'Invalid data'}), 400
        
    except Exception as e:
        print(e)
    return jsonify({'error': 'Some Exception throws'}), 400

@app.route('/getData', methods = ['POST'])
def getData():
    #get header request
    try:
        Content_Type =  request.headers.get('Content-Type')
        if(Content_Type != "application/json"):
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        for data in data_process.get_all_json():
            response = jsonify(data)
            response.headers['Content-Type'] = 'application/json'
            yield response, 200
        
    except Exception as e:
        print(e)
    return jsonify({'error': 'Some Exception throws'}), 400

def update_db(t):
    while True:
        time.sleep(t)
        try:
            public_url = get_tunnels.get_public_url()
            requests.get(url=public_url + '/updateDB') #crawlai
        except Exception as e:
            print(e)
       

if __name__ == '__main__':
    t = threading.Thread(target=update_db, args=(1200000000,))
    t.start()
    app.run()
        