from flask import Flask, request, jsonify, make_response,  render_template
from flask_cors import CORS
import json
import data_process
import get_tunnels
import requests
import time
import copy
import threading
from urllib.parse import unquote
import os
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
        # if(Content_Type != "application/json"):
        #     return jsonify({'error': 'Content-Type must be application/json'}), 400
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
        Name_Cate = request.headers.get('Name-Cate')
        data_list=[]
        if Name_Cate is None:
            for data in data_process.get_all_json():
                # print(len(data.get('Products')))
                data_list.append(copy.deepcopy(data))
        else:
            # print('Get one:' + Name_Cate)
            data_list.append(copy.deepcopy(data_process.get_Cate_json(Name_Cate)))
            
        # print(data_list[0].get('Products'))
        response = make_response(json.dumps(data_list, ensure_ascii=False, indent=4))
        response.headers['Content-Type'] = 'application/json'
        return response, 200
    
    except Exception as e:
        print(e)
        return jsonify({'error': 'Some Exception throws', 'e': str(e)}), 400


# renderCate(Name) {
#     try {
        

@app.route('/process_data', methods=['POST'])
def process_data():
    # Lấy giá trị của tham số name_cate từ form
    name_cate = request.form.get('name_cate')
    print(name_cate)
    # Lấy giá trị của tham số cate_price từ form
    cate_price = request.form.get('cate_price')
    print(cate_price)
    # Lấy giá trị của tham số desc từ form và giải mã chuỗi JSON
    desc_json = request.form.get('desc')

    desc = json.loads(unquote(desc_json))
    
    # Lấy giá trị của tham số img_len từ form
    img_len = request.form.get('img_len')
    
    # Lấy giá trị của tham số num_prods từ form
    num_prods = request.form.get('num_prods')
    
    # Lấy giá trị của các trường input vớitên `img_link_i` từ form
    img_links = []
    for i in range(int(img_len)):
        img_link = request.form.get(f'img_link_{i}')
        img_links.append(img_link)
    
    # Lấy giá trị của các trường input với tên `product_i_name`, `product_i_url`, `product_i_price`,
    # `product_i_original_price`, `product_i_img`, `product_i_web_icon` từ form
    products = []
    for i in range(int(num_prods)):
        product = {}
        product['Name'] = request.form.get(f'product_{i}_name')
        product['Url'] = request.form.get(f'product_{i}_url')
        product['Price'] = request.form.get(f'product_{i}_price')
        product['OriginalPrice'] = request.form.get(f'product_{i}_original_price')
        product['Imgs'] = request.form.get(f'product_{i}_img')
        product['WebIcon'] = request.form.get(f'product_{i}_web_icon')
        products.append(product)
    
        # Xử lý dữ liệu ở đây
        template_path = os.path.join(os.path.dirname(__file__), 'data.html')
        return render_template(template_path, name_cate=name_cate, cate_price=cate_price, desc=desc, img_links=img_links, products=products)
@app.route('/getProducts', methods = ['POST'])
def getProducts():
    #get header request
    try:
        Content_Type =  request.headers.get('Content-Type')
        if(Content_Type != "application/json"):
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        data_list=[]
        
        for data in data_process.get_products():
            # print(len(data.get('Products')))
            data_list.append(copy.deepcopy(data))
            
        # print(data_list[0].get('Products'))
        response = make_response(json.dumps(data_list, ensure_ascii=False, indent=4))
        response.headers['Content-Type'] = 'application/json'
        return response, 200
    
    except Exception as e:
        print(e)
        return jsonify({'error': 'Some Exception throws', 'e': str(e)}), 400



def update_db(t1, t2):
    while True:
        try:
            while(True):
                # print('update1')
                time.sleep(t1)

                public_url = get_tunnels.get_public_url()
                res = requests.get(url=public_url + '/updateDB') #crawlai
                if res.status_code == 200:
                    break
            time.sleep(t2)
        except Exception as e:
            print(e)
       

if __name__ == '__main__':
    t = threading.Thread(target=update_db, args=(20, 12000000))
    t.start()
    app.run(port=8001)
        