import requests
import parsel
import time
# from common import proc_exist
# import win32api
import pymongo
from subprocess import call
import os
import shutil
import constant


class Crawl:
    def __init__(self):
        self.start_url = constant.crawl_start_url
        self.headers = {
            'User-Agent': constant.user_agent}
        self.proxies = {
            'http': constant.proxy,
            'https': constant.proxy,
        }
        self.End = False
        # 提前开启软件
        self.num = 0
        self.beginTime = time.time()
        self.client = pymongo.MongoClient(constant.mongodb_path)
        self.db = self.client[constant.mongodb_db_name]
        self.item_name = constant.mongodb_collection_name
        self.db[self.item_name].drop()
        # 不同的请求链接html结构不一样，暂时只适配了chinese请求
        self.b = 'c'

        # if not proc_exist('IDMan.exe'):
        #     win32api.ShellExecute(0, 'open', r'C:\Program Files (x86)\Internet Download Manager\IDMan.exe', '', '', 1)

        self.down_path = constant.face_download_url
        if (os.path.exists(self.down_path)):
            shutil.rmtree(self.down_path)
            os.mkdir(self.down_path)
        else:
            os.mkdir(self.down_path)

        self.IDM = constant.idm_path

    def run(self, total_parse_num=1):
        # 总共爬取几页
        print('开始运行...')
        for i in range(total_parse_num):
            print('正在爬取第' + str(i + 1) + '页')
            self.parse_page_list(i)

    def parse_page_list(self, page_num):
        print('正在爬取每一个的封面链接...')
        # 爬取每一个的相簿链接
        try:
            if (self.End == False):
                url = self.start_url + '&page=' + str(page_num)

                html = requests.get(url=url, headers=self.headers, proxies=self.proxies)
                sel = parsel.Selector(html.text)
                album_list = sel.xpath('//table[@class="itg glt' + self.b + '"]//tr')

                for item in album_list:
                    face_ele = item.xpath('.//td[@class="gl2' + self.b + '"]/div[@class="glthumb"]/div/img')
                    link_url = item.xpath('.//td[@class="gl3' + self.b + ' glname"]/a/@href').getall()
                    album_name = item.xpath('.//td[@class="gl3c glname"]/a/div/text()').getall()
                    self.num += 1

                    if (face_ele.get() != None):
                        if (face_ele.xpath('.//@data-src')):
                            face_url = face_ele.xpath('.//@data-src').get()
                            # 存储图片链接
                            call([self.IDM, '/d', face_url, '/p', self.down_path, '/f', str(self.num) + '.jpg', '/a',
                                  '/n'])
                            self.db[self.item_name].insert_one(
                                {'link_url': link_url, 'face_url': './public/' + str(self.num) + '.jpg',
                                 'name': album_name})
                        else:
                            face_url = face_ele.xpath('.//@src').get()
                            # 存储图片链接
                            call([self.IDM, '/d', face_url, '/p', self.down_path, '/f', str(self.num) + '.jpg', '/a',
                                  '/n'])
                            self.db[self.item_name].insert_one(
                                {'link_url': link_url, 'face_url': './public/' + str(self.num) + '.jpg',
                                 'name': album_name})


        except Exception as e:
            print('访问home页面失败')
            print(e)


if __name__ == '__main__':
    obj = Crawl()
    obj.run()
    call([obj.IDM, '/s'])

    print('总爬取完成')
    overtime = time.time()
    print('总爬取共耗时：' + str(overtime - obj.beginTime))
