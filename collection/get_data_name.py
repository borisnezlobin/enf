import datetime

def get_enf_data_file_name():
    return get_current_data_dir() + str(datetime.datetime.now().day) + ".parquet"

def get_current_data_dir():
    now = datetime.datetime.now()
    return "enf_data/" + str(now.year) + "/" + str(now.month) + "/"