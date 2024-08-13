import datetime

def get_enf_data_file_name():
    return "collection/enf_data_" + str(datetime.datetime.now().month) + "_" + str(datetime.datetime.now().year) + ".parquet"