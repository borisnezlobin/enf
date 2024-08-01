# a script to collect ENF data from the European live ENF measurement
# https://www.mainsfrequency.com/
# the code they have is JS, check mains.js

import requests
import random

# python equivalent of "Math.round(Math.random() * 100000) * 31, true)"
def get_c():
    return round((random.random() * 100000)) * 31

def collect_enf_data():
    url = "https://netzfrequenzmessung.de:9081/frequenz02c.xml?c=2575511"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Host": "www.mainsfrequency.com",
        "Referer": "https://www.mainsfrequency.com/", # trust me bro
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        # some random user agent from https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    data = response.text
    return data

print(collect_enf_data())