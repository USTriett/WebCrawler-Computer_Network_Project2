# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EricspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ProductLazadaItem(scrapy.Item):
    Name = scrapy.Field()
    Price = scrapy.Field()
    Imgs = scrapy.Field()
    Desc = scrapy.Field()
