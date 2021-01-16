import scrapy

class ProxySpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/ip']

    def parse(self,response):
        print(response.text)

