# -*- coding:utf-8 -*-
import requests
import random
import time
import pandas as pd
from lxml import etree


import re

User_Agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"]

HEADERS = {
    'User-Agent': User_Agent[random.randint(0, 5)],
    # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    # 能力有限，不懂怎么解译JS来自动生成 cookie，只能复制张贴
    'Cookie': '',   # 请自行张贴上成功请求时的 cookie
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}

# 从游记中获取数据
def get_data(u):
    print('Getting...')


    res_u = requests.get(u, headers=HEADERS, timeout=10).text
    res_u1 = etree.HTML(res_u)
    dic = {}
    n = random.randint(5, 10)
    dic['标题'] = res_u1.xpath('//h1[@class="headtext lh80"]/text()')
    dic['月份'] = res_u1.xpath('//ul/li[@class="time"]/text()[2]')
    dic['天数'] = res_u1.xpath('//ul/li[@class="day"]/text()[2]')
    dic['人物'] = res_u1.xpath('//ul/li[@class="people"]/text()[2]')
    dic['费用'] = res_u1.xpath('//ul/li[@class="cost"]/text()[2]')
    dic['URL'] = u
    data.append(dic)
    print(link + '__success')
    time.sleep(n)
    return data

def getall(url):
    print("get js data")
    session_req = dryscrape.Session()
    session_req.visit(url)  # 请求页面
    response = session_req.body()  # 网页的文本
    return response



# 获取页面中每篇游记的链接
def get_links(res):
    res1 = etree.HTML(res)
    links = res1.xpath('//a[@class="title-link"]/@href')
    time.sleep(3)
    return links

data = []
# 要爬取的页面数 (1, 末页-1)
for i in range(1, 69):
    print('Start_' + str(i))
    url = 'http://www.mafengwo.cn/yj/18341/1-0-{}.html'.format(i)
    # url = 'https://m.mafengwo.cn/poi/33643552.html#&gid=1&pid=1'
    print(url)
    print('-' * 20)
    # proxies = get_proxies()
    res = requests.get(url, headers=HEADERS).text
    links = get_links(res)
    for link in links:
        # u = 'http://www.mafengwo.cn' + link
        u = 'http://www.mafengwo.cn/poi/3474.html'

        print(u)
        data = get_data(u)
        print(data)
    print('success')
    n = random.randint(3, 8)
    time.sleep(n)

df = pd.DataFrame(data)
print('=' * 20)
# 修改文件储存路径
df.to_csv('C:/MFW_notes_3.csv', mode='a', header=True, encoding='utf_8_sig')
print('All Finished')
