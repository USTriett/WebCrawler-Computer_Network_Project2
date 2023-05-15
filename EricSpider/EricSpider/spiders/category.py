import scrapy 
from scrapy.linkextractors import LinkExtractor
import scrapy
from bs4 import BeautifulSoup
from scrapy_pyppeteer.page import PageCoroutine
from pyppeteer.errors import TimeoutError
import sys
sys.path.insert(0, '/path/to/module/directory')
import json
from EricSpider.items import Category
import xml.etree.ElementTree as ET
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode
from shutil import which
import ListName
import re
class WebCrawlerSpider(scrapy.Spider):
    name = 'LaptopCrawler'
    setUrls = set()
    custom_settings = {
               'ITEM_PIPELINES' : {"EricSpider.pipelines.JsonCateWriterPipeline": 502}

    }
   
  

    def start_requests(self):
        
        crawler_search_url = ['https://fptshop.com.vn/may-tinh-xach-tay?trang=23']
        # print(crawler_search_url)
        
        yield scrapy.Request(url=crawler_search_url[0], callback=self.parse_product_data, meta=dict(
            pyppeteer=True,
            pyppeteer_page_coroutines=[
                PageCoroutine("waitForSelector", 'div.cdt-product div.cdt-product__info')
            ],
            url = crawler_search_url[0]
        ),)

    
    def parse_product_data(self, response):
        print(response.meta['url'])
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.select('div.cdt-product div.cdt-product__info')
        imgs = soup.select('div.cdt-product div.cdt-product__img')
        names = soup.select('div.cdt-product div.cdt-product__info h3 a')
        # prices = soup.select('div.cdt-product div.cdt-product__info div.progress')
        descs = soup.select('div.cdt-product div.cdt-product__info div.cdt-product__config__param') # 6 thong so
            # print(detail_product['additionalProperty'][8]['value'])
        print(len(divs))
        try:
            
            # upload caterogy
            for i in range(0, len(divs) - 1):
                category = Category()
                category['Name'] = ''
                category['Price'] = 1000000000   
                category['Type'] = 'Laptop'
                category['Imgs'] = []
                category['Desc'] = []
                try:
                    category['Name'] = str(names[i].get('title'))
                    img = imgs[i].find('img')
    
                    if img is None:
                        style = imgs[i]['style']
                        img = re.search(r'url\("(.+?)"\)', style).group(1)
                        print(img)
                    else:
                        img = img.get('src')
                    category['Imgs'].append(img)
                    spans = descs[i].find_all('span')
                    # print(len(spans))
                    desc = [
                        {'CPU': spans[1].text},
                        {'RAM': spans[2].text},
                        {'Ổ Cứng': spans[3].text},
                        {'Card Đồ hoạ': spans[4].text},
                        {'KT&KL': spans[0].text + ' & ' + spans[5].text}
                    ]
                    category['Desc'] = desc
        
                    print(category)
                    yield category
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
        
