import requests


class ezCrawler:
    def __init__(self):
        self.httpUrl = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all'
        self.socks5Url = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all'
        self.socks4Url = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
        self.proxies = {
            'http': 'http://localhost:7890',
            'https': 'http://localhost:7890'
        }

    def httpCrawl(self):
        res = requests.get(url=self.httpUrl, headers=self.headers, proxies=self.proxies)
        with open('out/http.txt', 'a+') as f:
            list = res.text.split('\n')
            for i in list:
                f.write(i)

    def socks5Crawl(self):
        res = requests.get(self.socks5Url, headers=self.headers, proxies=self.proxies)
        with open('out/socks5.txt', 'a+') as f:
            list = res.text.split('\n')
            for i in list:
                f.write(i)

    def socks4Crawl(self):
        res = requests.get(self.socks4Url, headers=self.headers, proxies=self.proxies)
        with open('out/socks4.txt', 'a+') as f:
            list = res.text.split('\n')
            for i in list:
                f.write(i)

#
# if __name__ == '__main__':
#     obj = ezCrawler()
#     obj.httpCrawl()
