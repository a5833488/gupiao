import threading
import time

import pymysql
import requests

import bs4
from spider import util
def getall():
    print("ss")

def get_all_ip():
    db = pymysql.connect("localhost", "root", "Aa5833488123", "city")
    cursor = db.cursor()
    sql = 'SELECT ip FROM url_proxy GROUP BY ip'
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

def get_data(start,end):
    sql = 'SELECT	id,travel_area_name FROM travel_area_new t LEFT  JOIN ( SELECT area_id FROM area_note_map GROUP BY area_id ) t1 ON t.id = t1.area_id  WHERE t1.area_id IS  NULL limit {},{}'.format(start,end)
    db = pymysql.connect("localhost", "root", "Aa5833488123", "city")
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data, db

def process(data,db,ip):
    time.sleep(3)
    cursor = db.cursor()
    for d in data:
        id = d[0]
        name = d[1]
        url = 'http://www.mafengwo.cn/search/q.php?q={}&t=notes'.format(name)
        header = {
            "User-Agent": "Mozilla/6.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/{}".format(
                id)
        }
        try:
            response = requests.get(url, headers=header,proxies={'http':ip},timeout=5)
            if 200==response.status_code:
                bs = bs4.BeautifulSoup(response.text)
                divs = bs.find("div", {"class": {"att-list"}})
                ul = divs.find("ul").findAll("div", {"class":{"flt1"}})
                for li in ul :
                    div = li.find("a")['href']
                    if div is not None:
                        sql = 'INSERT into area_note_map(id,area_id,area_name,note_url) VALUES(null,{},"{}","{}")'.format(id,name,div)
                        util.sql_process(db,cursor,sql)
        except:
            pass

if __name__ == '__main__':
    ips = get_all_ip()
    data, db = get_data(0, 50000)
    html_thread = []
    heads = {}
    s = 0
    i = 0
    for ip in ips:
        try:
            ip = str(ip).replace("('", '')
            ip = ip.replace("',)", '')
        except Exception as e:
            pass
        ds = []
        c = i * 1000
        b = (i + 1) * 1000
        for c in range(c, b):
            c = c + 1
            if (c == b):
                break
            ds.append(data[c])
        print(ip)
        thread = threading.Thread(target=process, args=(ds, db, ip))
        html_thread.append(thread)
        i = i+1
    for i in range(0, len(html_thread)):
        html_thread[i].start()

