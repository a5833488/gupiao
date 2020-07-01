import hashlib
import requests
import datetime
import time
# 可将t改为你想爬取的地区参数
t = datetime.datetime.now().timestamp()
t = int(t*1000)
def par(t):
    hl = hashlib.md5()
    hl.update(t)
    return hl.hexdigest()[2:12]


def get_page():
    for i in range(1,25):
        time.sleep(1)
        print('第' + str(i) + '页')
        page = str(i)
        # 可将iMddid改为你想爬取的地区码
        qdata = '{"_ts":"' + str(t) + '","iMddid":"15139","iPage":"' + str(
            page) + '","iTagId":"0","sAct":"KMdd_StructWebAjax|GetPoisByTag"}c9d6618dbc657b41a66eb0af952906f1'
        sn = par(qdata.encode('utf-8'))

        url = "http://www.mafengwo.cn/ajax/router.php"
        data = {
            'sAct': 'KMdd_StructWebAjax|GetPoisByTag',
            # 可将iMddid改为你想爬取的地区码
            'iMddid': '15139',
            '_ts': t,
            'iPage': page,
            'iTagId': '0',
            '_sn': sn
        }
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        response = requests.request("POST", url, headers=headers, data=data)
        print(response.text)


if __name__ == '__main__':
    get_page()
