import xmlrpc.client
from pyaria2 import Aria2RPC
import os


class aria2DL:

    def get_file_from_url(self, url, file_name, dir):
        try:
            jsonrpc = Aria2RPC()
            options = {"dir": dir, "out": file_name}
            jsonrpc.addUri([url], options=options)
        except Exception as e:
            print('下载出错！')
            print(e)

    def downloadAll(self):
        pass

# if __name__ == '__main__':
#     obj = aria2DL()
#     obj.get_file_from_url(
#         'https://oimagec3.ydstatic.com/image?id=8736622467468200472&product=adpublish&format=JPEG&w=520&h=347',
#         '123.png')
