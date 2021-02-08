import requests
from concurrent.futures import as_completed
import parsel
import time
from e1 import CrawlOne
from common import proc_exist
import win32api
import constant

class Crawl:
    def __init__(self):
        self.start_url = constant.crawl_custom
        self.headers = {
            'User-Agent': constant.user_agent}
        self.proxies = {
            'http': constant.proxy,
            'https': constant.proxy,
        }
        self.End = False
        self.parseImgTotal = 0
        # 提前开启软件
        if not proc_exist(constant.idm_name):
            win32api.ShellExecute(0, 'open', constant.idm_path, '', '', 1)

        if not proc_exist(constant.aria2_name):
            win32api.ShellExecute(0, 'open', constant.aria2_path, '', '', 1)

        self.beginTime = time.time()

    def run(self, total_parse_num=1):
        # 总共爬取几页
        print('开始运行...')
        for i in range(total_parse_num):
            print('正在爬取第' + str(i + 1) + '页')
            self.parse_page_list(i)

    def parse_page_list(self, page_num):
        print('正在爬取每一个的相簿链接...')
        # 爬取每一个的相簿链接
        try:
            if (self.End == False):
                url = self.start_url + '&page=' + str(page_num)

                html = requests.get(url=url, headers=self.headers, proxies=self.proxies)
                sel = parsel.Selector(html.text)
                album_list = sel.xpath('//td[@class="gl3c glname"]/a/@href').getall()
                for item in album_list:
                    subCrawler = CrawlOne(item)
                    subCrawler.run()
                    for future in as_completed(subCrawler.threads):
                        pass
                    if (subCrawler.End):
                        self.End = True
                        print('已被限制...')

                    print('爬取完成')
                    print('相簿爬取已完成，成功爬取了' + str(subCrawler.parseImg) + '张图片')
                    self.parseImgTotal += subCrawler.parseImg
                    crawl_overtime = time.time()
                    print('耗时：' + str(crawl_overtime - subCrawler.beginTime))
                    print('开始校验...')
                    subCrawler.dlServer.verify()
                    print('校验完成')

        except Exception as e:
            print('访问home页面失败')
            print(e)


if __name__ == '__main__':
    obj = Crawl()
    obj.run()

    print('总爬取完成')
    print('总成功爬取了' + str(obj.parseImgTotal) + '张图片')
    overtime = time.time()
    print('总爬取共耗时：' + str(overtime - obj.beginTime))
