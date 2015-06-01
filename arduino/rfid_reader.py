# -*- encoding: utf-8 -*-
import json
import platform
import requests
import time
import serial

from dotenv import read_dotenv
from getenv import env

read_dotenv()

BAUD_RATE = 9600

PLATFORM_DARWIN = 'Darwin'
PLATFORM_LINUX = 'Linux'

PORT_DARWIN = "/dev/tty.usbmodem1411"
PORT_LINUX = "/dev/ttyUSB0"

API_USER = env('API_USER')
API_KEY = env('API_KEY')
API_URL = env('API_URL')


def getport():
    if platform.system() == PLATFORM_DARWIN:
        return PORT_DARWIN
    else:
        return PORT_LINUX


def readline(com):
    while('\r\n' not in com.readline()):
        pass
    return com.readline().rstrip()


def readtag():
    port = getport()

    result = ''
    try:
        com = serial.Serial(port, baudrate=BAUD_RATE, timeout=1)
    except serial.SerialException as e:
        result = ('error', 'could not open serial port {}: {}'.format(port, e))

    result = ('success', readline(com))
    com.close()
    return result

if __name__ == '__main__':

    try:
        while True:
            status, message = readtag()
            while status != 'success':
                status, message = readtag()

            headers = {'content-type': 'application/json'}
            url = 'http://{}/api/materials/'.format(API_URL)

            data = {'material_number': message}
            params = {'username': API_USER, 'api_key': API_KEY}
            print url
            print params

            response = requests.post(url, params=params, data=json.dumps(data), headers=headers)
            time.sleep(1)
    except KeyboardInterrupt:
        pass
