import os
import random
import threading
import time

import bs4
import execjs
import pymysql
import requests
from plotly.utils import lock
from selenium import webdriver
from spider.SpiderUtil import YinjianSpider
from selenium.webdriver import ChromeOptions




def get_all_ip():
    db = pymysql.connect("localhost", "root", "Aa5833488123", "city")
    cursor = db.cursor()
    sql = 'SELECT ip FROM url_proxy GROUP BY ip'
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

def get_random_ip(ips):
    total = len(ips)
    i = int(random.uniform(1, total))
    ip = ips[i]
    ip = str(ip).replace("('",'')
    ip = ip.replace("',)",'')
    return  ip


def getAreaData(db,start, end):
    sql = 'SELECT t.travel_area_name,t.id,t.mf_area_id,0	FROM ( SELECT travel_area_name, id, mf_area_id FROM area_city_map_2 WHERE travel_area_name != "" GROUP BY travel_area_name, mf_area_id ) t LEFT JOIN  travel_area_new_copy2 t1 ON t.id = t1.area_id WHERE t1.area_id IS NULL limit {},{}'.format(start,end)
    print(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data,db
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json().get("proxy")

# def get_all_Area(mf_area_id,ip):
#     url = 'https://www.mafengwo.cn/poi/{}.html'.format(mf_area_id)
#     yj = YinjianSpider(url=url,mf_id=mf_area_id)
#     data =  yj.get_all(ip=ip)
#     return data

def get_Detail_Data(area_id,ip):
    header = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/{}".format(area_id)
    }
    url = "http://www.mafengwo.cn/poi/{}.html".format(3474)
    response = requests.get(url, headers=header,proxies={'http':ip},timeout=3)

    __jsluid_h = None
    __jsluid_h = response.headers['set-cookie']
    __jsluid_h = str(__jsluid_h).split(';')
    __jsluid_h = __jsluid_h[0]
    js_code1 = None
    js_code1 = response.text.strip()
    js_code1 = js_code1.replace('</script>', '').replace('<script>', '')
    index = js_code1.rfind('}')
    js_code1 = js_code1[0:index + 1]
    js_code1 = 'function getEval() {' + js_code1 + '}'
    js_code1 = js_code1.replace('eval(', 'return(')
    js_code2 = execjs.compile(js_code1)
    code = js_code2.call('getEval')
    code = 'var a' + code.split('document.cookie')[1].split("Path=/;'")[0] + "Path=/;';return a;"
    js_final = None
    js_final = "function aa(){" + code + "};"

    if 'href;' in js_final:
        start1 = js_final.index('href;') + 5
        end1 = js_final.index('return function')
        two_js = js_final[start1:end1].split(';')
        js = two_js[0] + ';'
        a = js.split('=')
        a_new = a[0] + '="https://";'
        js2 = two_js[1] + ';'
        b = js2.split('=')
        b_new = b[0] + '="www.mafengwo.cn/";'
        js_final = js_final.replace(js, a_new)
        js_final = js_final.replace(js2, b_new)
        jsl_clearance = execjs.compile(js_final).call('aa')
    else:
        js_final = "var jsdom = require('jsdom');var {JSDOM} = jsdom;var dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);window = dom.window;" + js_final
        jsl_clearance = execjs.compile(js_final).call('aa')
    jsl_cle = jsl_clearance.split(';')[0].split('=')[1]
    __jsl_clearances = '__jsl_clearance=' + jsl_cle

    cookie = '{};{}'.format(__jsluid_h, __jsl_clearances)


    header['Cookie'] = cookie
    response = requests.get(url, headers=header,proxies={'http':ip},timeout=5)

    return header
    # return web.text


def process(i, data, db,ip,head):

    for area in data:
        time.sleep(1)
        travel_area_name = area[0]
        area_id = str(area[1])
        mf_area_id = str(area[2])
        traffic = ''
        ticket = ''
        open_time = ''
        area_descrip = ''
        tel = ''
        travel_time = ''
        url = 'http://www.mafengwo.cn/poi/{}.html'.format(mf_area_id)
        html_text = None
        try:
            html_text =requests.get(url, headers=head,proxies={'http':ip})
        except:
            pass
        try:
            if 200==html_text.status_code:
                bs = bs4.BeautifulSoup(html_text.text)
            # 图片
                pic = None
                pic = bs.find("div", {"class": {"pic-big"}})
                if pic !=None:
                    pic = pic.find('img')
                    desktop_path = 'E:\\AreaData\\' + str(travel_area_name)
                    isExists = os.path.exists(desktop_path)
                    if not isExists:
                        # 如果不存在则创建目录
                        try:
                            os.makedirs(desktop_path)
                            print(desktop_path + '创建成功')
                            image_file = open(desktop_path + '//' + 'big_main' + '.jpg', 'wb')
                            image_file.write(requests.get(pic['src']).content)
                        except :
                            pass
                comments = None
                comments = bs.find("div",{"class": {"mod mod-detail"}})
                try:
                    if comments != None:
                        area_descrip = None
                        try:
                            area_descrip = comments.find("div", {"class": {"summary"}})
                        except:
                            pass
                        if area_descrip != None:
                            area_descrip = replace_text(area_descrip.text)
                        tel = None
                        try:
                            tel = comments.find("li", {"class": {"tel"}})
                        except:
                            pass
                        if tel != None:
                            tel = tel.find("div", {"class": {"content"}})
                            if tel != None:
                                tel = tel.string
                        travel_time = None
                        try:
                            travel_time = comments.find("li", {"class": {"item-time"}})
                        except:
                            pass
                        if travel_time != None:
                            travel_time = travel_time.find("div", {"class": {"content"}})
                            if travel_time != None:
                                travel_time = travel_time.string
                        dls = None
                        try:
                            dls = comments.find_all("dl")
                        except:
                            pass
                        for dl in dls:
                            dt = None
                            try:
                                dt = dl.find("dt").string
                            except:
                                pass
                            if dt =="交通":
                                traffic =  str(dl.find("dd"))
                                if traffic != None:
                                    traffic = replace_text(traffic)
                            elif dt =="门票":
                                ticket = None
                                try:
                                    ticket =  str(dl.find("dd").find("div").find("div"))
                                except:
                                    pass
                                if ticket != None:
                                    ticket = replace_text(ticket)
                                else:
                                    try:
                                        ticket = str(dl.find("dd").find("div"))
                                    except:
                                        pass
                                print(ticket)
                            elif dt =="开放时间":
                                open_time = None
                                try:
                                    open_time = str(dl.find("dd"))
                                except:
                                    pass
                                if traffic != None:
                                    open_time = replace_text(open_time)
                except:
                    pass
                try:
                    area_address = bs.find("div", {"class": {"mhd"}}).find("p", {"class": {"sub"}}).string
                    print(area_address)
                except Exception as e:
                    pass
                # 插入数据库
                try:
                    sql = 'insert into travel_area_new_copy2(id,travel_area_name,area_descrip,address,area_id,travel_time,traffic,ticket,open_time,phone,mf_area_id) VALUES(null,"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(
                        travel_area_name, area_descrip, area_address, area_id, travel_time,traffic,ticket,open_time,tel,mf_area_id)
                    cursor = db.cursor()
                    sql_process(db, cursor, sql)
                except Exception as e:
                    pass
        except:
            pass
def sql_process(db,cursor,sql):
    lock.acquire()
    try:
        cursor.execute(sql)
        db.commit()
        print(sql)
    except Exception as  e:
        # 如果发生错误则回滚
        db.rollback()
        cursor.close()
        print("更新失败"+e)
    finally:
        lock.release()

def replace_text(text):
    text = text.replace('<br>', '')
    text = text.replace('<dd>', '')
    text = text.replace('<br/>', '')
    text = text.replace('</dd>', '')
    text = text.replace('<div>', '')
    text = text.replace('</div>', '')
    text = text.replace('"', '')
    # text = text.encode('utf-8')
    return text

def all_job():
    ips = get_all_ip()
    db = pymysql.connect("localhost", "root", "Aa5833488123", "city")
    data, db = getAreaData(db, 0, 5000)
    html_thread = []
    heads = {}
    s = 0
    for ip in ips:
        s = s+1
        try:
            ip = str(ip).replace("('", '')
            ip = ip.replace("',)", '')
            head = get_Detail_Data(random.random(),ip)
            heads[ip] = head
        except Exception as e:
            pass
    i=0
    for ip, head in heads.items():
        ds = []
        c = i*100
        b = (i+1) *100
        for c in range(c,b):
            c = c+1
            if (c==b):
                break
            ds.append(data[c])
        i = i+1
        print(ip)
        if head !=None:
            thread = threading.Thread(target=process, args=(i, ds, db,ip,head))
            html_thread.append(thread)
    for i in range(0, len(html_thread)):
        html_thread[i].start()
if __name__ == '__main__':
    all_job()
