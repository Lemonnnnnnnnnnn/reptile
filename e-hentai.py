from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from download import dl

import json
import time


class Eh:
    def __init__(self):
        print('初始化')
        self.fileName = 'pic.txt'
        self.capa = DesiredCapabilities.EDGE
        self.capa["pageLoadStrategy"] = 'none'  # 懒加载模式
        self.driver = webdriver.Edge(capabilities=self.capa)
        self.isEnd = False
        self.length = -1
        self.dlService = dl()

        self.wait = WebDriverWait(self.driver, 10)
        url = 'https://e-hentai.org/s/d02a4dad50/1821771-1'
        self.driver.get(url)
        # self.pic = []

    def parse_page(self, num):
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//img[@id="img"]')))
            img = self.driver.find_element_by_xpath('//img[@id="img"]')
            self.dlService.direct(img.get_attribute('src'), num)
            # self.pic.append(img.get_attribute('src'))

        except TimeoutException:
            self.isEnd = True
        except NoSuchElementException:
            self.isEnd = True

    def turn_page(self):
        try:
            if (self.length == -1):
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="i2"]')))
                self.length = int(self.driver.find_element_by_xpath('//div[@class="sn"]/div/span[last()]').text)

            btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '//img[@src="https://ehgt.org/g/n.png"]')))

        except TimeoutException:
            self.isEnd = True
        except NoSuchElementException:
            self.isEnd = True
        else:
            btn.click()
            time.sleep(3)

    def crawl(self):
        num = 1
        while (not self.isEnd):
            print('正在爬取第 ' + str(num) + ' 页 ...')
            self.parse_page(num)
            self.turn_page()
            if self.length <= num: break
            num += 1

    def save(self):
        print('开始保存...')
        file = open(self.fileName, 'w')
        data = json.dumps(self.pic)
        file.write(data)
        file.close()

    def quit(self):
        self.driver.quit()


if __name__ == '__main__':
    obj = Eh()
    obj.crawl()
    # obj.save()
    obj.quit()
