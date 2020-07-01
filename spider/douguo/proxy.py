import requests
from  spider.SpiderUtil import get_all_ip
url = 'http://ip.hahado.cn/ip'
ips = get_all_ip()
for ip in ips:
    #{"ip":"59.63.206.110","locale":""}
    ip = str(ip).replace("('", '')
    ip = ip.replace("',)", '')
    print(ip)
    proxies =None
    proxies = {'http': ip}
    try:
        res = requests.get(url,proxies={'http': ip})
    except Exception as e:
        print(e)
    print(res.text)