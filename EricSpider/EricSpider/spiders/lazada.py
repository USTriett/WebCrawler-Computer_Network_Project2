import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.common.by import By

from EricSpider.items import ProductLazadaItem

class LazadaSpider(scrapy.Spider):
    name = "lazada"
    allowed_domains = ["www.lazada.vn"]
    max_page = 10
    def start_requests(self):
        start_url = 'https://www.lazada.vn/laptop/?page=1&spm=a2o4n.home.cate_1.3.19053bdc7bBAWL'
        
        yield SeleniumRequest(
            url = start_url,
            wait_time=2,
            # screenshot=True,
            callback=self.parse
        )
        

    def parse(self, response):
        self.driver.get(response.url)
        hrefs = response.css('div._95X4G a::attr(href)').extract()
        for href in hrefs:
            self.driver.get(href)
            # do something with the page source
            srcHtml = self.driver.page_source
            sel = Selector(text=srcHtml)
            product = ProductLazadaItem()
            try:
                product['Name'] = quote.css('div.RfADt a::attr(title)').get()
                product['Price'] = quote.css('div.aBrP0 span.ooOxS::text').get()
                product['Imgs'] = quote.css('div.RfADt a::attr(href)').get()
                product['Desc'] = quote.css('div.RfADt a::attr(href)').get()
                # print(product)
                yield product
            except:
                print('something wrong')
        
        # try:
        #     with open('image.png', 'wb') as image_file:
        #         image_file.write(response.meta['screenshot'])
        # except:
        #     print('something wrong1')
       

        driver = response.request.meta['driver']
        button = driver.find_element(By.CSS_SELECTOR, 'li.ant-pagination-next button.ant-pagination-item-link')
        if button:
            button.click()
            # Get the link
            link = driver.current_url
            if link:
                yield SeleniumRequest(
                url=link,
                wait_time=2,
                callback=self.parse
                )
       
