# a script to collect ENF data from the European live ENF measurement
# https://www.mainsfrequency.com/
# the code they have is JS, check mains.js

import requests
import random
import xml.etree.ElementTree as ET
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
from get_data_name import get_enf_data_file_name, get_current_data_dir
from uas import getUA
import datetime
import time
import os

last_id = None
def get_id():
    global last_id
    try:
        if last_id is None:
            # read parquet file and get the last id
            table = pq.read_metadata(get_enf_data_file_name())
            num_rows = table.num_rows
            last_id = num_rows
    except:
        last_id = 0
    last_id += 1
    return last_id

# the numbers 310_000 and -31 always work, but if you send too many requests, they will tell you so...
# so this function gives a random one of the two
def get_c():
    opts = [-31, 310_000]
    return str(random.choice(opts))

def get_enf_data(recursed=False):
    # Placeholder data to test if rate limited
    # return {
    #     "frequency": 50.0,
    #     "time": "2024-08-12 18:05:20",
    #     "phase": 276.4,
    #     "d": 7.0,
    #     "id": get_id()
    # }
    url = "https://netzfrequenzmessung.de:9081/frequenz02c.xml?c=" + get_c()
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Host": "www.mainsfrequency.com",
        "Referer": "https://www.mainsfrequency.com/", # trust me bro
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": getUA()
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
        # Typically happens because we've been rate limited... I don't know how to handle this
        print("Error parsing XML")
        print(data)
        if not recursed:
            return get_enf_data(True)
        return None


last_name = get_enf_data_file_name()
def append_to_parquet(data):
    global last_name
    if last_name != get_enf_data_file_name():
        print("New month, creating new parquet file")
        while not create_parquet():
            print("Failed to create parquet file, trying again")
        last_name = get_enf_data_file_name()

    id = get_id()
    # print("appending " + str(data) + " with id " + str(id))
    df = pd.DataFrame([data])
    table = pa.Table.from_pandas(df)

    if os.path.exists(last_name):
        # Append
        existing_table = pq.read_table(last_name)
        combined_table = pa.concat_tables([existing_table, table])
        pq.write_table(combined_table, last_name)
    else:
        pq.write_table(table, last_name)

def create_parquet():
    if os.path.exists(get_enf_data_file_name()):
        print("File at " + get_enf_data_file_name() + " already exists, not overwriting")
        return True

    seed = get_enf_data()
    if seed is None:
        print("Failed to get seed data")
        return False

    table = pa.Table.from_pandas(pd.DataFrame([seed]))

    if not os.path.exists(get_current_data_dir()):
        os.makedirs(get_current_data_dir())
        pq.write_table(table, get_enf_data_file_name())
        print("Created parquet file " + get_enf_data_file_name())
    return True

def main():
    create_parquet()
    while True:
        data = get_enf_data()
        if data is None:
            print("Failed to get data at " + str(datetime.datetime.now()))

            # If we get "too many requests", we can just wait a bit and it tends to start working.
            time.sleep(1)
            continue
        append_to_parquet(data)
        time.sleep(1 - datetime.datetime.now().microsecond / 1_000_000)

def print_parquet():
    print(pq.read_metadata(get_enf_data_file_name()))


if __name__ == "__main__":
    main()
    # print_parquet()
