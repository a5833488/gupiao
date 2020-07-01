import random

import execjs
import pymysql
import requests


class YinjianSpider(object):

    def __init__(self, url,mf_id):
        self.url = url
        self.session = requests.Session()
        self.session.headers = {
            'Referer': 'http://www.mafengwo.cn/poi/%d.html' % (3562),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
        }


    def add_cookie(self, html):
        js_code1 = html.text.strip()
        js_code1 = js_code1.replace('</script>', '').replace('<script>', '')
        index = js_code1.rfind('}')
        js_code1 = js_code1[0:index + 1]
        js_code1 = 'function getEval() {' + js_code1 + '}'
        js_code1 = js_code1.replace('eval(', 'return(')
        js_code2 = execjs.compile(js_code1)
        code = js_code2.call('getEval')
        code = 'var a' + code.split('document.cookie')[1].split("Path=/;'")[0] + "Path=/;';return a;"
        # code = code
        js_final = "function aa(){" + code + "};"
        start1 = js_final.index('href;') + 5
        end1 = js_final.index('return function')
        two_js = js_final[start1:end1].split(';')
        js = two_js[0] + ';'
        print(js)
        a = js.split('=')
        a_new = a[0] + '="https://";'
        print(a_new)
        js2 = two_js[1] + ';'
        print(js2)
        b = js2.split('=')
        b_new = b[0] + '="www.mafengwo.cn/";'
        jsfinal_1 = js_final.replace(js, a_new)
        jsfinal_2 = jsfinal_1.replace(js2, b_new)
        jsl_clearance = execjs.compile(jsfinal_2).call('aa')
        jsl_cle = jsl_clearance.split(';')[0].split('=')[1]
        self.session.cookies['__jsl_clearance'] = jsl_cle

    def get_all(self,ip):
        ip = str(ip).replace("('", '')
        ip = ip.replace("',)", '')
        proxies = {'http':ip}
        html = self.session.get(self.url)
        self.add_cookie(html)
        web = self.session.get(self.url)
        return web.text

def get_all_ip():
    db = pymysql.connect("localhost", "root", "Aa5833488123", "city")
    cursor = db.cursor()
    sql = 'select ip from url_proxy'
    cursor.execute(sql)
    data = cursor.fetchall()
    return data
if __name__ == '__main__':
    url = 'http://www.mafengwo.cn/poi/{}.html'.format("3562")
    yj = YinjianSpider(url=url, mf_id=3562)
    ips = get_all_ip()
    for ip in ips:
        data = yj.get_all(ip=ip)
        print(data)
