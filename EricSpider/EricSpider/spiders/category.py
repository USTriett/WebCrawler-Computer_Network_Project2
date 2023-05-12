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
class WebCrawlerSpider(scrapy.Spider):
    name = 'PhongVuCrawler'
    setUrls = set()
    custom_settings = {
                'DOWNLOADER_MIDDLEWARES' :{
                     'scrapy_selenium.SeleniumMiddleware': 800
                     },
               'ITEM_PIPELINES' : {"EricSpider.pipelines.JsonCateWriterPipeline": 502}

    }
   
  

    def start_requests(self):
        
        crawler_search_url = ['https://phongvu.vn/sitemap_categories_NH01-01-01-0{}.xml'.format(str(s)) for s in range(1, 4)]
        print(crawler_search_url)
        for i in range(0, 3):
            yield SeleniumRequest(url=crawler_search_url[i], callback=self.parse_search_results, wait_time=10)

    def parse_search_results(self, response):
        url_products  = response.css('.folder > div.opened > div:nth-child(2) > span:nth-child(2)::text').getall()
        # if url_products is not None:
        #     lenn = 1600
        #     maxx = lenn * 0
        #     for i in range(0, len(url_products), 2):
        #         url = url_products[i]
        #         if i >= maxx and i < maxx + lenn:
        #             print(url)
        #             yield SeleniumRequest(url=url, callback=self.parse_product_data, wait_time=10, wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, '#__NEXT_DATA__')), meta={'url': url})
        self.setUrls.update(ListName.get_url('DataFile/Category.json'))
        list_urls = set()
        for url in url_products:
            if url.startswith('https://phongvu.vn'):
                list_urls.add(url)
        list_urls = list_urls.symmetric_difference(list_urls.intersection(self.setUrls))
        self.setUrls = self.setUrls.union(list_urls)
        # count = 0
        for url in self.setUrls:
            # if(count == 3):
            #     break
            # count += 1     
            print(url)
            yield scrapy.Request(url=url, callback= self.parse_product_data, meta=dict(
                pyppeteer=True,
                pyppeteer_page_coroutines=[
                    PageCoroutine("waitForSelector", '#__NEXT_DATA__')
                ],
                url = url,
            ),)

    def parse_product_data(self, response):
        print(response.meta['url'])
        detail_product = json.loads(response.css('#__NEXT_DATA__::text').get())
        # print(detail_product['props']['pageProps']['serverProduct'])
        try:
            detail_product = json.loads(response.css('#__NEXT_DATA__::text').get())
            # print(detail_product['additionalProperty'][8]['value'])
            data = {
                'Name': detail_product['props']['pageProps']['serverProduct']['product']['productInfo']['displayName'],
                'Price': detail_product['props']['pageProps']['serverProduct']['priceAndPromotions']['price'],
                'Type': 'Laptop',
                'Imgs': [sub['url'] for sub in detail_product['props']['pageProps']['serverProduct']['product']['productDetail']['images']],
                'Desc': [
                    {
                        'CPU': detail_product['props']['pageProps']['serverProduct']['product']['productDetail']['attributeGroups'][8]['value'],
                        'OCung': detail_product['props']['pageProps']['serverProduct']['product']['productDetail']['attributeGroups'][12]['value'],
                        'RAM': detail_product['props']['pageProps']['serverProduct']['product']['productDetail']['attributeGroups'][10]['value'],
                        'Card': detail_product['props']['pageProps']['serverProduct']['product']['productDetail']['attributeGroups'][9]['value'],
                        'ManHinh': detail_product['props']['pageProps']['serverProduct']['product']['productDetail']['attributeGroups'][11]['value'],
                        'HDH': detail_product['props']['pageProps']['serverProduct']['product']['productDetail']['attributeGroups'][19]['value'],
                        'KT&KL': detail_product['props']['pageProps']['serverProduct']['product']['productDetail']['attributeGroups'][20]['value'] + ', ' + detail_product['props']['pageProps']['serverProduct']['product']['productDetail']['attributeGroups'][22]['value']
                    }
                ]
            }
            # upload caterogy
            record = data.copy()
            record['Name'] = record['Name'].split(' (')[0]
            record['Desc'] = record['Desc'][0]
            record['Price'] = json.dumps(record['Price'])

            category = Category()
            category['Name'] = record['Name']
            category['Price'] = record['Price']      
            category['Type'] = record['Type']
            category['Imgs'] = record['Imgs']
            category['Desc'] = record['Desc']
            print(category)
            yield category
        except Exception as e:
            print(e)
        
