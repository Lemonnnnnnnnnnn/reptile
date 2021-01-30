from pyaria2 import Aria2RPC
import time
from subprocess import call


class a2D:
    def __init__(self):
        self.server = Aria2RPC()
        self.downloadList = []
        self.IDM = "C:\Program Files (x86)\Internet Download Manager\IDMan.exe"
        self.down_path = r'D:\18x\pic'
        self.download_fail = 0


    def get_file_from_url(self, url, file_name, dir):
        try:
            options = {"dir": dir, "out": file_name}
            gid = self.server.addUri([url], options=options)
            self.downloadList.append(gid)
        except Exception as e:
            print('下载出错！')
            call([self.IDM, '/d', url, '/p', dir, '/f', file_name, '/a', '/n'])
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
