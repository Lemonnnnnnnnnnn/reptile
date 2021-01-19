import scrapy
from .aria2_download import aria2DL
import logging
import re


class HentaimaSpider(scrapy.Spider):
    name = 'hentaima'
    allowed_domains = ['hentaimama.io']
    start_urls = ['https://hentaimama.io/tvshows/3d/']
    list = []

    def parse(self, response):
        videoList = response.xpath(
            '//article[@class="item se episodes"]/div[@class="poster"]/div[@class="season_m animation-4"]/a/@href').getall()
        # yield scrapy.Request(videoList[0], callback=self.video_item)
        for item in videoList:
            yield scrapy.Request(item, callback=self.video_item)

    def video_item(self, response):
        # 由于iframe无法直接获取到目标元素 ， 解决方法：进入iframe页面
        try:
            iframe_url = response.xpath('//iframe/@src').get()
            yield scrapy.Request(url=iframe_url, callback=self.iframe)
        except Exception as e:
            logging.error('无法在当前页面找到视频资源')
            logging.error(e)

    def iframe(self, response):
        try:
            if (re.search(r"file: '(.+)',", response.text)):
                case1 = re.search(r"file: '(.+)',", response.text).group(1)
                logging.info('第一种获取方式：' + case1)
            else:
                case2 = response.xpath('//video[@id="my-video"]/source/@src').get()
                logging.info('第二种获取方式：' + case2)

        except Exception as e:
            logging.info('頁面結構為：' + response.text)
            logging.error(e)

        pass
