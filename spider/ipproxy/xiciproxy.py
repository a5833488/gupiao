import requests
from bs4 import BeautifulSoup
from pyExcelerator import *

s = requests.session()
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}

rs = s.get(url="http://www.xicidaili.com/nn/", headers=header)

soup = BeautifulSoup(rs.text, "lxml")
ip_list_all = []
ip_list = soup.select_one("#ip_list").select("tr")
ip_info_list_key = ["ip", "port", "address", "hidden", "type", "speed", "conn_time", "survival_time", "verify_time"]

for item in ip_list[1:]:
    ip_info_list_value = []
    ip_info = item.select("td")
    for info in ip_info[1:]:
        if info.select_one(".bar"):
            ip_info_list_value.append(info.select_one(".bar")["title"])
        else:
            ip_info_list_value.append(info.get_text().strip())
    ip_list_all.append(dict(zip(ip_info_list_key, ip_info_list_value)))


