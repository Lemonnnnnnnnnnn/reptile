from pyaria2 import Aria2RPC
import time
from subprocess import call
import constant
import win32api
from common import proc_exist

class a2D:
    def __init__(self):
        self.server = Aria2RPC()
        self.downloadList = []
        self.IDM = constant.idm_path
        self.down_path = constant.video_download_url
        self.download_fail = 0
        if not proc_exist(constant.idm_name):
            win32api.ShellExecute(0, 'open', constant.idm_path, '', '', 1)

        if not proc_exist(constant.aria2_name):
            win32api.ShellExecute(0, 'open', constant.aria2_path, '', '', 1)

    def get_file_from_url(self, url, dir, file_name=''):
        try:
            print('正在下载...')
            if (file_name):
                options = {"dir": dir, "out": file_name}
            else:
                options = {"dir": dir}
            gid = self.server.addUri([url], options=options)
            self.downloadList.append(gid)
        except Exception as e:
            print('下载出错！')
            if (file_name):
                call([self.IDM, '/d', url, '/p', dir, '/f', file_name, '/a', '/n'])
            else:
                call([self.IDM, '/d', url, '/p', dir, '/a', '/n'])

            self.download_fail += 1
            print(e)

    def getStatus(self, gid):
        status = self.server.tellStatus(gid=gid)['status']
        if (status != 'complete'):
            return False
        return True

    def verify(self):
        # 60秒下载超时
        print('等待60秒...')
        time.sleep(60)

        for i in self.downloadList:
            if (not self.getStatus(i)):
                info = self.server.getFiles(i)[0]
                path = info['path']
                dir_path, file_name = path.rsplit('/', 1)
                url = info['uris'][0]['uri']
                call([self.IDM, '/d', url, '/p', dir_path, '/f', file_name, '/a', '/n'])
                self.download_fail += 1

        if (self.download_fail):
            print('使用idm再次尝试下载...')
            call([self.IDM, '/s'])
