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


    
#gui yeu cau cap nhat lai co so du lieu
#Muon chay crawl local crawl 
#proxy

url ='https://ap-southeast-1.aws.data.mongodb-api.com/app/data-sdewu/endpoint/data/v1/action/'
headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': 'wrlShBSJ5hi8V8oFWdt9R131hhLJEx0WdJwtTzQaou0TGQD9ieti9U2j9coWGN9t'
}

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
        return jsonify({'error': 'Some Exception throws', 'e': str(e)}), 400


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
           return jsonify({'error': 'Invalid data 1'}), 400
       
        return jsonify(data_process.uploadProduct(data)), 200
    
    except Exception as e:
        print(e)
        return jsonify({'error': 'Some Exception throws', 'e': str(e)}), 400


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
            return jsonify({'error': 'Invalid data 1'}), 400
        if(data_process.uploadWebsite(data) == True):
            return jsonify({'done': data}), 200
        return jsonify({'error': 'Invalid data 2'}), 400
        
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
        data_list=[]
        for data in data_process.get_all_json():
            data_list.append(data)
        response = jsonify(data_list)
        response.headers['Content-Type'] = 'application/json'
        return response, 200
    
    except Exception as e:
        print(e)
        return jsonify({'error': 'Some Exception throws', 'e': str(e)}), 400

def update_db(t1, t2):
    while True:
        # print('update1')
        time.sleep(t1)
        try:
            while(True):
                public_url = get_tunnels.get_public_url()
                res = requests.get(url=public_url + '/updateDB') #crawlai
                if res.status_code == 200:
                    break;
            time.sleep(t2)
        except Exception as e:
            print(e)
       

if __name__ == '__main__':
    t = threading.Thread(target=update_db, args=(20, 12000000))
    t.start()
    app.run()
        