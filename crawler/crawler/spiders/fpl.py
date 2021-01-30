import scrapy
import re
from urllib.parse import unquote
from ..items import CrawlerItem
import parsel


class FplSpider(scrapy.Spider):
    name = 'fpl'
    allowed_domains = ['freeproxylists.net']
    start_urls = ['http://freeproxylists.net/zh/']

    def parse(self, response):
        pageNum = response.xpath('//div[@class="page"]/a[last()-1]/text()').get()
        for i in range(int(pageNum)):
            url = 'http://freeproxylists.net/zh/?page=' + str(i + 1)
            yield scrapy.Request(url=url, callback=self.page_parse)

    def page_parse(self, response):
        list = response.xpath('//tr[contains(@class,"Odd")or contains(@class,"Even")]')
        for item in list:
            try:
                IPunDecode = item.xpath('.//td[1]/script').get()
                IPDecode = unquote(re.search(r'"(.+)"', IPunDecode).group(1))
                sel = parsel.Selector(IPDecode)
                IP = sel.xpath('//a/text()').get()
                port = item.xpath('.//td[2]/text()').get()
                type = item.xpath('.//td[3]/text()').get()
                obj = CrawlerItem()
                obj['IP'] = IP + ':' + port
                obj['type'] = type
                yield obj

            except Exception as e:
                print(e)
                # 捕获报错后不要停止循环而是继续循环
                continue
