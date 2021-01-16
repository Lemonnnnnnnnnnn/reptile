import scrapy
from ..items import BeautifulpicItem
import logging


class ExampleSpider(scrapy.Spider):
    name = 'beautyPic'
    allowed_domains = ['desk.zol.com.cn']
    start_urls = ['http://desk.zol.com.cn/meinv/']

    # 爬取页面
    def parse(self, response):
        # 提取href属性值,get表示若href有多个属性值，获取第一个
        list_next_page = response.xpath("//a[@id='pageNext']/@href").get()
        # 如果有下一页，继续爬取下一页
        if (list_next_page):
            list_next_page = response.urljoin(list_next_page)
            yield scrapy.Request(list_next_page, callback=self.parse)

        # img_list = response.xpath("//a[@class='pic']/@href").getall()
        img_list = response.xpath("//a[@class='pic']/@href").getall()
        if (img_list):
            for item in img_list:
                img_list_url = response.urljoin(item)

                yield scrapy.Request(img_list_url, callback=self.album_parse)

    # 进入相册页
    def album_parse(self, response):
        img_next_page = response.xpath("//a[@id='pageNext']/@href").get()
        album_name = response.xpath('//a[@id="titleName"]/text()').get()
        if (img_next_page and img_next_page != 'javascript:;'):
            img_next_page = response.urljoin(img_next_page)
            yield scrapy.Request(img_next_page, callback=self.album_parse)

        BigimgUrl = response.xpath('//dd[@id="tagfbl"]/a[1]/@href').get()
        BigimgUrl = response.urljoin(BigimgUrl)
        yield scrapy.Request(BigimgUrl, callback=self.img_parse, cb_kwargs=dict(album_name=album_name))


    # 进入图片页
    def img_parse(self, response ,album_name):
        downloadUrl = response.xpath('//img[1]/@src').get()
        item = BeautifulpicItem()
        item['image_urls'] = downloadUrl
        item['name'] = album_name

        return item
