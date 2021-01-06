from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import os

import urllib
import time
import xlwt
import re


class douban:
    # 初始化
    def init(self):
        self.browser = webdriver.Edge()
        self.wait = WebDriverWait(self.browser, 10)
        self.browser.get('https://movie.douban.com/top250')
        self.isEnd = False
        self.workbook = xlwt.Workbook(encoding='utf-8')
        self.worksheet = self.workbook.add_sheet('Sheet1')

        self.title = []
        self.director = []
        self.actor = []
        self.date = []
        self.country = []
        self.genre = []
        self.star = []
        self.rateNum = []
        self.dict = [
            {'column': 0, 'title': '排名', 'link': list(range(1, 250 + 1))},
            {'column': 1, 'title': '标题', 'link': self.title},
            {'column': 2, 'title': '导演', 'link': self.director},
            {'column': 3, 'title': '主演', 'link': self.actor},
            {'column': 4, 'title': '上映时间', 'link': self.date},
            {'column': 5, 'title': '上映国家', 'link': self.country},
            {'column': 6, 'title': '类型', 'link': self.genre},
            {'column': 7, 'title': '评分', 'link': self.star},
            {'column': 8, 'title': '评分人数', 'link': self.rateNum},
        ]
        for item in self.dict:
            self.worksheet.write(0, item['column'], item['title'])

    # 爬取网页数据
    def parse_page(self):
        try:
            title = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a/span[@class="title"][1]')))
            for item in title:
                self.title.append(item.text)

            self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="bd"]/p[@class=""]')))
            # info包含 导演、主演、上映时间、上映地点、影片类型等五个信息
            info = self.browser.find_elements_by_xpath('//div[@class="bd"]/p[@class=""]')

            reDirector1 = re.compile(r'导演:(.+)主演')
            reDirector2 = re.compile(r'导演:(.+)\s?')
            for item in info:
                message = re.split(r'\n', item.text)
                # self.director.append(re.search(r'导演:(.*?)\s{2}', message[0]).group(1))
                # 匹配导演（导演+主演 或 只有导演）
                if (re.search(reDirector1, message[0])):
                    self.director.append(re.search(reDirector1, message[0]).group(1))
                else:
                    self.director.append(re.search(reDirector2, message[0]).group(1))

                # 匹配主演（有或没有）
                if (re.search(r'主演:(.+)?', message[0])):
                    self.actor.append(re.search(r'主演:(.+)?', message[0]).group(1))
                else:
                    self.actor.append('')

                # message[-1]为第二行内容，包含上映时间、上映地点、影片类型等三种信息，根据 / 将第二行信息切割成数组message_minor
                message_minor = re.split('/', message[-1])

                # 第一位到倒数第三位为上映时间
                dateStr = ''
                for i in message_minor[:-2]:
                    dateStr += i
                self.date.append(dateStr)
                # 倒数第二位为国家
                self.country.append(message_minor[-2])
                # 倒数第一位为类型
                self.genre.append(message_minor[-1])

            # 评分
            star = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="star"]/span[@class="rating_num"]')))
            for item in star:
                self.star.append(item.text or '')
            # 评价人数
            rateNum = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="star"]/span[last()]')))
            for item in rateNum:
                self.rateNum.append(item.text or '')



        except TimeoutException:
            self.isEnd = True
        except NoSuchElementException:
            self.isEnd = True

    # 进行翻页操作
    def turn_page(self):
        try:
            turnButton = self.browser.find_element_by_xpath('//span[@class="next"]/a')
        except TimeoutException:
            self.isEnd = True
        except NoSuchElementException:
            self.isEnd = True
        else:
            turnButton.click()
            time.sleep(1)

    # 爬取数据，调用 parse_page 和 turn_page
    def crawl(self):
        num = 0
        while (not self.isEnd):
            num += 1
            print('正在爬取第 ' + str(num) + ' 页 ...')
            self.parse_page()
            self.turn_page()

    # 保存数据，将数据保存到文件中
    def save(self):
        pass

    # 数据可视化
    def draw(self):
        pass

    def quit(self):
        self.browser.quit()


        for item in self.dict:
            for value in range(len(item['link'])):
                self.worksheet.write(value + 1, item['column'], item['link'][value])

        if os.path.exists("豆瓣250.xls"):
            os.remove("豆瓣250.xls")

        self.workbook.save('豆瓣250.xls')


if __name__ == '__main__':
    obj = douban()
    obj.init()
    obj.crawl()
    obj.save()
    obj.draw()
    obj.quit()
