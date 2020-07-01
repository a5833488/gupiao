import datetime

import execjs
import requests
from plotly import session

def get_head():

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/{}".format(56464464)
    }

    url = 'http://www.mafengwo.cn/poi/3474.html'
    response = requests.get(url, headers=header)
    __jsluid_h = None
    __jsluid_h = response.headers['set-cookie']
    __jsluid_h = str(__jsluid_h).split(';')
    __jsluid_h = __jsluid_h[0]
    js_code1 = None
    js_code1 = response.text.strip()
    js_code1 = js_code1.replace('</script>', '').replace('<script>', '')
    index = js_code1.rfind('}')
    js_code1 = js_code1[0:index + 1]
    js_code1 = 'function getEval() {' + js_code1 + '}'
    js_code1 = js_code1.replace('eval(', 'return(')
    js_code2 = execjs.compile(js_code1)
    code = js_code2.call('getEval')
    code = 'var a' + code.split('document.cookie')[1].split("Path=/;'")[0] + "Path=/;';return a;"
    # code = code
    js_final = None
    js_final = "function aa(){" + code + "};"
    print(js_final)

    if 'href;' in js_final:
        start1 = js_final.index('href;') + 5
        end1 = js_final.index('return function')
        two_js = js_final[start1:end1].split(';')
        js = two_js[0] + ';'
        a = js.split('=')
        a_new = a[0] + '="https://";'
        js2 = two_js[1] + ';'
        b = js2.split('=')
        b_new = b[0] + '="www.mafengwo.cn/";'
        js_final = js_final.replace(js, a_new)
        js_final = js_final.replace(js2, b_new)
        js_code2 = execjs.compile(js_final)
        jsl_clearance =js_code2.call('aa')
    else:
        js_final = "var jsdom = require('jsdom');var {JSDOM} = jsdom;var dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);window = dom.window;"+js_final
        js_code2 = execjs.compile(js_final)
        jsl_clearance =js_code2.call('aa')
    jsl_cle = jsl_clearance.split(';')[0].split('=')[1]
    __jsl_clearances = '__jsl_clearance='+jsl_cle
    print("__jsl_clearances is "+__jsl_clearances)
    cookie = '{};{}'.format(__jsluid_h,__jsl_clearances)
    header['Cookie']=cookie
    print("head Cookie is "+header['Cookie'])
    web=requests.get(url, headers=header)
    print(web.text)

    return header
#     web=requests.get(url, headers=header)
# print(web.text)


if __name__ == '__main__':
    head = get_head()
    web=requests.get('http://www.mafengwo.cn/poi/71736928.html', headers=head)
    print("web is "+web.text)
    web=requests.get('http://www.mafengwo.cn/poi/888951.html', headers=head)
    print("web is "+web.text)
