# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import json


class HentaimamaPipeline:
    def open_spider(self, spider):
        logging.info('爬取开始')
        self.f = open('hentaimama.txt', 'w')
        self.list = []

    def process_item(self, item, spider):
        logging.info('添加url地址')
        self.list.append(item['file_urls'])
        return item

    def close_spider(self, spider):
        logging.info('爬取结束')
        content = json.dumps(self.list)
        self.f.write(content)
        self.f.close()
