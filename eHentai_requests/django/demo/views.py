path = r'D:\technology\python\reptile\eHentai_requests'
import sys

sys.path.append(path)

from django.shortcuts import HttpResponse
import pymongo
import json
from catch_face import Crawl
from common import proc_exist
import constant
from subprocess import call
import time
import win32api

if not proc_exist(constant.idm_name):
    win32api.ShellExecute(0, 'open', constant.idm_path, '', '', 1)

obj = Crawl()
obj.run(constant.crawl_num)
call([obj.IDM, '/s'])

print('总爬取完成')
overtime = time.time()
print('总爬取共耗时：' + str(overtime - obj.beginTime))

client = pymongo.MongoClient(constant.mongodb_path)
db = client[constant.mongodb_db_name]
col = db[constant.mongodb_collection_name]
list = []
for i in col.find():
    list.append({'link_url': i['link_url'], 'face_url': i['face_url']})


def hello(request):
    return HttpResponse(json.dumps(list), content_type='application/json')
