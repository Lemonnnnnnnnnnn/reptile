from e1 import run_crawler
import threading
import  time
import win32api
from common import proc_exist
import constant

def bbb(url):
    time.sleep(2)
    print(url)

def syncProcess():
    if not proc_exist(constant.idm_name):
        win32api.ShellExecute(0, 'open', constant.idm_path, '', '', 1)

    if not proc_exist(constant.aria2_name):
        win32api.ShellExecute(0, 'open', constant.aria2_path, '', '', 1)

    process = True
    while (process):
        url = input('\n请输入要爬取的页面，结束请输入over：\n')
        if (url != 'over'):
            t = threading.Thread(target=run_crawler, args=(url,))
            t.start()
            # t.join()
        else:
            process = False


if __name__ == '__main__':
    syncProcess()
