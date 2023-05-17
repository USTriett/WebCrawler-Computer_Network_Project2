import scrapy 
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from scrapy_pyppeteer.page import PageCoroutine
from pyppeteer.errors import TimeoutError
import sys
sys.path.insert(0, '/path/to/module/directory')
import re
import ListName
from EricSpider.items import Product

class GoogleSpider(scrapy.Spider):
    name = "google"
    start_list = ListName.get_names('DataFile/category1.json')
    # start_list = ["Laptop HP Pavilion 15-eg2059TU"]
    # start_urls = [ 'https://www.google.com.vn/search?q={}'.format(s) for s in start_list]
    # allowed_domains = ['api.scraperapi.com']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  
            'EricSpider.middlewares.RotateUserAgentMiddleware': 400,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 100, 
        },
        'ITEM_PIPELINES': {"EricSpider.pipelines.ProductUploader": 502},
        'ROBOTSTXT_OBEY': False,
        'LOG_LEVEL': 'WARNING',
        'CONCURRENT_REQUESTS_PER_DOMAIN': 10,
        'RETRY_TIMES': 5
    }
    def start_requests(self):
        queries = self.start_list
        for query in queries:
            url = 'https://www.google.com/search?q={}'.format(query)
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(cname = query), meta=dict(
                pyppeteer=True,
                pyppeteer_page_coroutines=[
                    PageCoroutine("waitForSelector", 'a.pla-unit-title-link span.pymv4e')
                ],
                url = url
            ))

    def convert_to_vnd(self ,s):
        # Define conversion rates
        usd_to_vnd = 23000
        eur_to_vnd = 27000

        # Use regular expressions to find all money values in the string
        # money_values = string

        # Initialize total in VND
        total_vnd = 0
        s = s.replace(',', '')
        # s = s.replace('.', '')
        # Iterate over money values and convert to VND
        value = 0
        if '$' in s:
            # Remove the dollar sign and convert to float
            value = float(s.replace('$', ''))
            #Convert to VND
            total_vnd = value * usd_to_vnd
        elif '€' in s:
            # Remove the euro sign and convert to float
            value = float(s.replace('€', ''))
            # Convert to VND
            total_vnd = value * eur_to_vnd
        elif '£' in s:
            # Remove the euro sign and convert to float
            value = float(s.replace('£', ''))
            # Convert to VND
            total_vnd = value * eur_to_vnd
        elif 'USD' in s:
            total_vnd += float(value[:-3]) * usd_to_vnd
        elif 'E' in s:
            total_vnd += float(value[:-1]) * eur_to_vnd
        elif 'VND' in s:
            new_string = ''.join([char for char in s if char.isdigit()])
            value = float(new_string)
            total_vnd += value
        else:
            new_string = ''.join([char for char in s if char.isdigit()])
            return int(new_string)
        return int(total_vnd)


    def parse(self, response, cname):
        print('processing on '+ '\n')
        soup = BeautifulSoup(response.text, 'html.parser')
        imgs = soup.select('div.Gor6zc img')
        names = soup.select('a.pla-unit-title-link span.pymv4e')
        urls = soup.select('a.clickable-card')
        prices = soup.select('span.e10twf')
        # print(1)
        try:
            print(len(names))
            for index in range(0, 2):
                if(index == len(names)):
                    break
                product = Product()
                product['Url'] = ''
                product['Name'] = ''
                product['Price'] = 0
                product['OriginalPrice'] = 0
                product['NameCategory'] = ''
                product['Imgs'] = []

                product['NameCategory'] = cname

                    # img = soup.select('div.image-wrapper picture.webpimg-container img')
                product['Imgs'].append(imgs[index].get('src'))

                # name = soup.select('div.name h3')
                product['Name'] = names[index].text

                # url = soup.select('a.product-item')  
                product['Url'] = urls[index].get('href')

                # text_price = soup.select_one('div.price-discount__price')
                print(prices[index].text)
                price = self.convert_to_vnd(prices[index].text)
                product['Price'] = price
                product['OriginalPrice'] = price
                print(product)
                yield product

        except Exception as e:
              print(e)
              pass    
    



  # def parse_item(sef, response):
  #   print(response.url)