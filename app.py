import requests

import os
import sys
import json

from phonenumbers import COUNTRY_CODE_TO_REGION_CODE

from dotenv import load_dotenv

from datetime import date
from datetime import datetime


def get_api_key():
    load_dotenv()
    return os.getenv('API_KEY')


def get_dialing_code(iso):
    for code, isos in COUNTRY_CODE_TO_REGION_CODE.items():
        if iso.upper() in isos:
            return code


def format_number(number):
    return number.replace(' ', '').strip('0').rstrip('\n')


def unpack(response):
    return response.json()['response']['results'][0]['carrier_name']


def get_curr_time():
    return datetime.now().strftime('%H-%M-%S')


def get_curr_date():
    return date.today()


def write_json(dictionary, filename):
    with open(filename + '.json', 'w') as outfile:
        json.dump(dictionary, outfile, indent=4)


def gen_filename(iso):
    return f'{iso}-response-{get_curr_date()}({get_curr_time()})'


def fill_dictionary(dictionary, carrier_name, phone_number):
    if carrier_name not in dictionary:
        dictionary.setdefault(carrier_name, [])
    dictionary[carrier_name].append(phone_number)
    return dictionary


def request(url, phone_number):
    request_url = url + phone_number
    response = requests.get(request_url)
    carrier_name = unpack(response)
    return carrier_name


def parse_file(dictionary, url):
    for number in open('numbers.txt', 'r'):
        formatted_number = format_number(number)
        if formatted_number:
            carrier = request(url, formatted_number)
            dictionary = fill_dictionary(
                dictionary, carrier, formatted_number)
            print(dictionary)


def main(iso):
    dictionary = {}

    api_key = get_api_key()
    dialing_code = get_dialing_code(iso)
    url = f'https://api.data247.com/v3.0?key={api_key}&api=CI&phone={dialing_code}'

    parse_file(dictionary, url)
    response_filename = gen_filename(iso)
    write_json(dictionary, response_filename)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(sys.argv[1])
    else:
        print('ISO parameter is missing!')
