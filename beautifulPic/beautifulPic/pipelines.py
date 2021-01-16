# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import scrapy

# 自定义类ImagespiderPipeline继承了ImagesPipeline这个类，
# 里面的方法将覆盖ImagesPipeline中的方法
# 可以理解为局部覆盖ImagesPipeline后，ImagesPipeline更改名字为ImagespiderPipeline进行调用
class ImagespiderPipeline(ImagesPipeline):
    # 下载目标路径
    def file_path(self, request, response=None, info=None, *, item):
        url = request.url
        file_name = url.split('/')[-1]
        return f'{item["name"]}/{file_name}.jpg'

    # 从item里取出url下载
    def get_media_requests(self, item, info):
        logging.info(item)
        yield scrapy.Request(item['image_urls'])


    # 下载完成
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item

# class BeautifulpicPipeline():
#
#     def process_item(self, item, spider):
#         logging.debug('进入process_item')
#         return item
