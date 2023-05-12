from selenium import webdriver

import re
from selenium.webdriver.chrome.options import Options
import json
import requests


url = "https://ap-southeast-1.aws.data.mongodb-api.com/app/data-sdewu/endpoint/data/v1/action/"

headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': 'wrlShBSJ5hi8V8oFWdt9R131hhLJEx0WdJwtTzQaou0TGQD9ieti9U2j9coWGN9t', 
}

def parse_domain(url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    # Go to first URL and click on Download menu
    driver.get(url=url)
    # print(1)
    Url = driver.current_url
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

    # Insert documents into collection
    payload = json.dumps({
        "collection": "Website",
        "database": "Crawler",
        "dataSource": "Cluster",
        "filter":{'Domain': domain}
        # "options": {"ordered": False}
    })
    response = requests.request("POST", url + 'findOne', headers=headers, data=payload)
    post = response.json().get('document')
    if post is None:
        payload = json.dumps({
            "collection": "Website",
            "database": "Crawler",
            "dataSource": "Cluster",
            "document": web
            # "options": {"ordered": False}
        })
        response = requests.request("POST", url + 'insertOne', headers=headers, data=payload)
        print(web['Domain'])
        return True
    elif post.get('Icon') == '':
        payload = json.dumps({
            "collection": "Website",
            "database": "Crawler",
            "dataSource": "Cluster",
            "filter":{'Domain': domain},
            "document": web
            # "options": {"ordered": False}
        })
        response = requests.request("POST", url + 'replaceOne', headers=headers, data=payload)
        print(web['Domain'])
        return True
    
    return False

def uploadProduct(data):
    print(data)
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
    #     "Url": "https://www.sosanhgia.com/r/redirect.php?pm_id=120529783",
    # "Name": "Ổ cứng SSD Lexar NQ100 2.5 SATA (6Gb/s) - Hàng Chính Hãng - 240GB",
    # "Price": 469000,
    # "OriginalPrice": 469000,
    # "NameCategory": "Ổ cứng SSD Lexar NQ100 2.5” SATA (6Gb/s) - Hàng Chính Hãng",
    # "Imgs": [
    #     "https://img.sosanhgia.com/images/200x200/cb0af44f1f0e433aab9927ba3eead1ad/o-cung-ssd-lexar-nq100-25-sata-(6gb/s)-hang-chinh-hang-240gb.jpeg"
    # ]
        
        print('Finding Cate...')
        payload = json.dumps({
            "collection": "Category",
            "database": "Crawler",
            "dataSource": "Cluster",
            "filter":{'Name': data.get('NameCategory')},
            # "options": {"ordered": False}
        })
        response = requests.request("POST", url + 'findOne', headers=headers, data=payload)
        post = response.json().get('document')
        if post is None: #khong co cate phu hop
            print('Cannot find Category of Product: upload failed')
            return False    
        else:
            payload = json.dumps({
            "collection": "Product",
            "database": "Crawler",
            "dataSource": "Cluster",
            "filter":{'Name': data.get('Name'), 'Url': data.get('Url')},
            # "options": {"ordered": False}
            })
            response = requests.request("POST", url + 'findOne', headers=headers, data=payload)
            p = response.json().get('document')
            if p is None: # new Product
                payload = json.dumps({
                "collection": "Product",
                "database": "Crawler",
                "dataSource": "Cluster",
                "document": upPro
                # "options": {"ordered": False}
                })
                response = requests.request("POST", url + 'insertOne', headers=headers, data=payload)
                print('Upload status: ' + str(response.status_code))
            else: #updata Price
                if int(p.get('Price')) != data.get('Price'):
                    payload = json.dumps({
                    "collection": "Product",
                    "database": "Crawler",
                    "dataSource": "Cluster",
                    "filter":{'Name': data.get('Name'), 'Url': data.get('Url')},
                    "document": upPro
                    # "options": {"ordered": False}
                    })
                    response = requests.request("POST", url + 'replaceOne', headers=headers, data=payload)
                    print('Update status: ' + str(response.status_code))
            if int(post['Price']) > upPro.get('Price'):
                post['Price'] = upPro.get('Price')
                payload = json.dumps({
                "collection": "Category",
                "database": "Crawler",
                "dataSource": "Cluster",
                "filter":{'Name': data.get('NameCategory')},
                "document": post
                # "options": {"ordered": False}
                })
                response = requests.request("POST", url + 'replaceOne', headers=headers, data=payload)
        
        uploadWebsite(data.get('Url'))
        print(upPro)    
        return True
    except Exception as e:
        print("Exception throws")
        print(e)
    return False

# imgs = ["https://cdn.ankhang.vn/media/product/250_22214_laptop_dell_inspiron_3520_n3520_n5i5122w1_1.jpg"]
def uploadCate(data):
    try:
        payload = json.dumps({
            "collection": "Category",
            "database": "Crawler",
            "dataSource": "Cluster",
            "filter":{'Name': data.get('Name')},
            # "options": {"ordered": False}
        })
        response = requests.request("POST", url + 'findOne', headers=headers, data=payload)
        post = response.json().get('document')
        if post is None:# new category
            print('Load new Category...')
            payload = json.dumps({
                "collection": "Category",
                "database": "Crawler",
                "dataSource": "Cluster",
                # "filter":{'Name': data.get('Name')},
                "document": data
                # "options": {"ordered": False}
            })  
            response = requests.request("POST", url + 'insertOne', headers=headers, data=payload)
            print('Upload Status: ' + str(response.status_code))
        else:
            print('Category is existed')
            return False
    except Exception as e:
        print(e)
        return False


def get_all_json():
    try:
        payload = json.dumps({
            "collection": "Category",
            "database": "Crawler",
            "dataSource": "Cluster",
            "filter": {}
        })
        response = requests.request("POST", url + 'find', headers=headers, data=payload)
        cate = response.json()['documents']

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
            payload = json.dumps({
                "collection": "Product",
                "database": "Crawler",
                "dataSource": "Cluster",
                "filter": {'NameCategory': name_cate}
            })
            response = requests.request("POST", url + 'find', headers=headers, data=payload)
            product = response.json()['documents']
            # print(len(product))
            for p in product:
                payload = json.dumps({
                    "collection": "Website",
                    "database": "Crawler",
                    "dataSource": "Cluster",
                    "filter": {'Domain': p.get('WebDomain')}
                })
                response = requests.request("POST", url + 'findOne', headers=headers, data=payload)
                web = response.json()['document']
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

