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



from scrapy import Spider
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from EricSpider.items import ProductLazadaItem

class LazadaSpider(Spider):
    name = 'lazada'
    start_urls = ['https://www.lazada.vn/laptop/?page=1&sort=pricedesc&spm=a2o4n.home.cate_1.3.19053bdcqUEQV8']
    allowed_domains = ["www.lazada.vn"]
    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
              url = url,
              wait_time=2,
              # screenshot=True,
              callback=self.parse
              )

    def parse(self, response):
        # Get the hrefs of the items on the page
        item_hrefs = response.css('div.RfADt a::attr(href)').getall()
        
        
        # Follow each href to crawl the information of each item
        count = 0
        for href in item_hrefs:
            yield response.follow(href, self.parse_item, cb_kwargs={'href': href})

    def parse_item(self, response, href):
        # Use Selenium to interact with the dynamic web page
        print('Starting parse_item')
        driver = response.request.meta['driver']
        driver.get(response.url)
        
        # Wait for the dynamic content to load
        WebDriverWait(driver, 3)
    
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3)")
        try:
            button = driver.find_element(By.XPATH, '//button[contains(@class, "pdp-view-more-btn")]')
            button.click()
            print('button is clicked')
        except Exception as e:
            print(e)
        # Extract the data from the dynamic content
        product = ProductLazadaItem()
        try:
            print("hey\n\n\n\n")
            elements = driver.find_elements(By.XPATH, '//h1[contains(@class, "pdp-mod-product-badge-title")]')
            text = ''.join([element.text for element in elements])
            product['Name'] = text
            elements = driver.find_element(By.XPATH,'//span[contains(@class, "pdp-price")]')
            
            new_string = ''.join([char for char in elements.text if char.isdigit()])
            
            product['Price'] = int(new_string)

            product['Imgs'] = response.xpath('//img[contains(@class, "pdp-mod-common-image")]/@src').extract()
            #Extract desc
            elements = driver.find_elements(By.XPATH,'//article[contains(@class, "lzd-article")]')
            text = '\n'.join([element.text for element in elements])
            product['Desc'] = text
            product['WebDomain'] = self.allowed_domains[0]
            product['Url'] = href

            print(product)
            yield product
        except Exception as e:
            print(e)

       
       
