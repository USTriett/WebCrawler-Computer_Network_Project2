# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json   
import sqlite3
class JsonWriterPipeline:
    def __init__(self):
        self.file = open('items.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
    def close_spider(self, spider):
        self.file.close()
    
    


class EricspiderPipeline(object):
    def __init__(self):
        self.connection = sqlite3.connect('products.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                name TEXT unique,
                price INTEGER,
                imgs TEXT,
                url TEXT,
                wedDomain TEXT,
                desc TEXT
            )
        ''')
        self.connection.commit()

    def process_item(self, item, spider):
        self.cursor.execute('''
            INSERT OR IGNORE INTO products (name, price, imgs, url, wedDomain, desc)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (item['Name'], item['Price'], ','.join(item['Imgs']), item['Url'], item['WebDomain'], ','.join(item['Desc'])))
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.connection.close()