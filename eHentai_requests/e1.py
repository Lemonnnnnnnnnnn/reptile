import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import parsel
import time
import re
from common import customRequest,proc_exist,remove_aria2
from aria2_download import a2D
import win32api
import constant


class CrawlOne:
    def __init__(self, start_url):
        self.threadPool = ThreadPoolExecutor(max_workers=5)
        self.start_url = start_url
        self.headers = {
            'User-Agent': constant.user_agent}
        self.proxies = {
            'http': constant.proxy,
            'https': constant.proxy,
        }
        self.End = False
        self.parseImg = 0
        self.down_path = constant.pic_download_url
        self.down_path_full = constant.pic_download_url

        self.dlServer = a2D()
        # 提前开启软件
        # if not proc_exist('IDMan.exe'):
        #     win32api.ShellExecute(0, 'open', r'C:\Program Files (x86)\Internet Download Manager\IDMan.exe', '', '', 1)
        #
        # if not proc_exist('aria2c.exe'):
        #     win32api.ShellExecute(0, 'open', r'D:\aria2\HideRun.vbs', '', '', 1)

        self.threads = []
        self.beginTime = time.time()

    def run(self):
        # 总共爬取几页
        self.parse_album_pageNum(self.start_url)

    def parse_album_pageNum(self, url):
        print('正在爬取相簿页数...')
        # 爬取相簿页数
        try:
            if (self.End == False):
                html = requests.get(url=url, headers=self.headers, proxies=self.proxies)
                sel = parsel.Selector(html.text)
                album_page_list_length = sel.xpath('//table[@class="ptt"]/tr/td[last()-1]/a/text()').get()
                for i in range(int(album_page_list_length)):
                    page_url = url + '?p=' + str(i)
                    self.parse_album(page_url)

        except Exception as e:
            print('访问相簿详情页失败')
            print(e)

    def parse_album(self, url):
        print('正在爬取相簿每一页所有的图片链接...')
        # 爬取相簿每一页所有的图片链接
        try:
            if (self.End == False):
                html = requests.get(url=url, headers=self.headers, proxies=self.proxies)
                sel = parsel.Selector(html.text)
                detail_list = sel.xpath('//div[@class="gdtm"]/div/a/@href').getall()

                page_message = sel.xpath('//p[@class="gpc"]/text()').get()
                begin_id = re.search(r'(\d+) - ', page_message).group(1)
                for i in range(len(detail_list)):
                    obj = self.threadPool.submit(self.parse_detail, detail_list[i], i + int(begin_id))
                    self.threads.append(obj)
        except Exception as e:
            print('访问相簿详情页失败')
            print(e)

    def parse_detail(self, url, id):
        try:
            # 爬取图片
            # print('正在爬取图片...')
            if (self.End == False):
                html = customRequest(url=url, headers=self.headers, proxies=self.proxies)
                sel = parsel.Selector(html.text)
                img_url = sel.xpath('//img[@id="img"]/@src').get()
                name = sel.xpath('//*[@id="i1"]/h1/text()').get()
                # 对文件和文件夹命名bai是不du能使用以下9个字符：/ \ : * " < > | ？
                name = re.sub(r'[/\\:*"<>|?]', '', name)

                if (img_url != 'https://ehgt.org/g/509.gif' and img_url != None):
                    self.parseImg += 1
                    # 存储图片链接
                    self.down_path_full = self.down_path + '\\' + name
                    self.dlServer.get_file_from_url(url=img_url, dir=self.down_path_full, file_name=str(id) + '.jpg')

                else:
                    print('已被限制')
                    self.End = True
        except Exception as e:
            print('访问图片页失败')
            print(e)

def run_crawler(start_url):
    print('开始爬虫...')
    obj = CrawlOne(start_url)
    obj.run()
    for future in as_completed(obj.threads):
        pass

    print('爬取完成')
    print('相簿爬取已完成，成功爬取了' + str(obj.parseImg) + '张图片')
    crawl_overtime = time.time()
    print('共耗时：' + str(crawl_overtime - obj.beginTime))
    print('开始校验...')
    obj.dlServer.verify()
    print('校验完成')
    print('移除出错的aria2文件...')
    remove_aria2(obj.down_path_full)
    print('完成！')


# if __name__ == '__main__':
#     start_url = 'https://e-hentai.org/g/1841464/3c43b8b6b0/'
#     run_crawler(start_url)
