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


def write_month_to_csv(out, year, month):
    for i in range(32):
        path = os.path.join("enf_data", str(year), str(month))
        if os.path.exists(path):
            write_parquet_to_csv(path, out, include_header=(i == 0))


if __name__ == "__main__":
    write_month_to_csv("enf_data/august.csv", 2024, 8)
