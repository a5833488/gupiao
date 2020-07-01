import os

import pymysql

def process(data):
    dbs = pymysql.connect("localhost", "root", "Aa5833488123", "city")
    location = 'E:\\travelData'
    for area in data:
        area_parent_id = str(area[1])
        area_name = area[0]
        arealocal = location+'\\'+area_parent_id
        isExists = os.path.exists(arealocal)
        if isExists:
            print("处理"+area_parent_id)
            i = 1
            files = os.listdir(arealocal)
            if len(files) >=7:
                for filename in os.listdir(arealocal):
                    if filename.find('.jpg'):
                        if i<=6:
                           pic_url = 'static/images/'+area_parent_id+'/'+filename
                           sql = 'update travel_detail set pic_url'+str(i)+'= "'+pic_url+'" where parent_id='+str(area[1])
                           print(sql)
                           sql_process(dbs,sql)
                           i = i + 1
                           if i==7:
                                if filename.find('.txt'):
                                    file_path = location+'\\'+area_name+'\\'+area_name+'.txt'
                                    f = open(file_path, 'r',encoding='UTF-8')
                                    detail_txt = f.read()
                                    print(detail_txt[0:200])
                                    sql = 'update travel_detail set desc_detail = "'+detail_txt[0:200]+'" where parent_id='+str(area[1])
                                    print(sql)
                                    try:
                                        sql_process(dbs,sql)
                                    except:
                                        print("数据异常")
                                    break



def sql_process(db,sql):
    cursor = db.cursor()
    cursor.execute(sql)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print("更新失败")
    # 关闭光标对象
    cursor.close()


def getTravelDetail():
    db = pymysql.connect("localhost", "root", "Aa5833488123", "city")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    sql = 'SELECT area_name,parent_id FROM travel_detail'

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(sql)

    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchall()

    return data
if __name__ == '__main__':
    data = getTravelDetail()
    process(data)