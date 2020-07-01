import datetime
import threading
from plotly.utils import lock
import pymysql
import os
import bs4
import requests
import json


comment_url = 'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?'

def getAreaData(db,start,end):
    cursor = db.cursor()
    sql = 'SELECT t.mf_area_id,t.travel_area_name,t.id FROM ( SELECT * from area_city_map GROUP BY mf_area_id ) t LEFT JOIN ( SELECT area_id FROM uer_commont GROUP BY area_id ) t1 ON t.id = t1.area_id WHERE t1.area_id IS NULL limit {},{}'.format(start,end)
    cursor.execute(sql)
    data = cursor.fetchall()
    return data,db

def processHtml(db,cursor,html_text,area):
    bs = bs4.BeautifulSoup(html_text)
    #评论列表
    comments = bs.findAll("div", {"class": {"rev-list"}})

    for comment in comments:
        mf_area_id = area[0]
        area_name= area[1]
        area_id = area[2]
        # 创建文件目录和文档
        desktop_path = 'E:\\\AreaData\\' + area_name
        isExists = os.path.exists(desktop_path)
        if not isExists:
            # 如果不存在则创建目录
            try:
                os.makedirs(desktop_path)
            except Exception as e:
                print("创建目录失败"+e)
        lis = comment.find_all("li",{"class":{"rev-item comment-item clearfix"}})
        for li in lis:
            #用户解析
            a_name = li.find("a",{"class": {"name"}})
            u_name = a_name.string
            usr = li.find("div", {"class": {"user"}})
            com_time = li.find("span", {"class": {"time"}})
            com_time = com_time.string
            uid = usr.find("a", {"class": {"avatar"}})['href']
            usr_head = usr.find("a", {"class": {"avatar"}}).find("img").get("src")
            start = uid.index('/u/') + 3
            end = uid.index('.html')
            uid =  uid[start:end]
            user_path = '{}'.format(uid)
            user_path = desktop_path +'\\'+user_path
            isExists = os.path.exists(user_path)
            # start = time.time()
            if not isExists:
                try:
                    os.makedirs(user_path)
                except Exception as e:
                    print("创建目录失败" + e)
            image_file = open(user_path + '\\' + 'head.jpg', 'wb')
            image_file.write(requests.get(usr_head).content)
            #评论
            txt_path = user_path + '\\' + 'comment.txt'
            file = open(txt_path, 'wb')
            comms = li.find_all("p", {"class": {"rev-txt"}})
            for comm in comms:
                comm = str(comm).replace('<p class="rev-txt">', '')
                comm = comm.replace('<br>', '')
                comm = comm.replace('<br/>', '')
                comm = comm.replace('</p>', '')
                comm = comm.encode('utf-8')
                file.write(comm)
            # 评论图片列表
            images = li.find_all("div", {"class": {"rev-img"}})
            i = 0
            for image in images:
                aa = image.find_all("img")
                for img in aa:
                    img_src = img.get("src")
                    image_file = open(user_path +'\\'+ str(i) + '.jpg', 'wb')
                    image_file.write(requests.get(img_src).content)
                    i = i + 1
            #插入数据库
            try:
                sql = 'insert into uer_commont(id,u_id,u_name,mf_area_id,area_id,create_time) VALUES(null,{},"{}",{},{},"{}")'.format(
                    uid, u_name,mf_area_id,area_id,com_time)
                sql_process(db,cursor,sql)
            except Exception as e:
                print(u_name+"插入失败"+e)

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

def processOtherArea(db,cursor,html_text, area):
    print("二次逻辑2222222222222222222222222222222222")
    bs = bs4.BeautifulSoup(html_text)
    # 评论列表
    comments = bs.findAll("div", {"class": {"comment-item"}})
    for comment in comments:
        mf_area_id = area[0]
        area_name = area[1]
        area_id = area[2]
        # 创建文件目录和文档
        desktop_path = 'E:\\AreaData\\' + area_name
        isExists = os.path.exists(desktop_path)
        if not isExists:
            # 如果不存在则创建目录
            try:
                os.makedirs(desktop_path)
            except Exception as e:
                print("创建目录失败" + e)
        # 用户解析
        usr = comment.find("div", {"class": {"info"}})
        a_name = usr.find("a", {"class": {"user-name"}})
        u_name = a_name.string
        com_time = comment.find("span", {"class": {"time"}})
        com_time = com_time.string
        uid = usr.find("a", {"class": {"user-name"}})['href']
        usr_head = comment.find("div", {"class": {"user-bar"}}).find("a").find("img").get("src")
        start = uid.index('/u/') + 3
        end = uid.index('.html')
        uid = uid[start:end]
        user_path = str(uid)
        user_path = desktop_path + '\\' + user_path
        isExists = os.path.exists(user_path)
        # start = time.time()
        if not isExists:
            try:
                os.makedirs(user_path)
            except Exception as e:
                print("创建目录失败" + e)
        image_file = open(user_path + '\\' + 'head.jpg', 'wb')
        image_file.write(requests.get(usr_head).content)
        # 评论
        txt_path = user_path + '\\' + 'comment.txt'
        file = open(txt_path, 'wb')
        comms = comment.find_all("p", {"class": {"rev-txt"}})
        for comm in comms:
            comm = str(comm).replace('<p class="rev-txt">', '')
            comm = comm.replace('<br>', '')
            comm = comm.replace('<br/>', '')
            comm = comm.replace('</p>', '')
            comm = comm.encode('utf-8')
            file.write(comm)
        # 评论图片列表
        images = comment.find_all("a", {"class": {"album_photo"}})
        i = 0
        for image in images:
            aa = image.find_all("img")
            for img in aa:
                img_src = img.get("src")
                image_file = open(user_path + '\\' + str(i) + '.jpg', 'wb')
                image_file.write(requests.get(img_src).content)
                i = i + 1
        # 插入数据库
        try:
            sql = 'insert into uer_commont(id,u_id,u_name,mf_area_id,area_id,create_time) VALUES(null,{},"{}",{},{},"{}")'.format(
                uid, u_name, mf_area_id, area_id, com_time)
            sql_process(db, cursor, sql)
        except Exception as e:
            print(u_name + "插入失败" + e)



def process(i,area_data,db):
    # proxy = get_proxy().get("proxyy")
    # print(proxy)


    cursor = db.cursor()
    print("start is"+str(i))
    for area in area_data:
        area_id = area[0]
        requests_headers = {
            'Referer': 'http://www.mafengwo.cn/poi/%d.html' % (area_id),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
        }
        for num in range(1, 5):
            requests_data = {
                'params': '{"poi_id":"%d","page":"%d","just_comment":1}' % (area_id, num)
            }
            try:
                response = requests.get(url=comment_url, headers=requests_headers, params=requests_data)

                if 200 == response.status_code:
                    html_text = response.text
                    if html_text is not None:
                        html_text = json.loads(html_text)
                        html_text = html_text.get('data').get('html')
                        if html_text.strip() == '':
                            break
                        if html_text.strip()=='<div>暂无内容</div>':
                                t = datetime.datetime.now().timestamp()
                                t = int(t * 1000)
                                url = 'http://www.mafengwo.cn/gonglve/ajax.php?act=get_poi_comments&poi_id={}&type=0&order=0&category=&page={}&ts={}'.format(area_id,num,t)
                                print(url)
                                response=requests.get(url=url,headers=requests_headers)
                                html_text = json.loads(response.text)
                                if html_text.get('msg').strip() == 'failed':
                                    break
                                html_text = html_text.get('html').get('html')
                                if html_text.strip() == '':
                                    break
                                processOtherArea(db,cursor,html_text, area)
                                if num==6:
                                    break
                        processHtml(db,cursor,html_text, area)
            except Exception as e:
                print(e)

def  all_job():
    db = pymysql.connect("localhost", "root", "Aa5833488123", "city")
    html_thread= []
    for i in range(0, 8):
        start = i * 10000
        end = (i + 1) * 10000
        data, db = getAreaData(db, start, end)
        thread = threading.Thread(target=process, args=(i,data,db))
        html_thread.append(thread)
    for i in range(0,8):
        html_thread[i].start()
if __name__ == '__main__':
    all_job()
