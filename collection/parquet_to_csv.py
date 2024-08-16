import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
import os

def parquet_to_csv(file_name, include_header=True):
    data = pd.read_parquet(file_name)
    return data.to_csv(header=include_header)

def write_parquet_to_csv(parquet, out, include_header=True):
    with open(out, 'a') as file:
        file.write(parquet_to_csv(parquet, include_header=include_header))
        file.close()

def csv_to_table(csv):
    table = pa.csv.read_csv(csv)
    return table

def write_csv_to_parquet(csv, writer):
    writer.write_table(csv_to_table(csv))


def write_month_to_parquet(out, year, month):
    pq_writer = pq.ParquetWriter(out, pa.schema([
        ("frequency", pa.float()),
        ("time", pa.string()),
        ("phase", pa.float()),
        ("d", pa.float())
    ]))
    # no month has more than 31 (and I made it 33 just to be safe) days right...
    for i in range(33):
        path = os.path.join("enf_data", str(year), str(month), str(i) + ".csv")
        # todo (have class)
        if os.path.exists(path):
            write_csv_to_parquet(path, pq_writer)
    pq_writer.close()


if __name__ == "__main__":
    # write_month_to_csv("enf_data/august.csv", 2024, 8)
    write_parquet_to_csv("enf_data/2024/8/14.parquet", "enf_data/fourtheenth.csv", include_header=True)
