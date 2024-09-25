import random
import requests
from utils import log

proxies = []

def get_proxy():
    if len(proxies) == 0:
        log("proxies are empty, updating")
        update_proxies()
    return random.choice(proxies)

def update_proxies():
    global proxies

    try:
        response = requests.get("https://proxylist.geonode.com/api/proxy-list?limit=30&protocols=https%2Chttp")
        json = response.json()
        # data = [{'_id': '63161eeede95dae521686fae', 'ip': '47.105.126.142', 'anonymityLevel': 'elite', 'asn': 'AS37963', 'city': 'Qingdao', 'country': 'CN', 'created_at': '2022-09-05T16:08:14.685Z', 'google': False, 'isp': 'Hangzhou Alibaba Advertising Co', 'lastChecked': 1727290851, 'latency': 194.497, 'org': 'Aliyun Computing Co., LTD', 'port': '80', 'protocols': ['socks4'], 'region': None, 'responseTime': 71, 'speed': 78, 'updated_at': '2024-09-25T19:00:51.592Z', 'workingPercent': None, 'upTime': 92.28557139284821, 'upTimeSuccessCount': 7381, 'upTimeTryCount': 7998}]
        proxies = [
            {
                "http": "http://" + e["ip"] + ":" + e["port"],
                "https": "http://" + e["ip"] + ":" + e["port"],
            }
            for e in json["data"]
        ]
        log("updated proxies")
    except Exception as e:
        log("failed to update proxies :(")
        log(e)

def mark_bad_proxy(proxy):
    proxies.remove(proxy)


update_proxies()