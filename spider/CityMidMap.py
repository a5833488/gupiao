import pymysql
from selenium import webdriver
import json

def getCity():
    db = pymysql.connect("localhost", "root", "Aa5833488123", "city")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    sql = 'SELECT t.id,t.short_name FROM  (SELECT id,short_name from z_cnarea_2016 WHERE `level` < 3) t LEFT JOIN city_mf_map t1 on t.id = t1.city_id WHERE t1.city_id is null '
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(sql)

    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchall()
    return data

def getHtml(db,datas):
      for data in datas:
        city_id = data[0]
        city_name = data[1]
        url = 'https://www.mafengwo.cn/search/ss.php?callback=jQuery181039442571110573676_1586931968696&isHeader=1&key=' + city_name + '&_ts=1586932390206&_sn=0d6469ce88&_=1586932390206'
        driver = webdriver.Chrome()
        driver.get(url)
        html_text = driver.page_source
        start = html_text.index("({")+1
        end = html_text.index(");")
        jsondata = html_text[start:end]
        driver.quit()
        d = json.loads(jsondata)
        try:
            mf_id = None
            if ('mdd_info'in d):
                mf_id = d['mdd_info']['result'][0]['id']
            elif('poi_info' in d):
                mf_id = d['poi_info']['result'][0]['id']
            if mf_id is not None:
                sql = 'insert into city_mf_map (id,city_name,mf_id,city_id) VALUES(null,"{}",{},{})'.format(city_name,mf_id, city_id)
                print(sql)
                sql_process(db, sql)
        except:
            print("更新失败")


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


if __name__ == '__main__':
    db = pymysql.connect("localhost", "root", "Aa5833488123", "city")
    data = getCity(db)
    getHtml(db,data)