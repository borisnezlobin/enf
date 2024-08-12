# a script to collect ENF data from the European live ENF measurement
# https://www.mainsfrequency.com/
# the code they have is JS, check mains.js

import requests
import random
import xml.etree.ElementTree as ET
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
from uas import getUA

FILE_PATH = "collection/enf_data.parquet"
last_id = None
def get_id():
    global last_id
    try:
        if last_id is None:
            # read parquet file and get the last id
            table = pq.read_table(FILE_PATH)
            last_id = table["id"].to_pandas().iloc[-1]
    except:
        last_id = 0
    last_id += 1
    return last_id

# python equivalent of "Math.round(Math.random() * 100000) * 31, true)"
# for whatever reason, c=-31 *always* works, so... sure lol
def get_c():
    return round((random.random() * 100000)) * 31

def get_enf_data(recursed=False):
    return {
        "frequency": 50.0,
        "time": "2024-08-12 18:05:20",
        "phase": 276.4,
        "d": 7.0,
        "id": get_id()
    }
    # url = "https://netzfrequenzmessung.de:9081/frequenz02c.xml?c=-31"
    # headers = {
    #     "Accept": "*/*",
    #     "Accept-Language": "en-US,en;q=0.5",
    #     "Connection": "keep-alive",
    #     "Host": "www.mainsfrequency.com",
    #     "Referer": "https://www.mainsfrequency.com/", # trust me bro
    #     "Sec-Fetch-Dest": "empty",
    #     "Sec-Fetch-Mode": "cors",
    #     "Sec-Fetch-Site": "same-origin",
    #     "User-Agent": getUA()
    # }
    # response = requests.get(url, headers=headers)
    # data = response.text
    # try:
    #     xml = ET.fromstring(data)
    #     freq = xml.find("f2").text
    #     time = xml.find("z").text
    #     phase = xml.find("p").text
    #     d = xml.find("d").text # I don't know what d is, but it's there so it's (probably) important
    #     data = {
    #         "frequency": float(freq),
    #         "time": time.strip(),
    #         "phase": float(phase),
    #         "d": float(d),
    #         "id": get_id()
    #     }
    #     return data
    # except:
    #     print("Error parsing XML")
    #     print(data)
    #     if not recursed:
    #         return get_enf_data(True)
    #     return None

pqwriter = pq.ParquetWriter(FILE_PATH, pa.schema([
    ("frequency", pa.float64()),
    ("time", pa.string()),
    ("phase", pa.float64()),
    ("d", pa.float64()),
    ("id", pa.int64())
]))

def append_to_parquet(data):
    df = pd.DataFrame(data, index=[data["id"]])
    df.reset_index(drop=True, inplace=True)
    pqwriter.write_table(pa.Table.from_pandas(df))

def create_parquet():
    seed = get_enf_data()
    # table = pa.Table.from_schema(pa.schema([
    #     ("frequency", pa.float64()),
    #     ("time", pa.string()),
    #     ("phase", pa.float64()),
    #     ("d", pa.float64()),
    #     ("id", pa.int64())
    # ]))
    if seed is None:
        print("Failed to get seed data")
        return
    table = pa.Table.from_pydict({
        "frequency": [seed["frequency"]],
        "time": [seed["time"]],
        "phase": [seed["phase"]],
        "d": [seed["d"]],
        "id": [seed["id"]]
    })
    pq.write_table(table, FILE_PATH)

def main():
    create_parquet()
    while True:
        data = get_enf_data()
        if data is None:
            print("Failed to get data")
            continue
        append_to_parquet(data)

def print_parquet():
    print(pq.read_metadata(FILE_PATH))


if __name__ == "__main__":
    # main()
    print_parquet()
