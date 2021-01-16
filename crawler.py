import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from dataBase import database
import requests


class crawler:
    def __init__(self):
        print('初始化')
        # self.capa = DesiredCapabilities.CHROME
        opt = webdriver.ChromeOptions()
        # self.capa["pageLoadStrategy"] = 'none'  # 懒加载模式
        desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        desired_capabilities['pageLoadStrategy'] = 'none'

        self.driver = webdriver.Chrome(options=opt, desired_capabilities=desired_capabilities)
        self.isEnd = False
        self.wait = WebDriverWait(self.driver, 10)
        self.data = []
        self.finalData = []

    def judge(self):
        print('开始校验...')
        # # 检测可用性
        for i in range(len(self.data)):
            address = self.data[i]['address']
            port = self.data[i]['port']
            type = self.data[i]['type']
            try:
                proxies = {
                    type: type + "://" + address + ":" + port
                }
                print('正在检测...')
                requests.get('http://www.baidu.com', proxies=proxies)
            except Exception as e:
                print(e)
                continue
            else:
                self.finalData.append(self.data[i])
                print('success')

    def parse_jiangxianli(self):
        url = 'https://ip.jiangxianli.com/'
        self.driver.get(url)
        try:
            address = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr')))
            for item in address:
                address = item.find_element_by_xpath('.//td[1]').text
                type = item.find_element_by_xpath('.//td[4]').text
                port = item.find_element_by_xpath('.//td[2]').text
                lastTime = item.find_element_by_xpath('.//td[last()-1]').text

                self.data.append({
                    'address': address,
                    'port': port,
                    'lastTime': lastTime,
                    'type': type
                })

        except Exception as e:
            print(e)
            self.isEnd = True

    def parse_xiaoHuan(self):
        url = 'https://ip.ihuan.me/'
        self.driver.get(url)
        try:
            address = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr')))
            for item in address:
                address = item.find_element_by_xpath('.//td[1]').text
                if (item.find_element_by_xpath('.//td[5]').text == '不支持'):
                    type = 'http'
                else:
                    type = 'https'

                port = item.find_element_by_xpath('.//td[2]').text
                lastTime = item.find_element_by_xpath('.//td[last()]').text

                self.data.append({
                    'address': address,
                    'port': port,
                    'lastTime': lastTime,
                    'type': type
                })

        except Exception as e:
            print(e)
            self.isEnd = True

    def save(self):
        db = database()
        db.insert_multiple(self.finalData)
        db.close()
        pass

    def quit(self):
        self.driver.quit()


if __name__ == '__main__':
    obj = crawler()
    obj.parse_jiangxianli()
    # obj.parse_xiaoHuan()
    obj.quit()
    obj.judge()
    obj.save()
