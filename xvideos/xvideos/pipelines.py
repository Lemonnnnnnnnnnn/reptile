# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import json
from aria2_download import a2D
import constant
from common import remove_aria2, random_chose_node


class XvideosPipeline:
    def open_spider(self, spider):
        logging.info('爬取开始')
        self.dlServer = a2D()
        self.video_download_url = constant.video_download_url

    def process_item(self, item, spider):
        random_chose_node()
        self.dlServer.get_file_from_url(url=item['url'], dir=self.video_download_url, file_name=item['name'] + '.mp4')
        return item

    def close_spider(self, spider):
        logging.info('爬取结束')
        print('开始校验...')
        self.dlServer.verify()
        print('校验完成')
        print('移除出错的aria2文件...')
        remove_aria2(self.video_download_url)
        print('完成！')
