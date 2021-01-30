from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ez_crawler import ezCrawler
from judge_ip import ipJudge


def processCrawl1():
    process = CrawlerProcess(get_project_settings())
    process.crawl('fpl')
    process.start()  # the script will block here until the crawling is finished


def processCrawl2():
    crawler = ezCrawler()
    crawler.httpCrawl()
    crawler.socks4Crawl()
    crawler.socks5Crawl()

def judge():
    pass
    obj = ipJudge()
    http_num_lines = sum(1 for line in open('out/http.txt'))
    socks4_num_lines = sum(1 for line in open('out/socks4.txt'))
    socks5_num_lines = sum(1 for line in open('out/socks5.txt'))
    thread_num = 50
    print('正在开启线程...')

    obj.thread(http_num_lines, thread_num, 'http')
    obj.thread(socks4_num_lines, thread_num, 'socks4')
    obj.thread(socks5_num_lines, thread_num, 'socks5')


if __name__ == '__main__':
    # processCrawl1()
    # processCrawl2()
    judge()
