import random
import datetime
from get_data_name import get_enf_data_file_name, get_error_file_name, get_current_data_dir
import os

def log(s):
    print(
        datetime.datetime.now().strftime("(%d/%m %H:%M:%S) ") +
        str(s)
    )

UA_LIST = [
    'Dalvik/2.1.0 (Linux; U; Android 11; V2026 Build/RP1A.200720.012)',
    'Mozilla/5.0 (Linux; U; Android 8.1.0; SM-G610F Build/M1AJQ; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36 OPR/51.0.2254.150807',
    'Dalvik/1.6.0 (Linux; U; Android 4.4.4; KC-01 Build/100.0.1a20)',
    'Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.116 Mobile Safari/537.36 EdgA/45.04.4.4995',
    'Mozilla/5.0 (Linux; Android 10; ELE-L29 Build/HUAWEIELE-L29; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.101 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; arm_64; Android 10; SM-G965F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 YaBrowser/20.4.4.76.00 SA/1 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 5.1.1; HUAWEI P8max Build/HUAWEIDAV-701L; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 9; MAR-LX3Am) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.50 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-A920F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 9; KFONWI) AppleWebKit/537.36 (KHTML, like Gecko) Silk/85.2.3 like Chrome/85.0.4183.101 Safari/537.36'
]

def getUA():
    return random.choice(UA_LIST)


def get_seconds_from_timestamp(timestamp):
    return int(timestamp.split(":")[-1])

def seconds_to_format(seconds):
    ret = str(seconds % 60) + "s"
    if (seconds >= 60):
        ret = str((seconds // 60) % 60) + "m " + ret
    if (seconds >= 60 * 60):
        ret = str((seconds // (60 * 60)) % 24) + "h " + ret

    if (seconds >= 60 * 60 * 24):
        ret = str(seconds // (60 * 60 * 24)) + "d " + ret
    
    return ret


def print_info():
    today = datetime.datetime.now().day
    max_error = -1
    max_error_day = -1
    total_error = 0

    errors = []
    if os.path.exists(get_error_file_name()):
        with open(get_error_file_name(), 'r') as err:
            errors = err.readlines()

    for i in range(1, today + 1):
        num_lines = 0
        day_path = get_current_data_dir() + str(i) + ".csv"
        if not os.path.exists(day_path):
            continue
        with open(day_path, 'r') as file:
            lines = file.readlines()
            num_lines = len(lines)


        day_errors = [e for e in errors if e[0] == str(i) or e[0:2] == str(i)]

        small_errors = len([a for a in day_errors if a.split(",")[2].strip() == '0'])
        duration = 0
        for j in day_errors:
            duration += int(j.split(",")[-1])

        p_error = ((duration / (24 * 60 * 60 * 1000)) * 100)
        if p_error > max_error:
            max_error = p_error
            max_error_day = i
        total_error += duration

        if i == today:
            print("\n\n+++ TODAY +++\n")
            print(get_enf_data_file_name() + " has " + str(num_lines) + " entries.")
            print("that's about " + seconds_to_format(num_lines) + " of data")
            print("data loss:")
            print("\taveraged values (small errors): " + str(small_errors))
            print("\tlarge errors (>2s) that we couldn't average: " + str(len(day_errors) - small_errors))
            print("\tthat's " + seconds_to_format(duration))
        else:
            print(
                str(i) + ": " + str(len(day_errors)) + " (" + str(small_errors) + " small). " + str(duration // 1000) + "s of error ("
                + str(p_error) + "%)"
            )
    
    print("\n\n+++ ERROR SUMMARY +++\n")
    print("total error: " + seconds_to_format(total_error))
    print("highest error was on day " + str(max_error_day) + ": " + str(max_error) + "%.")

if __name__ == "__main__":
    print_info()
