import scrapy
import logging
from urllib import parse
import json
from ..items import LagouItem


class LgSpider(scrapy.Spider):
    name = 'lg'
    allowed_domains = ['lagou.com']

    def start_requests(self):
        with open('D:\\technology\python\\reptile\lagou\lagou\spiders\cookie.txt', 'r') as f:
            cookieStr = f.read()
            self.cookies = {}
            for item in cookieStr.strip().split(';'):
                k, v = item.split('=', 1)
                self.cookies[k] = v
        self.search_key = 'web前端'
        self.dataList = []
        self.sid = ''
        self.pn = 1
        self.totalPage = 30
        self.first = 'true'
        self.url = 'https://www.lagou.com/jobs/list_' + self.search_key + '?labelWords=&fromSearch=true&suginput='
        self.headers = {"Connection": "keep-alive",
                        "Accept": "application/json, text/javascript, */*; q=0.01",
                        "X-Anit-Forge-Code": "0",
                        "X-Requested-With": "XMLHttpRequest",
                        "X-Anit-Forge-Token": "None",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "Origin": "https://www.lagou.com",
                        "Sec-Fetch-Site": "same-origin",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Dest": "empty",
                        "Referer": self.url,
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6",
                        'Pragma': 'no-cache',
                        'Cache-Control': 'no-cache'
                        }
        yield scrapy.Request(url=self.url, callback=self.parse, cookies=self.cookies,
                             dont_filter=True)

    def parse(self, response):
        # 第一次请求获取总页数和sid信息，第二页开始修改first,pn,sid等数据
        # ajax请求抓取数据
        self.Ajaxurl = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
        body = {
            'first': self.first,
            'pn': str(self.pn),
            'kd': self.search_key,
        }
        self.first = 'false'

        yield scrapy.FormRequest(url=self.Ajaxurl, headers=self.headers, formdata=body, cookies=self.cookies,
                                 callback=self.parsePage,
                                 method="POST")

    def parsePage(self, response):
        # 获取数据
        content = json.loads(response.text)
        data = content['content']['positionResult']['result']
        if (self.pn == 1):
            self.sid = content['content']['showId']
        logging.info('正在爬取' + str(self.pn) + '页的数据 ...')
        self.pn += 1
        for item in data:
            obj = LagouItem()
            obj['city'] = item['city'],
            obj['companySize'] = item['companySize'],
            obj['education'] = item['education']
            obj['skillLables'] = item['skillLables'],
            obj['workYear'] = item['workYear'],
            obj['salary'] = item['salary'],
            obj['companyShortName'] = item['companyShortName']
            yield obj

        # 递归爬取下一页
        if (self.totalPage >= self.pn):
            body = {
                'first': self.first,
                'pn': str(self.pn),
                'kd': self.search_key,
                'sid': self.sid
            }

            yield scrapy.FormRequest(url=self.Ajaxurl, headers=self.headers, formdata=body, cookies=self.cookies,
                                     callback=self.parsePage,
                                     method="POST")
