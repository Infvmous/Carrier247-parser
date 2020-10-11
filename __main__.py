import os
import sys
import json
import requests

from phonenumbers import COUNTRY_CODE_TO_REGION_CODE
from dotenv import load_dotenv
from datetime import date, datetime


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


def write_json(dictionary, filename):
    with open(filename, 'w') as outfile:
        json.dump(dictionary, outfile, indent=4)


def gen_filename(iso):
    return f'{iso}-response-{date.today()}({get_curr_time()}).json'


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


def parse_file(dictionary, url, number_limit):
    counter = 0
    for number in open('numbers.txt', 'r'):
        if counter == number_limit:
            break
        formatted_number = format_number(number)
        if formatted_number:
            carrier = request(url, formatted_number)
            dictionary = fill_dictionary(
                dictionary, carrier, formatted_number)
            counter += 1
            print(dictionary)


def main(iso, number_limit=None):
    dictionary = {}

    api_key = get_api_key()
    dialing_code = get_dialing_code(iso)
    url = f'https://api.data247.com/v3.0?key={api_key}&api=CI&phone={dialing_code}'

    parse_file(dictionary, url, number_limit)
    response_filename = gen_filename(iso)
    write_json(dictionary, response_filename)
    print('\nWritten complete to ' + response_filename)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) == 3:
        main(sys.argv[1], int(sys.argv[2]))
    else:
        print('ISO parameter is missing!')
