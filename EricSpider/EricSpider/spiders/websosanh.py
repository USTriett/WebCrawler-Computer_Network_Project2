import scrapy 
from scrapy.linkextractors import LinkExtractor
import scrapy
from bs4 import BeautifulSoup
from scrapy_pyppeteer.page import PageCoroutine
from pyppeteer.errors import TimeoutError
import sys
sys.path.insert(0, '/path/to/module/directory')
import re
import ListName
from EricSpider.items import Product
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class SoSanhSpider(scrapy.Spider):
    name = "sosanhgia"
    start_list = ListName.get_names('DataFile/category1.json')
    # start_list = ["Laptop HP Pavilion 15-eg2059TU"]
    start_urls = [ 'https://www.sosanhgia.com/s-{}'.format(s) for s in start_list]
    allowed_domains = ["www.sosanhgia.com"]
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    def start_requests(self):
        
        # for i in range(651, 709):
        #     url = 'https://www.sosanhgia.com/s-{}'.format(self.start_list[i])
        #     print(url)
        i = 0
        for url in self.start_urls:
            print(url)
            yield scrapy.Request(url, self.parse, cb_kwargs=dict(cname = self.start_list[i]), meta=dict(
                pyppeteer=True,
                # pyppeteer_page_coroutines=[
                #     PageCoroutine("waitForSelector", 'div.name h3')
                # ],
                url = url
            ),)
            i+=1
        self.driver.quit()
    def convert_to_vnd(self, s):
        # Define conversion rates
        usd_to_vnd = 23000
        eur_to_vnd = 27000

        # Use regular expressions to find all money values in the string
        # money_values = string

        # Initialize total in VND
        total_vnd = 0
        s = s.replace(',', '')
        # Iterate over money values and convert to VND
        for value in s:
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
            elif 'USD' in value:
                total_vnd += float(value[:-3]) * usd_to_vnd
            elif 'E' in value:
                total_vnd += float(value[:-1]) * eur_to_vnd
            elif 'VND' in value:
                new_string = ''.join([char for char in s if char.isdigit()])
                value = float(new_string)
                total_vnd += value
            else:
                new_string = ''.join([char for char in s if char.isdigit()])
                # print(new_string)
                value = float(new_string)
                # print(value)
                total_vnd = value
        return int(total_vnd)
    
    def parse_url(self, url, driver):
        
        
        # Go to first URL and click on Download menu
        driver.get(url=url)
        # print(1)
        return driver.current_url
        
        
    def parse(self, response, cname):
        # print('processing on '+ '\n')
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.select('div.grid__product-cell')
        
        imgs = soup.select('div.grid__product-cell div.grid__product-img img')
        names = soup.select('div.grid__product-cell div.grid__product-name')
        prices = soup.select('div.grid__product-cell div.grid__product-price')

        for i in range(0, len(divs)):
            product = Product()
            product['Url'] = ''
            product['Name'] = ''
            product['Price'] = 0
            product['OriginalPrice'] = 0
            product['NameCategory'] = ''
            product['Imgs'] = []
            try:
                id_str = str(divs[i].get('id'))
                id = ''.join([char for char in id_str if char.isdigit()])
                product['Imgs'].append(imgs[i].get('src'))
                product['NameCategory'] = cname
                product['Name'] = names[i].text
                # print(prices[i].text)
                price = self.convert_to_vnd(prices[i].text)
                product['Price'] = price
                product['OriginalPrice'] = price
                url = self.parse_url('https://www.sosanhgia.com/r/redirect.php?pm_id={}'.format(id), self.driver)
                
                product['Url'] = url
                print(product)
                yield product
            except Exception as e:
              print(e)
              pass    

    