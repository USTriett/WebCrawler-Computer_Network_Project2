# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EricspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Category(scrapy.Item):
    Url = scrapy.Field()
    Name = scrapy.Field()
    Price = scrapy.Field()
    Original_Price = scrapy.Field()
    Type = scrapy.Field()
    Imgs = scrapy.Field()
    Desc = scrapy.Field()

class Product(scrapy.Item):
    Url = scrapy.Field()
    Name = scrapy.Field()
    Price = scrapy.Field()
    OriginalPrice = scrapy.Field()
    NameCategory = scrapy.Field()
    Imgs = scrapy.Field()
    
class ProductLazadaItem(scrapy.Item):
    Name = scrapy.Field()
    Price = scrapy.Field()
    Imgs = scrapy.Field()
    Url = scrapy.Field()
    WebDomain = scrapy.Field()
    Desc = scrapy.Field()
    pass

class ProductAnKhangItem(scrapy.Item):
    ID = scrapy.Field()
    Name = scrapy.Field()
    OriginPrice = scrapy.Field()
    Price = scrapy.Field()
    Imgs = scrapy.Field()
    Url = scrapy.Field()
    WebDomain = scrapy.Field()
    Desc = scrapy.Field()
    pass