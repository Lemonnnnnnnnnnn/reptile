import scrapy
import re
import requests
import logging
import json


class XvideoSpider(scrapy.Spider):
    name = 'xvideo'
    allowed_domains = ['xvideos.com']

    def start_requests(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        }
        self.cookies = {}
        for line in open('D:\python\\reptile\\xvideos\\xvideos\cookie.txt', 'r'):
            k = re.search(r'(.*?)=(.+)', line).group(1)
            v = re.search(r'(.*?)=(.+)', line).group(2)
            self.cookies[k] = v
        self.beginUrl = 'https://www.xvideos.com'
        yield scrapy.Request(url=self.beginUrl, headers=self.headers, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        url_list = response.xpath('//div[@class="thumb"]/a/@href').getall()
        for i in url_list:
            url = response.urljoin(i)
            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, callback=self.detailParse)

    def detailParse(self, response):
        videoID = re.search(r'/video(.+)/', response.url).group(1)
        requestUrl = self.beginUrl + '/video-download/' + videoID + '/'
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': self.beginUrl,
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': response.url,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
            # cookie只需要添加一次 不用重复添加
            # 'Cookie': 'wpn_ad_cookie=43db2801de42d877dba0084ac644441a; html5_pref=%7B%22SQ%22%3Afalse%2C%22MUTE%22%3Afalse%2C%22VOLUME%22%3A0.14444435967339408%2C%22FORCENOPICTURE%22%3Afalse%2C%22FORCENOAUTOBUFFER%22%3Afalse%2C%22FORCENATIVEHLS%22%3Afalse%2C%22PLAUTOPLAY%22%3Atrue%2C%22CHROMECAST%22%3Afalse%2C%22EXPANDED%22%3Afalse%2C%22FORCENOLOOP%22%3Afalse%7D; chat_data_c=%7B%22ct%22%3A%22EbGlXeXySyCn%2Byghwx9Qg318xv8QfYjlS9mr95EUwTkD%5C%2FExzOD9dJzSzWylj5sZaGCAOL2oe5NLrNBDt6VaMNHUPX1L41kYLD9Xl942uibXpx%2BQTDk%2BtIm%2BuuCxeVojbrlWWtGLPRyaN2aRwZb3qyLSlqt5UaSnyQA7yK%2BdFgwMOPvp84z%2Bw%5C%2FqXWIzm%5C%2FMl0Mk8XbwytlRLrrEnEyE%5C%2FGM0kMaA1qU5VVCWav2B1izC%2Bvba25k6xdyjCEAugzBGtsrImOS9Wi679feP32gOLwIsZbU263wk%2BUWFxn5xxQxofezwHjv63EdHuzNZuB%5C%2Fore2s5FGbKz2Xn0Lk2Uenudve3rfRXBWXOZzKG7eXEvpwfDlzR0Pno2kgs%2BYjDU6B2NLdDAzuymOdj4MO%2Bwdiecd4WWLv0ied%5C%2FeVnNGop7n4mX5VVftIzzOePgZa%5C%2FRr9W8qVHrw0yV9mdyuhPup3KPo0EoBQJKWVmQjJGVcPjIj4Vkk%2By7I0DIGc8IxNkqR7gUtXRIgdfvJIy%2BQx65RjGFueSPQbvx7w%5C%2F2goHAB5a2VLjPO6jY0Mp8jQin51Y1PP5%5C%2FTxHv5suSaA9l6OhOQrCSnLJ9EM7c%2BaX4UMBkku%2B6rxYZnmIUnX33FXc8i03Exdg9bOwxZZUWqzcSADxWXPc3ylmtMS%2Bx85QW%5C%2FUvJQxhIbX5B5QB1WLaPCTBvrUlQgAx%2B8Sy4T0YWTpUrnPS0oO%5C%2FE9HXsxTDrsQQTZeqJ9aW5xiAYbN8sgPN6Pxg8LK3%5C%2FeanRPRMYC2vkKuGupNRlH0ksMMy7T5hjxZhN5153UdWB2raasj5149E2Nx%5C%2F1Uu%5C%2FWNe%5C%2FWKLtkZxauzx7YlyC8GAWcYOpAFrNGVRxjA7e96ypbc317Bs4hmrXKQxnCEBZ5su0M1TrKGcQBjnAakpXLtcZMvIncyGQn9fhSVfZmuwhX5NC7LdKGOWRVpIWtSYbDK6TdSf9rKIhrLSZfG%5C%2FdGDorAhFpXiB%2BQ4uenVwU9G6bll4TV%5C%2FzbG5ZH9nsQ%2BpJL6Ua2rqnNFaxnyCguoih8hHHMurhhtWiQoCDBM3P3G4d%2BkWvzay0DXGGzJOkoe7XiVc7tgr52JH7QdFkr4AfwL9KyaAMxqlmXxEs37N4QzE5UVEoxBNyicILPlJA%5C%2FARH6vWh9c2qRx3%5C%2Fgu4oVh53hyOIiiwnG2mscjzanlNhm7zl2kjs9MzUG3FI0kIrBvYCEs8%5C%2FusCjIyslrvK%5C%2FK34N4Xp3oYkQbWhiyofQxSAEdio3DApYb%2BS5sg4xqS7jfOuP4Z8YUdkL%22%2C%22iv%22%3A%22d59cb826d82dfd91a33ad577919a719e%22%2C%22s%22%3A%228b2df4082257a8aa%22%7D; xv_nbview=-1; html5_networkspeed=5466; X-Backend=11|YAMEj|YAMEj; thumbloadstats_vthumbs=%7B%222%22%3A%5B%7B%22s%22%3A2%2C%22d%22%3A970%7D%2C%7B%22s%22%3A1%2C%22d%22%3A117%7D%2C%7B%22s%22%3A1%2C%22d%22%3A4212%7D%5D%2C%223%22%3A%5B%7B%22s%22%3A2%2C%22d%22%3A132%7D%2C%7B%22s%22%3A1%2C%22d%22%3A35%7D%2C%7B%22s%22%3A1%2C%22d%22%3A5821%7D%5D%2C%2210%22%3A%5B%7B%22s%22%3A2%2C%22d%22%3A400%7D%2C%7B%22s%22%3A1%2C%22d%22%3A39%7D%2C%7B%22s%22%3A1%2C%22d%22%3A4178%7D%5D%2C%22last%22%3A%7B%22s%22%3A1%2C%22v%22%3A%5B4212%2C5821%2C4178%5D%7D%7D; hexavid_lastsubscheck=1; last_views=%5B%2260269407-1610545022%22%2C%2260436229-1610587821%22%2C%2251978347-1610587826%22%2C%2227011125-1610587853%22%2C%2260373221-1610588152%22%2C%2260399581-1610590429%22%2C%2247939005-1610593964%22%2C%2238730821-1610594551%22%2C%2234143803-1610594605%22%2C%2231669337-1610594753%22%2C%2230831479-1610595655%22%2C%2216441155-1610596155%22%2C%2259636249-1610596190%22%2C%2259637483-1610596224%22%2C%2212836177-1610596249%22%2C%2210481560-1610596330%22%2C%227192860-1610596508%22%2C%221564089-1610596555%22%2C%2260031851-1610596820%22%2C%2259750567-1610597009%22%2C%2258762607-1610597169%22%2C%2252341865-1610597301%22%2C%2260448221-1610711674%22%2C%2260456915-1610716661%22%2C%223536305-1610717361%22%2C%2256547859-1610719324%22%2C%2260403171-1610765168%22%2C%2214454513-1610769666%22%2C%2260480577-1610807989%22%2C%2256915065-1610810963%22%5D; session_token=7cdf01c98150e4b7E13_0-w_22AJds6I0MvVjJlTjacmQjXoUluWqGVDYGpbzqmdsZzpMzdS9vM0FcHheSNqfXFeTcgAs2BKLKEisU2jR0bka6pGt4vCySiZtV5dcDfpt5lk4JL10-uCOv4RzecfZMRLAnuxoYnllU_h31Mt9t9e9cKlHtY-ACv4ZUo-bcszf_zJ8TCgGSXx9gQa6Jegz4Z6HYWjax7EdpkiMFFHPzV8AKjG-WLJrkISN6_rEbBoMUhgk-mmSwxP6CgjQqDICexTC_Q09GDXpcJZhpInKEC7xaygwM8EagKlHRND5Ak1TSxlyaDm_tfYg-FzgZ2p7ug4BIzMMDgA9OK2kTpK579LckHaujRx5B7nLwIIRPW6em472uo1U-Nm930gSB007PnQ19Ntj1lLV6oVVx8w_apq1a0sng_VH9UsCks%3D'
        }
        yield scrapy.Request(url=requestUrl, headers=headers, method='POST',
                             callback=self.download)

    def download(self, response):
        logging.info(response.text)
