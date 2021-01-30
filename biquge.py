import requests
import parsel
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class crawl:
    def __init__(self):
        # 200 10.19
        # 1000 8.45
        # 100 10.95
        # 500 9.5
        # 2000 8.4
        # 50  17.71
        # 默认  51.47
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
        self.down_path = r'D:\Download\我有一座冒险屋'
        self.start_url = 'https://www.biquge.com.cn/book/33556/'
        self.threadPool = ThreadPoolExecutor(max_workers=1000)
        self.threads = []
        self.beginTime = time.time()

    def parse(self):
        html = requests.get(url=self.start_url, headers=self.headers)
        sel = parsel.Selector(html.text)
        list = sel.xpath('//div[@id="list"]/dl/dd/a/@href').getall()
        for item in list:
            id = item.rsplit('/', 1)[1]
            url = self.start_url + id
            obj = self.threadPool.submit(self.parse_page, url)
            self.threads.append(obj)

    def parse_page(self, url):
        html = requests.get(url=url, headers=self.headers)
        sel = parsel.Selector(html.text)
        title = sel.xpath('//h1/text()').get()
        content = sel.xpath('//div[@id="content"]/text()').getall()
        path = self.down_path + '\\' + title + '.txt'
        with open(path, 'w', encoding='utf-8')as f:
            for i in content:
                f.write(i + '\n')


if __name__ == '__main__':
    obj = crawl()
    obj.parse()
    for future in as_completed(obj.threads):
        pass
    print('爬取完成')
    crawl_overtime = time.time()
    print('共耗时：' + str(crawl_overtime - obj.beginTime))
