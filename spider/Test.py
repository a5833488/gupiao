import re
import time
import js2py
import requests
import execjs


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

# your spider code

def getHtml():
    comment_url = 'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?'

    retry_count = 1
    while retry_count > 0:
        try:
            requests_headers = {
                'Referer': 'http://www.mafengwo.cn/poi/%d.html' % (3562),
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
            }
            for num in range(1, 6):
                requests_data = {
                    'params': '{"poi_id":"%d","page":"%d","just_comment":1}' % (3562, 1)
                }
            # response = requests.get(url='https://www.mafengwo.cn/poi/3562.html', headers=requests_headers)
            response = requests.get(url=comment_url,headers=requests_headers,proxies={'http':'112.80.248.18:80'})
            # js_code1 = response.text.strip()
            # js_code1 = js_code1.replace('</script>', '').replace('<script>', '')
            # index = js_code1.rfind('}'    )
            # js_code1 = js_code1[0:index + 1]
            # js_code1 = 'function getEval() {' + js_code1 + '}'
            # js_code1 = js_code1.replace('eval(', 'return(')
            # js_code2 = execjs.compile(js_code1)
            # code = js_code2.call('getEval')
            # code = 'var a' + code.split('document.cookie')[1].split("Path=/;'")[0] + "Path=/;';return a;"
            # # code = code
            # js_final = "function aa(){" + code + "};"
            # js_final = js_final.replace("return return", "return eval")
            # jsl_clearance = execjs.compile(js_final).call('aa')
            # jsl_cle = jsl_clearance.split(';')[0].split('=')[1]

            js_uid_s  = response.headers['set-cookie']
            res = str(response.text)
            print(res)
            res = re.search(r"<script>(.*?)</script>",res).group(1)
            res = res.replace("eval(","return(")
            js1 = "function aa(){"+res+";return x}"
            data = js2py.eval_js(js1)()
            func = re.search('__jsl_clearance=.*?(function.*})\)\(\)\+.;Expires=',data).group(1)
            func = func.replace("function()","function bb()")
            data2 = js2py.eval_js(func)()
            print(data2)
            return response
        except Exception as e:
            print(e)
            retry_count -= 1
    # 出错5次, 删除代理池中代理
    return None

if __name__ == '__main__':
    getHtml()