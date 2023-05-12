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
    # print(data)
    # print(data.get('Url'))
    try: 
        # print(url)
        domain = parse_domain(url)
        upPro = {
            "Url": url,
            "Name": data.get('Name'),
            "Price": data.get('Price'),
            "OriginalPrice": data.get('OriginalPrice'),
            "Imgs": data.get('Imgs'),
            "NameCategory": data.get('NameCategory'),
            "WebDomain": domain
        }
        
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

data = {
        "Name": "Laptop MSI Modern 15 A11M (i5-1155G7/RAM 8GB/512GB SSD/ Windows 11)",
        "Price": "13990000",
        "Type": "Laptop",
        "Imgs": [
            "https://lh3.googleusercontent.com/AuqhERmRG5UzcXhYp4bksbuNkPecHQzTdlBN8COMmC866UWUcKE9P3DnEOFsWjB64G8UYAZJbrvpNgeec3M664cagmbuJXtt",
            "https://lh3.googleusercontent.com/p5iKyyLKPYdHC-x4qImhfDOleAHNXLFGYvWg0mFHBAEIhGC8x15b7_9c7Y1Am75CM3DvwUNM7it3o4f7N4f1scZfbbpMZZVI",
            "https://lh3.googleusercontent.com/QTDmu2AsIrhfxYH_lmTRKK488Sa4BX_ypGUeqPmIXReexolTJSONXCUakcMgRaGmS5FFnuqTMr85TJlBk_Wg4oKnv5K1fwo",
            "https://lh3.googleusercontent.com/muBEYkfQ4gNo8s4rEmkw4YGXANBlhyiRaPq2bAiu9uOHgo45dB9-QQy8181HhZ96jsZoros5jXbrFmzIMqDPhruuvcMU4T4",
            "https://lh3.googleusercontent.com/6jrMhLA161SkP3riT2UjbMs_aX4vOx5tKsypdEYTxphunEwUj0iCWWWIyqnexdm_HmPeiyla8HtdV9koULj2Yjw4i9yGZQA",
            "https://lh3.googleusercontent.com/HoaHzIVBSolNHQH15OPinlJVq6IrD2H61QqQkBZyBqynO2M19YY0Vvuwna9cbzaaMWsC5yw43JiTGHKhs-UMm4nAAG6XFfjn",
            "https://lh3.googleusercontent.com/ERAMeOhYYCnl0dLRAvVV3VzfUDtixW9ObKhQU4PNDaFPqQzjKK2dQ68PJZ62Xu9lWFzPDxdIa8G2z82STkjzJuBX8MF-nlSM"
        ],
        "Desc": {
            "CPU": " Core i5 , Intel Core thế hệ thứ 11 ",
            "OCung": " 15.6\" ( 1920 x 1080 ) Full HD  IPS  không cảm ứng , HD webcam ",
            "RAM": " Onboard  Intel Iris Xe Graphics ",
            "Card": " Intel Core i5-1155G7 ( 2.5 GHz - 4.5 GHz / 8MB / 4 nhân, 8 luồng ) i5-1155G7 ",
            "ManHinh": " 1 x 8GB  DDR4  3200MHz ( 2 Khe cắm / Hỗ trợ tối đa 64GB )",
            "HDH": " thường , LED ",
            "KT&KL": " Windows 11  Windows 11 ,  3 cell  52 Wh , Pin liền "
        }
    }
uploadCate(data)

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

