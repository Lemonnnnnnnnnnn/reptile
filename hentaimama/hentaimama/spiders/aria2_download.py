import xmlrpc.client

class aria2DL:
    def __init__(self):
        self.server = xmlrpc.client.ServerProxy('http://173.82.197.174:6800/rpc')  # 连接RPC服务器
        self.download_path = '/var/www/d'

    def downloadOne(self,url,fileName):
        try :
            self.server.aria2.addUri("token:d379a277dc507c31f0ac", [url], {"out": fileName, "dir": self.download_path})  # 添加下载链接
        except Exception as e:
            print(e)



    def downloadAll(self):
        pass


if __name__ == '__main__':
    obj = aria2DL()
    obj.downloadOne('https://oimagec3.ydstatic.com/image?id=8736622467468200472&product=adpublish&format=JPEG&w=520&h=347','123.png')


