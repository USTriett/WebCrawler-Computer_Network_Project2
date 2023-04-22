# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json   
import sqlite3
class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file = open('items.json', 'w', "utf-8")
    def process_item(self, item, spider):
        try:
            print(item)
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            self.file.write(line)
        except:
            print('something wrong')
        return item
    def close_spider(self, spider):
        self.file.close()
    
    
class EricspiderPipeline:
    def __init__(self):
        self.conn = sqlite3.connect('test2.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS testTable (title TEXT, price TEXT, link TEXT)')

    def process_item(self, item, spider):
        self.cursor.execute('INSERT INTO testTable (title, price, link) VALUES (?, ?, ?)', (item['title'], item['price'], item['href']))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()
# class QuotesJsScraperPipeline:
#     def process_item(self, item, spider):
#         return item