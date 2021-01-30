import requests
import parsel
import threading

url = 'http://e-hentai.org/s/0f277011ef/1832332-1'


class ipJudge:
    def __init__(self):
        self.httpList = []
        self.socks4List = []
        self.socks5List = []

    def judge(self, start_num, end_num, type):
        if (type == 'http'):
            file = open('out/http.txt', 'r', encoding='utf-8')
        if (type == 'socks4'):
            file = open('out/socks4.txt', 'r', encoding='utf-8')
        if (type == 'socks5'):
            file = open('out/socks5.txt', 'r', encoding='utf-8')

        for line in file.readlines()[start_num:end_num]:
            for i in range(2):
                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
                proxy = {}
                if (type == 'http'):
                    proxy = {
                        'http': type + '://' + line
                    }
                if (type == 'socks4' or type == 'socks5'):
                    proxy = {
                        'http': type + '://' + line,
                        'https': type + '://' + line,
                    }

                try:
                    html = requests.get(url=url, proxies=proxy, headers=headers, timeout=10)
                    sel = parsel.Selector(html.text)
                    img = sel.xpath('//img[@id="img"]/@src').get()
                    if (img != 'https://ehgt.org/g/509.gif' and img != None):
                        print(line + '成功！')
                        if (type == 'http'):
                            self.httpList.append(line)
                        if (type == 'socks4'):
                            self.socks4List.append(line)
                        if (type == 'socks5'):
                            self.socks5List.append(line)

                    break
                except Exception as e:
                    print(e)
                    print(line + '失败...')
                    continue

    def save(self, type):
        with open('out/' + type + '_proxy.txt', 'a+') as f:
            if (type == 'http'):
                for i in self.httpList:
                    f.write(i)
            if (type == 'socks4'):
                for i in self.socks4List:
                    f.write(i)
            if (type == 'socks5'):
                for i in self.socks5List:
                    f.write(i)

    #     :param all_num: 要采集的总页数
    #     :param thread_num: 要开启的线程数

    def thread(self, all_num, thread_num, type):
        per_num = int(all_num / thread_num)  # 每个线程处理的任务数量
        threads = []  # 开启的线程放到一个列表

        for i in range(thread_num):
            t = threading.Thread(target=self.judge, args=(i * per_num, i * per_num + per_num, type))
            threads.append(t)

        # 开启守护线程，目的是使后面的save函数在线程执行结束后再执行
        # setDaemon表示 主线程执行完毕并且没有任何非守护线程继续运行时，主线程可以正常终止退出了。
        for t in threads:
            t.setDaemon(True)
            t.start()
        #
        for t in threads:
            t.join()

        print('程序执行完毕!')
        self.save(type)
