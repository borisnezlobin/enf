import random
from get_data_name import get_enf_data_file_name

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


def print_info():
    with open(get_enf_data_file_name(), 'r') as file:
        lines = file.readlines()
        ergh = len(lines) - 1
        print(get_enf_data_file_name() + " has " + str(ergh) + " entries. last entry written:")
        print(lines[-1])