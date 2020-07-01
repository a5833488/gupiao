#获取有用的ip插入到mysql中
import re

import bs4
import pymysql
import requests
from spider.util import sql_process

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def get_proxy():
    ips = requests.get("http://127.0.0.1:5010/get_all/").json()
    ip_list = []
    for ip in ips:
        date = ip.get("last_time")
        if "2020-06-13" in date:
            print(date)
            ip_list.append(ip.get("proxy"))
    return ip_list


def get_ips():
    comment_url = 'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?'

    requests_headers = {
        # 'Referer': 'http://www.mafengwo.cn/poi/%d.html' % (3562),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/225.36'
    }

    # response = requests.get(url=comment_url, headers=requests_headers, params=requests_data)
    ip_list = get_proxy()
    ip_200 = []

    for ip in ip_list:
        proxies = 'http://{}'.format(ip)
        try:
            response = requests.get(
                url='http://www.mafengwo.cn/search/q.php?q=故宫&t=notes',
                headers=requests_headers, proxies={'http': ip},timeout=5)
            if 200 == response.status_code:
                ip_200.append(ip)
                print(ip)

        except Exception as e:
            print("调用马蜂窝失败"+ip)
    return ip_200




if __name__ == '__main__':
    ips = get_ips()
    db = pymysql.connect("localhost", "root", "Aa5833488123", "city")
    cursor = db.cursor()
    sql = "DELETE FROM url_proxy"
    sql_process(db, cursor, sql)
    for ip in ips:
        sql = 'insert  into url_proxy(ip)VALUES("{}")'.format(ip)
        sql_process(db,cursor,sql)




