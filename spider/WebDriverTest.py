import os
import threading
import time

import bs4
import pymysql
import requests
from plotly.utils import lock
from selenium import webdriver

def get_proxy():
    ips = requests.get("http://127.0.0.1:5010/get_all/").json()
    ip_list = []
    for ip in ips:
        date = ip.get("last_time")
        if "2020-05-21" in date:
            print(date)
            ip_list.append(ip.get("proxy"))
    return ip_list

def getbrowser(ip):
    options = webdriver.ChromeOptions()
    # 设置代理
    desired_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
    desired_capabilities['proxy'] = {
        "httpProxy": ip,
        "noProxy": None,
        "proxyType": "MANUAL",
        "class": "org.openqa.selenium.Proxy",
        "autodetect": False
    }
    # 使用无头模式
    options.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=options,
                               desired_capabilities=desired_capabilities)
    return browser

if __name__ == '__main__':

    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--proxy-server=http://217.160.63.219:3128")
    browser = webdriver.Chrome(chrome_options=chromeOptions)
    # ip_list = get_proxy()
    url = 'https://www.mafengwo.cn/poi/{}.html'.format('3474')
    # browser = getbrowser("58.220.95.86:9401")
    # # 打开目标网站
    # browser.get("https://www.baidu.com")
    # # 对整个页面进行截图
    # # browser.save_screenshot('百度.png')
    # # # 打印网站的title信息
    # # print(browser.title)
    # # 检测代理ip是否生效
    # browser.get("http://httpbin.org/ip")
    # # 获取当前所有窗口集合(list类型) --- 因为打开多个窗口
    # handles = browser.window_handles
    # # 切换到最新的窗口
    # browser.switch_to_window(handles[-1])
    # print(browser.page_source)
    # 打印新窗口网页的内容
    url = 'https://www.mafengwo.cn/poi/{}.html'.format('3474')
    browser.get(url)
    # time.sleep(3)
    html_text = browser.page_source
    print(html_text)