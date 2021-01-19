# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo


class LagouPipeline:
    collection_name = 'lagou_items'

    def open_spider(self, spider):
        logging.info('爬取开始')
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client["lagou"]
        logging.info('已连接数据库')

        # dbList = self.client.list_database_names()
        # if "lagou" in dbList:
        #     print('数据库已存在')

    def close_spider(self, spider):
        self.client.close()
        pass

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item
