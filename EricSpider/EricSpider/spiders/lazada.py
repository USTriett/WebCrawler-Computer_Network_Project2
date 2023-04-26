# import scrapy
# from scrapy_selenium import SeleniumRequest
# from scrapy.selector import Selector
# from selenium.webdriver.common.by import By

# from EricSpider.items import ProductLazadaItem

# class LazadaSpider(scrapy.Spider):
#     name = "lazada"
#     allowed_domains = ["www.lazada.vn"]
#     max_page = 10
#     def start_requests(self):
#         start_url = 'https://www.lazada.vn/laptop/?page=1&spm=a2o4n.home.cate_1.3.19053bdc7bBAWL'
        
#         yield SeleniumRequest(
#             url = start_url,
#             wait_time=2,
#             # screenshot=True,
#             callback=self.parse
#         )
        

#     def parse(self, response):
#         self.driver.get(response.url)
#         hrefs = response.css('div._95X4G a::attr(href)').extract()
#         for href in hrefs:
#             self.driver.get(href)
#             # do something with the page source
#             srcHtml = self.driver.page_source
#             sel = Selector(text=srcHtml)
#             product = ProductLazadaItem()
#             try:
#                 product['Name'] = quote.css('div.RfADt a::attr(title)').get()
#                 product['Price'] = quote.css('div.aBrP0 span.ooOxS::text').get()
#                 product['Imgs'] = quote.css('div.RfADt a::attr(href)').get()
#                 product['Desc'] = quote.css('div.RfADt a::attr(href)').get()
#                 # print(product)
#                 yield product
#             except:
#                 print('something wrong')
        
#         # try:
#         #     with open('image.png', 'wb') as image_file:
#         #         image_file.write(response.meta['screenshot'])
#         # except:
#         #     print('something wrong1')
       

#         driver = response.request.meta['driver']
#         button = driver.find_element(By.CSS_SELECTOR, 'li.ant-pagination-next button.ant-pagination-item-link')
#         if button:
#             button.click()
#             # Get the link
#             link = driver.current_url
#             if link:
#                 yield SeleniumRequest(
#                 url=link,
#                 wait_time=2,
#                 callback=self.parse
#                 )



# from scrapy import Spider
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
from EricSpider.items import ProductLazadaItem
from scrapy_pyppeteer.handler import ScrapyPyppeteerDownloadHandler
# from selenium import webdriver
import scrapy
from bs4 import BeautifulSoup
import pyppeteer
from scrapy_pyppeteer.page import PageCoroutine
from pyppeteer.errors import TimeoutError
class LazadaSpider(scrapy.Spider):
    name = 'lazada'
    start_urls = ['https://www.lazada.vn/laptop/?page={}&sort=pricedesc&spm=a2o4n.home.cate_1.3.19053bdcqUEQV8'.format(i) for i in range(1, 5)]
    allowed_domains = ["www.lazada.vn"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url , meta={"pyppeteer": True})

    def extract_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.select('div.RfADt a')
        links = [element.get('href') for element in elements]
        return links

    def parse(self, response):
        links = self.extract_links(response.text)
        coroutines = [
        PageCoroutine('evaluate', 'window.scrollTo(0, document.body.scrollHeight / 2)'),
        PageCoroutine('waitForSelector', 'button.pdp-view-more-btn', TimeoutError = 5000),
        PageCoroutine('click', 'button.pdp-view-more-btn')
        ]
        for link in links:
            try:
                yield response.follow(link, self.parse_item, cb_kwargs={'href': link}, meta={"pyppeteer": True, "pyppeteer_page_coroutines": coroutines})
            except TimeoutError:
                # Handle the case where the button is not found
                print("Button not found")

                


    def parse_item(self, response, href):
        try:
            print('processing on ' + href + '\n')
            soup = BeautifulSoup(response.text, 'html.parser')
            product = ProductLazadaItem()
            try:
                product['Name'] = soup.select_one('h1.pdp-mod-product-badge-title').text
                text = soup.select_one('span.pdp-price').text
                      
                new_string = ''.join([char for char in text if char.isdigit()])
            
                product['Price'] = int(new_string)
                img_srcs = [img.get('src') for img in soup.select('img.pdp-mod-common-image')]
                product['Imgs'] = img_srcs
                #Extract desc
                product['Desc'] = []
                elements_list = soup.select('article.lzd-article')
                if not elements_list:
                    # No elements were found
                    print("No elements found")
                else:
                    text = [article.text for article in elements_list]
                    product['Desc'] = text
                
                product['WebDomain'] = self.allowed_domains[0]
                product['Url'] = href

                print(product)
                yield product
            except Exception as e:
                print('Catch in parse: ')
                print(e)
                pass
        except TimeoutError as e:
            print('Catch in time: ')
            print (e)  
        


    # def parse(self, response):
        # Get the hrefs of the items on the page
        # driver = response.request.meta['driver']
        
        # print('response url:' + response.url)

        # elements = self.river.find_elements(By.CSS_SELECTOR, 'div.RfADt a')
        # item_hrefs = [element.get_attribute('href') for element in elements]
        
        #Follow each href to crawl the information of each item
        # count = 0
        # for href in item_hrefs:
        #     if(count == 1):
        #         break
        #     count += 1
        #     yield response.follow(href, self.parse_item, cb_kwargs={'href': href})
        # self.driver.close()

    # def parse_item(self, response, href):
    #     # Use Selenium to interact with the dynamic web page
    #     print('Starting parse_item')
    #     driver = response.request.meta['driver']
    #     driver.get(response.url)
        
    #     # Wait for the dynamic content to load
    #     WebDriverWait(driver, 3)
    
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3)")
    #     try:
    #         button = driver.find_element(By.XPATH, '//button[contains(@class, "pdp-view-more-btn")]')
    #         button.click()
    #         print('button is clicked')
    #     except Exception as e:
    #         print(e)
    #     # Extract the data from the dynamic content
    #     product = ProductLazadaItem()
    #     try:
    #         print("hey\n\n\n\n")
    #         elements = driver.find_elements(By.XPATH, '//h1[contains(@class, "pdp-mod-product-badge-title")]')
    #         text = ''.join([element.text for element in elements])
    #         product['Name'] = text
    #         elements = driver.find_element(By.XPATH,'//span[contains(@class, "pdp-price")]')
            
    #         new_string = ''.join([char for char in elements.text if char.isdigit()])
            
    #         product['Price'] = int(new_string)

    #         product['Imgs'] = response.xpath('//img[contains(@class, "pdp-mod-common-image")]/@src').extract()
    #         #Extract desc
    #         elements = driver.find_elements(By.XPATH,'//article[contains(@class, "lzd-article")]')
    #         text = '\n'.join([element.text for element in elements])
    #         product['Desc'] = text
    #         product['WebDomain'] = self.allowed_domains[0]
    #         product['Url'] = href

    #         print(product)
    #         yield product
    #     except Exception as e:
    #         print(e)

       
       
