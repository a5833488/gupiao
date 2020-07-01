import hashlib
import requests, json
import pymysql
import bs4
import time
import os
import datetime
def par(t):
    hl = hashlib.md5()
    hl.update(t)
    return hl.hexdigest()[2:12]

def get_page(data,db):
    mf_id = data[0]
    city_id = data[1]
    for i in range(1,20):
        page = str(i)
        print('第' + page + '页')
        t = datetime.datetime.now().timestamp()
        t = int(t * 1000)
        # 可将iMddid改为你想爬取的地区码
        qdata = '{"_ts":"' + str(t) + '","iMddid":"'+str(mf_id)+'","iPage":"' + str(
            page) + '","iTagId":"0","sAct":"KMdd_StructWebAjax|GetPoisByTag"}c9d6618dbc657b41a66eb0af952906f1'
        sn = par(qdata.encode('utf-8'))
        time.sleep(0.5)
        url = "http://www.mafengwo.cn/ajax/router.php"
        data = {
            'sAct': 'KMdd_StructWebAjax|GetPoisByTag',
            # 可将iMddid改为你想爬取的地区码
            'iMddid': '{}'.format(str(mf_id)),
            '_ts': t,
            'iPage': page,
            'iTagId': '0',
            '_sn': sn
        }
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        r = requests.request("POST", url, headers=headers, data=data)
        if r.status_code == 200:
            # 将返回的数据转成json
            print(r.content)
            strs = json.loads(r.text)
            # 使用bs解析

            html = strs.get('data').get('list')
            if html.strip() =='':
                break
            soup = bs4.BeautifulSoup(html)
            imgs = soup.find_all('img')
            titles = soup.find_all('h3')
            urls = soup.find_all('a')
            for title, img_src, url in zip(titles, imgs, urls):
                try:
                    print(title.text, img_src['src'], url['href'])
                    travel_area_name = title.text
                    uri = url['href']
                    start = uri.index("poi/") + 4
                    end = uri.index(".html")
                    mf_area_id =  uri[start:end]
                    sql = 'insert into area_city_map (id,travel_area_name,mf_area_id,city_id) VALUES(null,"{}",{},{})'.format(
                        travel_area_name, mf_area_id, city_id)
                    print(sql)
                    sql_process(db, sql)
                    # 保存图片
                    desktop_path = 'E:\\AreaData\\' + travel_area_name
                    isExists = os.path.exists(desktop_path)
                    if not isExists:
                        # 如果不存在则创建目录
                        os.makedirs(desktop_path)
                        print(desktop_path + '创建成功')
                    image_file = open(desktop_path + '//' + 'main' + '.jpg', 'wb')
                    image_file.write(requests.get(img_src['src']).content)
                except:
                    print("处理失败")


def getAllCity():
    db = pymysql.connect("localhost", "root", "Aa5833488123", "city")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = 'SELECT t.mf_id,t.city_id from city_mf_map t LEFT JOIN area_city_map t1 on t.city_id = t1.city_id WHERE t1.city_id is null'
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(sql)
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchall()
    return data,db


def sql_process(db,sql):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print("更新失败")
    # 关闭光标对象
    cursor.close()

def getallid(datas,db):
    for data in datas:
        get_page(data,db)

if __name__ == '__main__':
    data,db = getAllCity()
    getallid(datas=data,db=db)