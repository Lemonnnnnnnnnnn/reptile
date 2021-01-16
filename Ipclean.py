from dataBase import database
import requests

db = database()
IPArr = db.search()
for item in IPArr:
    try:
        print(item)
        proxies = {
            'http': item
        }
        print('正在检测...')
        aaa =requests.get('https://www.lagou.com/', proxies=proxies)
    except Exception as e:
        print(e)
        continue
    else:
        print('success')

# db.removeAll()
