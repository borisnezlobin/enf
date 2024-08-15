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


def write_month_to_csv(out, year, month):
    with open(out, 'w') as file:
        file.write('')
    # no month has more than 31 (and I made it 33 just to be safe) days right...
    written_header = False
    for i in range(33):
        path = os.path.join("enf_data", str(year), str(month), str(i) + ".parquet")
        if os.path.exists(path):
            print("reading (and writing) " + path)
            write_parquet_to_csv(path, out, include_header=not written_header)
            written_header = True


if __name__ == "__main__":
    write_month_to_csv("enf_data/august.csv", 2024, 8)
