import json
import os
from dataBase import database
import random
import requests
import time


class dl:
    def __init__(self):
        print('开始下载...')
        if (not os.path.exists('pic')):
            os.makedirs('pic')

    def execute(self, url, num):
        # 从数据库里取出IP地址
        db = database()
        IPArr = db.search()
        tryTimes = 3  # 重试的次数
        img = ''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'}

        # sleepTime = random.randint(1, 5)
        # print('正在休眠...')
        # time.sleep(sleepTime)

        print('正在下载第 ' + str(num) + ' 张图片...')

        for i in range(tryTimes):
            try:
                print('正在进行第 ' + str(i + 1) + ' 次尝试' )
                proxy_ip = {'http': random.choice(IPArr)}
                print(proxy_ip)
                img = requests.get(url, headers=headers, proxies=proxy_ip, timeout=10).content
                break

            except Exception as e:
                print(e)

        if img != '':
            with open('./pic/' + str(num) + '.jpg', 'wb') as f:
                f.write(img)


    def file(self):
        file = open('pic.txt', 'r')
        data = json.load(file)
        num = 0
        for item in data:
            num += 1
            self.execute(item, num)

    def direct(self, url, num):
        self.execute(url, num)

# if (__name__ == '__main__'):
#     download()
