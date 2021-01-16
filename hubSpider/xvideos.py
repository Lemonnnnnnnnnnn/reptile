import logging
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
from aria2_download import aria2DL
import time


class xvideosSpider():
    def __init__(self):
        self.cookiesDic = {}
        self.parseNum = 0
        self.videoList = []
        for line in open('cookie.txt', 'r'):
            k = re.search(r'(.*?)=(.+)', line).group(1)
            v = re.search(r'(.*?)=(.+)', line).group(2)
            self.cookiesDic[k] = v

        self.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        self.beginUrl = 'https://www.xvideos.com/?k=123'

        opts = webdriver.ChromeOptions()
        opts.add_argument('--headless')
        opts.add_argument('user-agent=' + self.userAgent)
        opts.add_argument('--disable-gpu')
        # 不加载图片
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2,
            }
        }
        opts.add_experimental_option('prefs', prefs)
        # capa = DesiredCapabilities.CHROME
        # capa["pageLoadStrategy"] = 'none'  # 懒加载模式

        self.driver = webdriver.Chrome(options=opts)
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.get(self.beginUrl)
        self.driver.delete_all_cookies()
        try:
            for key in self.cookiesDic:
                self.driver.add_cookie({'name': key, 'value': self.cookiesDic[key]})
        except Exception as e:
            logging.error('添加cookies失败！')
            logging.error(e)

        self.driver.get(self.beginUrl)
        self.next_list = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="thumb"]/a')))
        self.next_list_url = []
        for item in self.next_list:
            self.next_list_url.append(item.get_attribute('href'))

        self.parseNumTotal = len(self.next_list)

    def clickDownloadBtn(self):
        try:
            downloadBtn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="video-actions"]/ul/li[2]/a')))
        except Exception as e:
            logging.error(e)
        else:
            downloadBtn.click()

    def saveDownloadUrl(self):
        name = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="hlsplayer"]/div[2]/p'))).text
        downloadUrl = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="tabDownload"]/p/a[1]'))).get_attribute('href')
        self.videoList.append({'name': name, 'downloadUrl': downloadUrl})

    def parseDetail(self):
        try:
            # 进入页面
            next_url = self.next_list_url[self.parseNum]
            self.driver.get(next_url)
            # 进行爬取
            self.clickDownloadBtn()
            self.saveDownloadUrl()
            self.parseNum += 1
            self.driver.back()
        except Exception as e:
            print('第 ' + str(self.parseNum + 1) + ' 个视频爬取失败，跳过...')
            self.parseNum += 1
            print(e)

    def crawl(self):
        while (self.parseNumTotal > self.parseNum + 1):
            print('正在爬取第 ' + str(self.parseNum + 1) + '个视频... , 总共' + str(self.parseNumTotal) + '个')
            self.parseDetail()

    def save(self):
        with open('download_url.txt', 'a+', encoding='utf-8') as f:
            json.dump(self.videoList, f)

    def download(self):
        dl = aria2DL()
        with open('download_url.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            mediaArr = json.loads(content)
            print('正在下载，请等待...')
            for item in mediaArr:
                dl.downloadOne(url=item['downloadUrl'], fileName=item['name'])

    def quit(self):
        self.driver.quit()


if __name__ == '__main__':
    spider = xvideosSpider()
    spider.crawl()
    spider.save()
    # spider.download()
    spider.quit()
