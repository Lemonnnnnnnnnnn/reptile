import requests
import win32com.client
import os
import re
import json
import random
import constant


def random_chose_node():
    print('随机选择节点...')
    name = random.choice(constant.clash_name_list)
    data = json.dumps({'name': name})
    url = constant.clash_url
    requests.put(url, data=data, params=data)


def customRequest(url, headers=None, proxies=None):
    for i in range(3):
        try:
            return requests.get(url, headers=headers, proxies=proxies)
        except Exception as e:
            print(e)


def proc_exist(process_name):
    is_exist = False
    wmi = win32com.client.GetObject('winmgmts:')
    processCodeCov = wmi.ExecQuery('select * from Win32_Process where name=\"%s\"' % (process_name))
    if len(processCodeCov) > 0:
        is_exist = True
    return is_exist


def remove_aria2(path):
    for i in os.listdir(path):
        if (re.search(r'\.aria2', i)):
            wait_remove = re.search(r'.*\.aria2', i).group()
            os.remove(path + '\\' + wait_remove)
