# a script to collect ENF data from the European live ENF measurement
# https://www.mainsfrequency.com/
# the code they have is JS, check mains.js

import requests
import random
import xml.etree.ElementTree as ET
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
from get_data_name import get_enf_data_file_name, get_error_file_name, get_current_data_dir
from utils import getUA, get_seconds_from_timestamp
from proxies import get_proxy, update_proxies, mark_bad_proxy
import datetime
import time
import os
from utils import log

last_succesful_write = None

def get_c():
    return str(-31 * random.randint(1, 69_273_666))

def get_enf_data():
    url = "https://netzfrequenzmessung.de:9080/frequenz03c.xml?c=" + get_c()
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Host": "www.mainsfrequency.com",
        "Referer": "https://www.mainsfrequency.com/", # trust me bro
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": getUA(),
    }

    proxy = get_proxy()
    log("got proxy " + str(proxy))
    response = None
    try:
        response = requests.get(url, headers=headers, proxies=proxy, timeout=1)
        log("got responsee")
    except requests.exceptions.ProxyError as e:
        log("proxy error! marking as bad")
        log(e)
        mark_bad_proxy(proxy)
        return None
    log("got response")

    data = response.text
    data = data.replace("<f<", "<")

    try:
        xml = ET.fromstring(data)
        freq = xml.find("f2").text
        data_time = xml.find("z").text
        phase = xml.find("p").text
        d = xml.find("d").text # I don't know what d is, but it's there so it's (probably) important

        data = {
            "frequency": float(freq),
            "time": data_time.strip(),
            "phase": float(phase),
            "d": float(d),
        }

        return data
    except:
        log(data)
        log("caught error; updating proxies...")
        update_proxies()
        return None


last_name = get_enf_data_file_name()
last_data = None
def append_to_csv(data):
    global last_name, last_data, last_succesful_write

    if last_name != get_enf_data_file_name():
        log("New day, creating new CSV file")
        last_name = get_enf_data_file_name()

    df = pd.DataFrame([data])

    now = int(time.time() * 1000 + 500)
    if last_succesful_write != None and now - last_succesful_write > 2800:
        write_error(last_succesful_write, now - last_succesful_write)
    elif last_succesful_write != None and last_data != None:
        # it's been two seconds, so we can actually interpolate the previous one lol
        current_tm = get_seconds_from_timestamp(data["time"])
        last_tm = get_seconds_from_timestamp(last_data["time"])
        if current_tm % 60 == (last_tm + 2) % 60:
            log("missed request (probably due to rate limit)")
            log("\tthis value will be interpolated")
            fake_data = {
                "frequency": (data["frequency"] + last_data["frequency"]) / 2,
                "time": data["time"][0:-2] + str(last_tm + 1),
                "phase": (data["phase"] + last_data["phase"]) / 2,
                "d": (data["d"] + last_data["d"]) / 2
            }
            df = pd.DataFrame([fake_data, data])
            write_error(last_succesful_write, 0)


    if os.path.exists(last_name):
        df.to_csv(last_name, index=False, header=False, mode='a')
    else:
        if not os.path.exists(get_current_data_dir()):
           os.mkdir(get_current_data_dir())
           log("created directory", get_current_data_dir())
        log("File doesn't exist, writing data and header")
        df.to_csv(last_name, index=False, header=True, mode='a')

    last_succesful_write = now
    last_data = data


def write_error(start, duration):
    path = get_error_file_name()
    header = False
    if not os.path.exists(path):
        header = True

    with open(path, 'a') as error:
        if header:
            log("error file does not exist, writing header")
            error.write("day,start,duration\n")

        error.write(
            str(datetime.datetime.now().day) + "," + str(start) + "," + str(duration) + "\n"
        )
        log("wrote error to error.csv")

def main():
    while True:
        try:
            log("Starting collection...")
            while True:
                data = get_enf_data()
                if data is None:
                    log("Failed to get data")
                    continue
                log("appending to csv")
                append_to_csv(data)
                time.sleep(1 - datetime.datetime.now().microsecond / 1_000_000)
        except KeyboardInterrupt:
            log("\nkeyboard interrupt, exiting")
            exit(0)
        except Exception as error:
            log("error!")
            log(error)

if __name__ == "__main__":
    main()
    # print_info()
