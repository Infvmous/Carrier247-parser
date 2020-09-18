import requests
from phonenumbers import COUNTRY_CODE_TO_REGION_CODE
import os
from dotenv import load_dotenv
import sys
import json


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


def parse(dictionary, url):
    for number in open('numbers.txt', 'r'):
        formatted_number = format_number(number)
        if formatted_number:
            carrier = request(url, formatted_number)
            dictionary = fill_dictionary(
                dictionary, carrier, formatted_number)
            print(dictionary)


def write_json(dictionary):
    with open('response.json', 'w') as outfile:
        json.dump(dictionary, outfile, indent=4)


def main(iso):
    dictionary = {}

    api_key = get_api_key()
    dialing_code = get_dialing_code(iso)
    url = f'api.data247.com/v3.0?key={api_key}&api=CI&phone={dialing_code}'

    parse(dictionary, url)
    write_json(dictionary)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(sys.argv[1])
    else:
        print('ISO parameter is missing!')
