import requests
import json
from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor  # 线程池

# 创建队列
queue_list = Queue()


# 处理数据请求
def handle_request(url, data):
    #
    header = {
        "client": "4",
        "version": "6962.2",
        "device": "SM-G955N",
        "sdk": "25,7.1.2",
        "channel": "sougousj",
        # "resolution":"1600*900",
        # "display-resolution":"1600*900",
        # "dpi":"2.0",
        # "android-id":"784F438E43A20000",
        # "pseudo-id":"864394010787945",
        "brand": "samsung",
        "scale": "2.0",
        "timezone": "28800",
        "language": "zh",
        "cns": "2",
        "carrier": "CMCC",
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; MI 9 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36",
        "imei": "355757801822442",
        "terms-accepted": "1",
        "newbie": "1",
        "reach": "10000",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive",
        "Host": "api.douguo.net",
        "Content-Length": "147",
    }

    response = requests.post(url=url, headers=header, data=data)
    return response


# 抓取品类列表
def handle_cat():
    url = 'https://api.douguo.net/recipe/flatcatalogs'
    data = {
        "client": "4",
        "keyword":"%E7%BA%A2%E7%83%A7%E8%82%89",
        "_vs":"400",
    }
    response = handle_request(url, data)
    index_dic = json.loads(response.text)
    result = index_dic['result']['cs']

    for index_item in result:
        for cs in index_item['cs']:
            for cs_s in cs['cs']:
                print(cs_s)
                data_food = {
                    "client": "4",
                    "keyword": cs_s["name"],
                    "order":"3",
                    "_vs": "400"
                }
                queue_list.put(cs_s["name"])

# 关键词搜索
def handle_search(keyword):
    print("当前处理的食材是:", keyword, end="\n")
    url = 'http://api.douguo.net/search/universalnew/0/10'
    data = {
        "client": "4",
        "keyword": keyword,
        "_vs": "400",
    }
    response = handle_request(url, data)
    caipu_list_dict = json.loads(response.text)
    for item in caipu_list_dict["result"]["recipe"]["recipes"]:
        caipu_info = {}
        caipu_info["shicai"] = keyword
        caipu_info['caipu_name'] = item["n"]
        caipu_info["author_name"] = item["an"]
        caipu_info["caipu_id"] = item["id"]
        caipu_info["cookstory"] = item["cookstory"]
        caipu_info["img"] = item["img"]
        caipu_info["major"] = item["major"]
        caipu_info["detail_url"] = item["au"]
        detail_info_dict = json.loads(handle_detail(caipu_info))
        caipu_info["tips"] = detail_info_dict["result"]["recipe"]["tips"]
        caipu_info["cookstep"] = detail_info_dict["result"]["recipe"]["cookstep"]
        print(caipu_info)
        print("当前入库的菜谱是：", caipu_info['caipu_name'])


# 菜谱详情
def handle_detail(item):
    url = "http://api.douguo.net/recipe/detail/" + str(item["caipu_id"])
    data = {
        "client": "4",
        "_vs": "11101",
        "_ext": '{"query":{ "kw":' + str(item["shicai"]) + ',"src":"11101","idx":"1", "type":"13", "id":' + str(
            item["caipu_id"]) + ' }',
    }
    response = handle_request(url, data)
    return response.text

def do_process():
    queue_lists =  handle_cat()

    pool = ThreadPoolExecutor(max_workers=1)  # 创建线程池
    # while queue_list.qsize() > 0: 报错
    
    while not queue_list.empty():
        pool.submit(handle_search, queue_list.get())  # 函数名和 参数

if __name__ == '__main__':
    do_process()