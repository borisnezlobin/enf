# a script to collect ENF data from the European live ENF measurement
# https://www.mainsfrequency.com/
# the code they have is JS, check mains.js

import requests
import random
import xml.etree.ElementTree as ET
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
from get_data_name import get_enf_data_file_name, get_error_file_name
from utils import getUA, print_info, get_seconds_from_timestamp
import datetime
import time
import os

last_succesful_write = int(time.time() * 1000 + 500)

# the numbers 310_000 and -31 always work, but if you send too many requests, they will tell you so...
# so this function gives a random one of the two
def get_c():
    opts = [-31, 310_000]
    return str(random.choice(opts))

def get_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def get_enf_data():
    url = "https://netzfrequenzmessung.de:9081/frequenz02c.xml?c=" + get_c()
    ip = get_ip()
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
        "Forwarded": "for=" + ip,
        "X-Forwarded-For": ip,
    }
    response = requests.get(url, headers=headers)
    data = response.text

    try:
        xml = ET.fromstring(data)
        freq = xml.find("f2").text
        time = xml.find("z").text
        phase = xml.find("p").text
        d = xml.find("d").text # I don't know what d is, but it's there so it's (probably) important

        data = {
            "frequency": float(freq),
            "time": time.strip(),
            "phase": float(phase),
            "d": float(d),
        }

        return data
    except:
        print()
        print(data)
        return None


last_name = get_enf_data_file_name()
last_data = None
def append_to_csv(data):
    global last_name, last_data, last_succesful_write

    if last_name != get_enf_data_file_name():
        print("New day, creating new CSV file")
        last_name = get_enf_data_file_name()

    df = pd.DataFrame([data])

    now = int(time.time() * 1000 + 500)
    if now - last_succesful_write > 2500:
        write_error(last_succesful_write, now - last_succesful_write)
    elif last_data != None:
        # it's been two seconds, so we can actually interpolate the previous one lol
        current_tm = get_seconds_from_timestamp(data["time"])
        last_tm = get_seconds_from_timestamp(last_data["time"])
        if current_tm % 60 == (last_tm + 2) % 60:
            print("missed request (probably due to rate limit) at " + str(datetime.datetime.now()))
            print("\tthis value will be interpolated")
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
        print("File doesn't exist, writing data and header")
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
            print("error file does not exist, writing header")
            error.write("day,start,duration\n")

        error.write(
            str(datetime.datetime.now().day) + "," + str(start) + "," + str(duration) + "\n"
        )
        print("wrote error to error.csv")

def main():
    print("Starting collection...")
    while True:
        data = get_enf_data()
        if data is None:
            print("Failed to get data at " + str(datetime.datetime.now()))

            # If we get "too many requests", we can just wait a bit and it tends to start working.
            time.sleep(1)
            continue
        append_to_csv(data)
        time.sleep(1 - datetime.datetime.now().microsecond / 1_000_000)


if __name__ == "__main__":
    # main()
    print_info()
