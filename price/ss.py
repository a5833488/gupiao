import pandas as pd
import requests
import time
from pylab import mpl, datetime
import  matplotlib.pyplot as plt

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}


#生成出生当年所有日期
def dateRange(a,b):
    fmt = '%Y-%m-%d'
    bgn = int(time.mktime(time.strptime(a,fmt)))
    end = int(time.mktime(time.strptime(b,fmt)))
    list_date = [time.strftime(fmt,time.localtime(i)) for i in range(bgn,end+1,3600*24)]
    return list_date

def get_json(url):
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            json_text=response.json()
            return json_text
    except Exception:
        print('此页有问题！')
        return None


def get_comments(url):
    doc = get_json(url)
    dic = {}
    dic['pigprice'] = doc['pigprice']
    dic['pig_in'] = doc['pig_in']
    dic['pig_local'] = doc['pig_local']
    dic['maizeprice'] = doc['maizeprice']
    dic['bean'] = doc['bean']
    a = '-'.join(doc['time'][3])
    b = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    print(dateRange(a,b))
    dic['time'] = dateRange(a,b)
    return pd.DataFrame(dic)

data =get_comments('https://zhujia.zhuwang.cc/api/chartData?areaId=-1&aa=1589629763568')

print(data)


days = []
today = datetime.date.today()
for i in range(0,366,1):
    daybeforetoday = today + datetime.timedelta(days=-i)
    days.append(daybeforetoday.strftime('%Y-%m-%d'))
days = list(reversed(days))
print(days)

list_number = data['pigprice']
print(len(list_number), len(days))
# prophet模型预测前需要将日期列设为ds，预测的值设为y
df = pd.DataFrame({'y':list_number, 'ds':days})
print(len(df), len(days))

from fbprophet import Prophet

# 调用"先知"生成对象
m = Prophet()

# 使用"先知对象"进行预测
m.fit(df)

# 获得未来30天的数据
future = m.make_future_dataframe(periods=30)

forecast = m.predict(future)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())



# mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
# mpl.rcParams['axes.unicode_minus']
#
# plt.figure(figsize=(8,10), dpi=80)
# plt.figure(1)
# ax1 = plt.subplot(311)
# plt.plot(data['time'],data['pigprice'], color="r",linestyle = "-")
# plt.xticks([])
# plt.annotate(data['pigprice'][365], xy=(data['time'][365], 40), xytext=(data['time'][270], 35), arrowprops=dict(facecolor='black', shrink=0.1, width=0.5))
# plt.xlabel("生猪(外三元) 元/公斤")
#
# ax2 = plt.subplot(312)
# plt.plot(data['time'],data['maizeprice'],color="y",linestyle = "-")
# plt.xticks([])
# plt.xlabel("玉米(15%水分) 元/吨")
#
# ax3 = plt.subplot(313)
# plt.plot(data['time'],data['bean'],color="g",linestyle = "-")
# plt.xlabel("豆粕(43%蛋白) 元/吨")
# plt.xticks(data['time'][2::121], rotation=0)
#
# from pylab import mpl
# import  matplotlib.pyplot as plt
# '''
# python学习交流群：821460695更多学习资料可以加群获取
# '''
# mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
# mpl.rcParams['axes.unicode_minus']
#
# plt.figure(figsize=(8,4), dpi=80)
# plt.plot(data['time'],data['pigprice'], color="r",linestyle = "-")
# plt.xticks(data['time'][2::121], rotation=0)
# plt.xlabel("生猪(外三元) 元/公斤")
# plt.show()
#
# from pylab import mpl
# import  matplotlib.pyplot as plt
# mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
# mpl.rcParams['axes.unicode_minus']
#
# plt.figure(figsize=(8,10), dpi=80)
# plt.figure(1)
# ax1 = plt.subplot(311)
# plt.plot(data['time'],data['pigprice'], color="r",linestyle = "-")
# plt.xticks([])
# plt.annotate(data['pigprice'][365], xy=(data['time'][365], 40), xytext=(data['time'][270], 35), arrowprops=dict(facecolor='black', shrink=0.1, width=0.5))
# plt.xlabel("生猪(外三元) 元/公斤")
#
# ax2 = plt.subplot(312)
# plt.plot(data['time'],data['maizeprice'],color="y",linestyle = "-")
# plt.xticks([])
# plt.xlabel("玉米(15%水分) 元/吨")
#
# ax3 = plt.subplot(313)
# plt.plot(data['time'],data['bean'],color="g",linestyle = "-")
# plt.xlabel("豆粕(43%蛋白) 元/吨")
# plt.xticks(data['time'][2::121], rotation=0)

