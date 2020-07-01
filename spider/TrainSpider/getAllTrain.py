import json

import pymysql
import requests

from spider import util
def get_All_Train():
    url = 'https://kyfw.12306.cn/otn/resources/js/query/train_list.js?scriptVersion=1.0'
    data = requests.get(url)
    return data
if __name__ == '__main__':

    db = pymysql.connect("localhost", "root", "Aa5833488123", "city")
    cursor = db.cursor()
    data = get_All_Train()
    data = data.content
    data = str(data.decode('utf-8')).split(" =")
    data = data[1]
    data = json.loads(data)
    json = data['2019-10-18']
    for j in json :
        train_type = str(j)
        data = json[train_type]
        for train in data:
            train_name = train['station_train_code']
            train_name = str(train_name).split("(")
            train_code = train_name[0]
            start_station = train_name[1].split("-")[0]
            end_station =  train_name[1].split("-")[1].split(")")[0]
            print(train_code)
            print(start_station)
            print(end_station)
            train_no = train['train_no']
            sql = 'INSERT into  train_base(id,train_no,train_code,start_station,end_station,train_type) VALUES(null,"{}","{}","{}","{}","{}")'.format(train_no,
                train_code,start_station,end_station,train_type )
            util.sql_process(db,cursor,sql)
    # datas =  json.loads(data)
    # json = datas['2019-10-18']

    # print(data.content)