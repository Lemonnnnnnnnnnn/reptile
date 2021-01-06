from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
import urllib.parse
import time
import json
import matplotlib.pyplot as plt


class Lagou:
    # 初始化
    def init(self):
        self.data = list()
        self.isEnd = False
        opt = webdriver.chrome.options.Options()
        opt.set_headless()
        self.browser = webdriver.Chrome(chrome_options=opt)
        self.wait = WebDriverWait(self.browser, 10)
        self.position = input('前端')
        self.browser.get('https://www.lagou.com/jobs/list_' + urllib.parse.quote(
            self.position) + '?labelWords=&fromSearch=true&suginput=')
        cookie = input('JSESSIONID=ABAAABAABEIABCIDE2785171429CE7F2403378D60C5881B; WEBTJ-ID=20210102203526-176c3186d3c9d7-0e420cd8153ad1-5a301e44-2359296-176c3186d3da76; RECOMMEND_TIP=true; PRE_UTM=; PRE_HOST=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; user_trace_token=20210102203527-027e190a-7423-44ee-b306-60bcf6da7d15; LGSID=20210102203527-90a82d02-6ad3-4777-ba86-fac04638bd62; PRE_SITE=https%3A%2F%2Fwww.lagou.com; LGUID=20210102203527-140ddfdf-7b1a-40e2-950a-2c0779168080; sajssdk_2015_cross_new_user=1; sensorsdata2015session=%7B%7D; _ga=GA1.2.915710751.1609590927; _gat=1; _gid=GA1.2.1536518760.1609590927; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1609590927; index_location_city=%E5%85%A8%E5%9B%BD; gate_login_token=1f13ad96ae6333a732b602ef16cf43e0955a8956f1e85939761d118d5fab8d0c; LG_HAS_LOGIN=1; _putrc=BC6DC905F921B2E3123F89F2B170EADC; login=true; hasDeliver=0; privacyPolicyPopup=false; unick=%E6%9E%97%E5%AE%87%E8%BE%B0; TG-TRACK-CODE=index_search; X_MIDDLE_TOKEN=da69e40e12cf869c7af1408fb93e4adf; SEARCH_ID=96dcea77c980469bb2797d51dc7ff90f; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2220323062%22%2C%22first_id%22%3A%22176c3186fb326e-058c1073ee7a15-5a301e44-2359296-176c3186fb4a3c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2287.0.4280.88%22%2C%22lagou_company_id%22%3A%22%22%7D%2C%22%24device_id%22%3A%22176c3186fb326e-058c1073ee7a15-5a301e44-2359296-176c3186fb4a3c%22%7D; X_HTTP_TOKEN=884e5be83fcab1844741959061198447e7091b1036; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1609591475; LGRID=20210102204435-64088b0e-99a1-4b89-bddc-c8b6219e5cee')
        for item in cookie.split(';'):
            k, v = item.strip().split('=')
            self.browser.add_cookie({'name': k, 'value': v})

    # 爬取网页数据
    def parse_page(self):
        try:
            link = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="position_link"]')))
            link = [item.get_attribute('href') for item in link]
            position = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[@class="position_link"]/h3')))
            position = [item.text for item in position]
            city = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[@class="position_link"]/span/em')))
            city = [item.text for item in city]
            ms_we_eb = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="p_bot"]/div[@class="li_b_l"]')))
            monthly_salary = [item.text.split('/')[0].strip().split(' ')[0] for item in ms_we_eb]
            working_experience = [item.text.split('/')[0].strip().split(' ')[1] for item in ms_we_eb]
            educational_background = [item.text.split('/')[1].strip() for item in ms_we_eb]
            company_name = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="company_name"]/a')))
            company_name = [item.text for item in company_name]
        except TimeoutException:
            self.isEnd = True
        except StaleElementReferenceException:
            time.sleep(3)
            self.parse_page()
        else:
            temp = list(map(lambda a, b, c, d, e, f, g: {'link': a, 'position': b, 'city': c, 'monthly_salary': d,
                                                         'working_experience': e, 'educational_background': f,
                                                         'company_name': g}, link, position, city, monthly_salary,
                            working_experience, educational_background, company_name))
            self.data.extend(temp)

    # 进行翻页操作
    def turn_page(self):
        try:
            pager_next = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'pager_next')))
        except TimeoutException:
            self.isEnd = True
        else:
            pager_next.click()
            time.sleep(3)

    # 爬取数据
    def crawl(self):
        count = 0
        while not self.isEnd:
            count += 1
            print('正在爬取第 ' + str(count) + ' 页 ...')
            self.parse_page()
            self.turn_page()
        print('爬取结束')

    # 保存数据
    def save(self):
        with open('lagou.json', 'w', encoding='utf-8') as f:
            for item in self.data:
                json.dump(item, f, ensure_ascii=False)

    # 数据可视化
    def draw(self):
        count_we = {'经验不限': 0, '经验应届毕业生': 0, '经验1年以下': 0, '经验1-3年': 0, '经验3-5年': 0, '经验5-10年': 0}
        total_we = {'经验不限': 0, '经验应届毕业生': 0, '经验1年以下': 0, '经验1-3年': 0, '经验3-5年': 0, '经验5-10年': 0}
        count_eb = {'不限': 0, '大专': 0, '本科': 0, '硕士': 0, '博士': 0}
        total_eb = {'不限': 0, '大专': 0, '本科': 0, '硕士': 0, '博士': 0}
        for item in self.data:
            count_we[item['working_experience']] += 1
            count_eb[item['educational_background']] += 1
            try:
                li = [float(temp.replace('k', '000')) for temp in item['monthly_salary'].split('-')]
                total_we[item['working_experience']] += sum(li) / len(li)
                total_eb[item['educational_background']] += sum(li) / len(li)
            except:
                count_we[item['working_experience']] -= 1
                count_eb[item['educational_background']] -= 1
        # 解决中文编码问题
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 工作经验-职位数量
        plt.title(self.position)
        plt.xlabel('工作经验')
        plt.ylabel('职位数量')
        x = ['经验不限', '经验应届毕业生', '经验1-3年', '经验3-5年', '经验5-10年']
        y = [count_we[item] for item in x]
        plt.bar(x, y)
        plt.show()
        # 工作经验-平均月薪
        plt.title(self.position)
        plt.xlabel('工作经验')
        plt.ylabel('平均月薪')
        x = list()
        y = list()
        for item in ['经验不限', '经验应届毕业生', '经验1-3年', '经验3-5年', '经验5-10年']:
            if count_we[item] != 0:
                x.append(item)
                y.append(total_we[item] / count_we[item])
        plt.bar(x, y)
        plt.show()
        # 学历-职位数量
        plt.title(self.position)
        plt.xlabel('学历')
        plt.ylabel('职位数量')
        x = ['不限', '大专', '本科', '硕士', '博士']
        y = [count_eb[item] for item in x]
        plt.bar(x, y)
        plt.show()
        # 学历-平均月薪
        plt.title(self.position)
        plt.xlabel('学历')
        plt.ylabel('平均月薪')
        x = list()
        y = list()
        for item in ['不限', '大专', '本科', '硕士', '博士']:
            if count_eb[item] != 0:
                x.append(item)
                y.append(total_eb[item] / count_eb[item])
        plt.bar(x, y)
        plt.show()


if __name__ == '__main__':
    obj = Lagou()
    obj.init()
    obj.crawl()
    obj.save()
    obj.draw()