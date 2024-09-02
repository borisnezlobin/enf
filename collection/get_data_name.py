import datetime

def get_enf_data_file_name():
    return get_current_data_dir() + str(datetime.datetime.now().day) + ".csv"

def get_error_file_name():
    return get_current_data_dir() + "error.csv"

def get_current_data_dir():
    now = datetime.datetime.now()
    return "/home/random/enf/collection/enf_data/" + str(now.year) + "/" + str(now.month) + "/"
