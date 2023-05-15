import pymongo
import re




client = pymongo.MongoClient("mongodb+srv://USTriet:1234@cluster.sq4uzoz.mongodb.net/?retryWrites=true&w=majority")
db = client["Crawler"]
Product = db["Product"]
Category = db["Category"]
Website = db["Website"]

url = "https://ap-southeast-1.aws.data.mongodb-api.com/app/data-sdewu/endpoint/data/v1/action/"

headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': 'wrlShBSJ5hi8V8oFWdt9R131hhLJEx0WdJwtTzQaou0TGQD9ieti9U2j9coWGN9t', 
}

def parse_domain(url):
    # options = Options()
    # options.headless = True
    # driver = webdriver.Chrome(options=options)
    # # Go to first URL and click on Download menu
    # driver.get(url=url)
    # # print(1)
    # Url = driver.current_url
    # options = Options()
    # options.headless = True

    # driver = webdriver.Chrome(options=options)

    # # Go to first URL and click on Download menu
    # driver.get(url=url)

    # driver.implicitly_wait(3)
    domain = re.findall('//([a-zA-Z.]+)/', url)
    if len(domain) == 0:
        return None
    return domain[0]

def uploadWebsite(domain, icon = ''):
    default_icon = "https://websosanh.vn/images/no-logo.jpg"
    if (icon == ''):
        icon = default_icon

    web = {
        'Domain': domain,
        'Icon': icon
    }

    #Find domain
    post = Website.find_one(filter={'Domain': domain})
    # Insert documents into collection
    
    if post is None: #new website
        Website.insert_one(document=web)
        print(web['Domain'])
        return True
    elif post.get('Icon') == '': #existed web and icon is empty add default icon
        Website.replace_one(filter={'Domain': domain}, replacement= web)
        print(web['Domain'])
        return True
    
    return False

def uploadProduct(data):
    print("Product:" + str(data))
    # print(data.get('Url'))
    try: 
        Url = data.get('Url')
        domain = parse_domain(Url)
        upPro = {
            "Url": Url,
            "Name": data.get('Name'),
            "Price": data.get('Price'),
            "OriginalPrice": data.get('OriginalPrice'),
            "Imgs": data.get('Imgs'),
            "NameCategory": data.get('NameCategory'),
            "WebDomain": domain
        }
        
        print('Finding Cate...')
        post = Category.find_one(filter={'Name': data.get('NameCategory')})

        if post is None: #khong co cate phu hop
            print('Cannot find Category of Product: upload failed')
            return {'mesage': 'Cannot find Category of Product: upload failed'}    
        else:
            p = Product.find_one(filter={'Name': data.get('Name'), 'Url': data.get('Url')})
            if p is None: # new Product
                print("Adding new product...")
                id = Product.insert_one(document=upPro)
                print('Upload id: ' + str(id))
            else: #updata Price
                if int(p.get('Price')) != data.get('Price'):
                    print("Updating Price of Product...")
                    id = Product.replace_one(filter={'Name': data.get('Name'), 'Url': data.get('Url')}, replacement=upPro)
                    print('Update status: ' + str(id))
            if int(post['Price']) > upPro.get('Price'): #update min Price of Category
                post['Price'] = upPro.get('Price')
                print('Category found:' + str(post))
                Category.replace_one(filter={'Name': data.get('NameCategory')}, replacement=post)
        
        uploadWebsite(data.get('Url'))
        print(upPro)    
        return {'message': 'success'}
    except Exception as e:
        print("Exception throws")
        print(e)
        return {'Exception': str(e)}

# imgs = ["https://cdn.ankhang.vn/media/product/250_22214_laptop_dell_inspiron_3520_n3520_n5i5122w1_1.jpg"]
def uploadCate(data):
    try:
        post = Category.find_one(filter={'Name': data.get('Name')})
        
        if post is None:# new category
            print('Load new Category...')
            id = Category.insert_one(document=data)
            print('Loading: ' + str(id))
            return True
        else:
            print('Category is existed')
            return False
    except Exception as e:
        print(e)
        return False


def get_all_json():
    try:
        cate = Category.find(filter={})

        # product = db['Product']
        # cate = db['Category']
        # web = db['Website']
        # result = []
        for item in cate:
            # url = item['URL']
            name_cate = item.get('Name')
            CatePrice = item.get('Price')
            CateImgs = item.get('Imgs')
            Desc = item.get('Desc')
            print(name_cate)
            p_arr = []
            product = Product.find(filter={'NameCategory': name_cate})
            
            # print(len(product))
            for p in product:
                web = Website.find_one(filter={'Domain': p.get('WebDomain')})
                if web is not None:
                    p['WebIcon'] = web.get('Icon')
                else:
                    p['WebIcon'] = "https://websosanh.vn/images/no-logo.jpg"
                p_arr.append(p)
            # print(p_arr)
            record = {
                'NameCategory': name_cate, #ten goc san pham 
                'CatePrice' : CatePrice, #gia thap nhat
                'CateImgs' : CateImgs,
                'Desc' : Desc,
                'Products': p_arr,
            }
            # result.append(record)
            # print(record['Products'])
            yield record

    except Exception as e:
        print(e)

# def remove_trailing_comma(file_path):
#         with open(file_path, 'r', encoding='utf-8') as f:
#             content = f.read().strip()
#             content = content[:-3] + '\n]'
#         with open(file_path, 'w', encoding='utf-8') as f:
#             f.write(content)
# count = 0
# with open("data.json", 'w', encoding='utf-8') as f:
#     f.write('[\n')
#     for i in get_all_json():
#         if(count == 2):
#             break
#         count += 1
#         f.write(json.dumps(i, indent=4, ensure_ascii=False) + ',\n')
#     f.write(']')
# remove_trailing_comma('data.json')


# count = 0
# for item in get_all_json():
#     if(count == 1):
#         break
#     count += 1
#     print(uploadProduct(item))


# headers = {
#   'Content-Type': 'application/json',
#   'Access-Control-Request-Headers': '*',
#   'api-key': 'wrlShBSJ5hi8V8oFWdt9R131hhLJEx0WdJwtTzQaou0TGQD9ieti9U2j9coWGN9t', 
# }

# payload = json.dumps({
# "collection": "Category",
# "database": "Crawler",
# "dataSource": "Cluster",
# "documents": data
# })
# response = requests.request("POST", url + 'insertMany', headers=headers, data=payload)



# p_arr = []
# for p in product:
#     p_arr.append(p_arr)

# record = {

#     'Products': p_arr,
# }

# print(record['Products'][0])

