import scrapy
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.support import expected_conditions as EC
from .aria2_download import aria2DL


class HentaimaSpider(scrapy.Spider):
    name = 'hentaima'
    allowed_domains = ['hentaimama.io']
    start_urls = ['https://hentaimama.io/tvshows/3d/']
    list = []

    def parse(self, response):
        videoList = response.xpath(
            '//article[@class="item se episodes"]/div[@class="poster"]/div[@class="season_m animation-4"]/a/@href').getall()
        # yield scrapy.Request(videoList[0], callback=self.video_item)
        for item in videoList:
            yield scrapy.Request(item, callback=self.video_item)

    def video_item(self, response):
        # 由于iframe无法直接获取到目标元素 ， 解决方法：进入iframe页面
        iframe_url = response.xpath('//iframe/@src').get()
        name = response.xpath('//*[@id="info"]/h1/text()').get()
        useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        opts = webdriver.ChromeOptions()
        opts.add_argument('--headless')
        opts.add_argument('user-agent=' + useragent)
        opts.add_argument("--window-size=1245,1254")
        opts.add_argument('--disable-gpu')

        driver = webdriver.Chrome(options=opts)
        wait = WebDriverWait(driver, 10)
        driver.get(iframe_url)
        video = wait.until(EC.presence_of_element_located((By.XPATH, '//video')))
        # driver.save_screenshot('test.png')
        video_url = video.get_attribute('src')

        dl = aria2DL()
        print('正在下载，请等待...')
        dl.downloadOne(url=video_url, fileName=name)

        driver.quit()

