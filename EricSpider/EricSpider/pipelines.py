# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json   
import sqlite3
import os
class JsonWriterPipeline:
    def __init__(self):
        self.file = open('DataFile/items.json', 'w', encoding="utf-8")
        if os.stat('DataFile/items.json').st_size == 0:
            self.file.write('[\n')

    def process_item(self, item, spider):
        if not item['Imgs']:
            item['Imgs'] = ""
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + ",\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.seek(self.file.tell() - 2) # remove the last comma
        self.file.write('\n]')
        self.file.close()
    
class JsonCateWriterPipeline:
    def __init__(self):
        self.file = open('DataFile/category1.json', 'w', encoding="utf-8")
        if os.stat('DataFile/category1.json').st_size == 0:
            self.file.write('[\n')

    def process_item(self, item, spider):
        if not item['Imgs']:
            item['Imgs'] = ""
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + ",\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.seek(self.file.tell() - 2) # remove the last comma
        self.file.write('\n]')
        self.file.close()

#  #work with database sqlite3
# class EricspiderPipeline(object):
#     def __init__(self):
#         self.connection = sqlite3.connect('productItem.db')
#         self.cursor = self.connection.cursor()
#         self.cursor.execute('''
#             CREATE TABLE IF NOT EXISTS products (
#                 ID TEXT,
#                 pname TEXT unique,
#                 originprice INTEGER,
#                 price INTEGER,
#                 imgs TEXT,
#                 url TEXT,
#                 webDomain TEXT,
#                 desc TEXT
#             )
#         ''')
#         self.connection.commit()

#     def process_item(self, item, spider):
#         self.cursor.execute('''
#             INSERT OR IGNORE INTO products (id, pname, originprice, price, imgs, url, wedDomain, desc)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#         ''', (item['ID'], item['Name'], item['OriginPrice'], item['Price'], ','.join(item['Imgs']), item['Url'], item['WebDomain'], ','.join(item['Desc'])))
#         self.connection.commit()
#         return item

#     def close_spider(self, spider):
#         self.connection.close()