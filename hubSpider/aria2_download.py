import xmlrpc.client

class aria2DL:
    def __init__(self):
        self.server = xmlrpc.client.ServerProxy('http://173.82.197.174:6800/rpc')  # 连接RPC服务器
        self.download_path = '/usr/share/nginx/html/download'

    def downloadOne(self,url,fileName):
        try :
            self.server.aria2.addUri("token:abc839986", [url], {"out": fileName, "dir": self.download_path})  # 添加下载链接
        except Exception as e:
            print(e)



    def downloadAll(self):
        pass





