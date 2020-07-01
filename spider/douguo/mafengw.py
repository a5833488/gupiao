import datetime
import os
import re

import execjs
import js2py
import requests

os.environ["EXECJS_RUNTIME"] = "phantomjs"


def handle_request(url):
    #
    header = {
        "Cache-Control": "max-age=0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "Cookies":"mfw_uuid=5e7492a4-53d4-39fb-42c6-65e5ccc8c8ef; __jsluid_h=4491414ef604703984c28de95a58e687; uva=s%3A78%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1584698022%3Bs%3A10%3A%22last_refer%22%3Bs%3A6%3A%22direct%22%3Bs%3A5%3A%22rhost%22%3Bs%3A0%3A%22%22%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1584698022%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A0%3A%22%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5e7492a4-53d4-39fb-42c6-65e5ccc8c8ef; UM_distinctid=170f75b4e3e61e-096410078fe825-f313f6d-1fa400-170f75b4e3fa2e; __jsluid_s=041bcebabd65a1806dc45154406facf4; c=LOXlXFpq-1587801871829-017e101e2fff7-118354888; _r=baidu; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A18%3A%22www.baidu.com%2Flink%22%3Bs%3A1%3A%22t%22%3Bi%3A1588146570%3B%7D; _fmdata=%2FvUSo%2Bq6usjhfB03q9rj%2FP%2BEya2lSynU5YxR2j0rUE0zH6gWCGen9exBzh4lccCBLam7efi0RORFOjUwZfrGl7a2cuSxsZ47ZuY615FCr1o%3D; _xid=P9KV2XIb8wCMFuagZEuhmB3OiNRmA7Wb0qMh1HUI%2BmAYZbuBvgWPg1JHY46tilu6QyJ17SRdppLuMs%2FlXPu3NQ%3D%3D; oad_n=a%3A5%3A%7Bs%3A5%3A%22refer%22%3Bs%3A21%3A%22https%3A%2F%2Fwww.baidu.com%22%3Bs%3A2%3A%22hp%22%3Bs%3A13%3A%22www.baidu.com%22%3Bs%3A3%3A%22oid%22%3Bi%3A1026%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222020-05-22+14%3A45%3A57%22%3B%7D; __mfwothchid=referrer%7Cwww.baidu.com; __omc_chl=; __mfwc=referrer%7Cwww.baidu.com; bottom_ad_status=0; PHPSESSID=lslibe2ct0b1eda7a1qk6vsvh3; __mfwlv=1590573701; __mfwvn=41; __jsl_clearance=1590579854.332|0|pZpUHzDPKR7cUZ2QyvdJuJ1ud5s%3D; __mfwa=1584697920779.11447.58.1590577616853.1590579856107; CNZZDATA30065558=cnzz_eid%3D1317455400-1584693096-%26ntime%3D1590579464; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1590308162,1590559835,1590573702,1590580560; __omc_r=; __mfwb=95ed260d6a43.3.direct; __mfwlt=1590580565; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1590580565"
    }

    response = requests.post(url=url, headers=header)
    return response

if __name__ == '__main__':
    url = " http://www.mafengwo.cn/poi/3474.html"

    t = datetime.datetime.now().timestamp()
    t = int(t)
    print(t)
    header = {
        "Host":"www.mafengwo.cn",
        "Connection": "keep-alive",
        "Referer": "https://www.mafengwo.cn/poi/3474.html",
        'Sec-Fetch-Site':'same-origin',
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "Cookie": 'mfw_uuid=5e7492a4-53d4-39fb-42c6-65e5ccc8c8ef; __jsluid_h=4491414ef604703984c28de95a58e687; uva=s%3A78%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1584698022%3Bs%3A10%3A%22last_refer%22%3Bs%3A6%3A%22direct%22%3Bs%3A5%3A%22rhost%22%3Bs%3A0%3A%22%22%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1584698022%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A0%3A%22%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5e7492a4-53d4-39fb-42c6-65e5ccc8c8ef; UM_distinctid=170f75b4e3e61e-096410078fe825-f313f6d-1fa400-170f75b4e3fa2e; __jsluid_s=041bcebabd65a1806dc45154406facf4; c=LOXlXFpq-1587801871829-017e101e2fff7-118354888; _r=baidu; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A18%3A%22www.baidu.com%2Flink%22%3Bs%3A1%3A%22t%22%3Bi%3A1588146570%3B%7D; _fmdata=%2FvUSo%2Bq6usjhfB03q9rj%2FP%2BEya2lSynU5YxR2j0rUE0zH6gWCGen9exBzh4lccCBLam7efi0RORFOjUwZfrGl7a2cuSxsZ47ZuY615FCr1o%3D; _xid=P9KV2XIb8wCMFuagZEuhmB3OiNRmA7Wb0qMh1HUI%2BmAYZbuBvgWPg1JHY46tilu6QyJ17SRdppLuMs%2FlXPu3NQ%3D%3D; __mfwothchid=referrer%7Cwww.baidu.com; __omc_chl=; RT="sl=1&ss=1590581261872&tt=0&obo=1&sh=1590581305697%3D1%3A1%3A0&dm=mafengwo.cn&si=ntamwpedgi&ld=1590581305698&r=https%3A%2F%2Fwww.mafengwo.cn%2Fpoi%2F3474.html&ul=1590581305700&hd=1590581305704"; PHPSESSID=1daje2jiiknt3bggv6udv4udv1; __mfwa=1584697920779.11447.59.1590579856107.1590735932123; oad_n=a%3A5%3A%7Bs%3A5%3A%22refer%22%3Bs%3A21%3A%22https%3A%2F%2Fwww.baidu.com%22%3Bs%3A2%3A%22hp%22%3Bs%3A13%3A%22www.baidu.com%22%3Bs%3A3%3A%22oid%22%3Bi%3A1026%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222020-05-29+15%3A15%3A41%22%3B%7D; __mfwc=referrer%7Cwww.baidu.com; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1590580560,1590735932,1590736542,1590737760; bottom_ad_status=0; __omc_r=; __jsl_clearance=1590743251.402|0|7ryz2BScZTDGgRzNy8MxsM%2FF%2B58%3D; __mfwb=a36bd2a5bba0.14.direct; __mfwlv=1590743252; __mfwvn=44; __mfwlt=1590743252; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1590743253; CNZZDATA30065558=cnzz_eid%3D1317455400-1584693096-%26ntime%3D1590742617'
    }
    response = requests.post(url=url, headers=header)
    print(response.text)

