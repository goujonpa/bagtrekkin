# -*- encoding: utf-8 -*-
import collections
import json
import os
import platform
import requests
import serial
import sys
import time

from dotenv import read_dotenv
from getenv import env

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

read_dotenv(os.path.join(BASE_DIR, '/arduino/.env'))

STEPS = ['-', '/', '|', '\\']

BAUD_RATE = 9600

PLATFORM_DARWIN = 'Darwin'
PLATFORM_LINUX = 'Linux'

PORT_DARWIN = "/dev/tty.usbmodem1411"
PORT_LINUX = "/dev/ttyUSB0"

API_USER = env('API_USER')
API_KEY = env('API_KEY')
API_URL = env('API_URL')


def logr(message):
    sys.stdout.flush()
    sys.stdout.write('\r%s' % message)


def logn(message):
    sys.stdout.flush()
    sys.stdout.write('\n%s' % message)


def logs(message):
    sys.stdout.write(' [%s]' % message)


def send(number):
    headers = {'content-type': 'application/json'}
    url = 'http://{}/api/v1/luggage/'.format(API_URL)
    params = {'username': API_USER, 'api_key': API_KEY}
    data = {'material_number': number}

    logs('Sending')
    response = requests.post(
        url,
        params=params,
        data=json.dumps(data),
        headers=headers
    )
    logs('Sent')
    logn('')
    response.raise_for_status()


class TagReader():
    last_read = 0

    def __init__(self, *args, **kwargs):
        self.port = self._getport()
        self.buf = collections.deque(maxlen=10)

    def __enter__(self):
        try:
            self.com = serial.Serial(self.port, baudrate=BAUD_RATE, timeout=1)
            logn('Serial Com Connected\n')
        except (serial.SerialException, OSError), e:
            raise serial.SerialException(
                'could not open serial port {}: {}'.format(self.port, e)
            )
        return self

    def __exit__(self, type, value, traceback):
        logn('Serial Com Disonnected\n')
        if not self.com.closed:
            self.com.close()

    def _readline(self):
        return self.com.readline().strip()

    def _getport(self):
        if platform.system() == PLATFORM_DARWIN:
            return PORT_DARWIN
        else:
            return PORT_LINUX

    def readtag(self):
        try:
            if time.time() >= TagReader.last_read + 10:
                number = self._readline()
                if number and number not in self.buf:
                    self.buf.append(number)
                    logr('Read %s' % number)
                    TagReader.last_read = time.time()
                    return number
            return None
        except serial.SerialException, e:
            raise serial.SerialException(
                'could not readline from serial port {}: {}'.format(self.port, e)
            )


if __name__ == '__main__':
    try:
        with TagReader() as tagreader:
            i = 0
            try:
                while True:
                    logr('Reading %s' % STEPS[i % 4])
                    number = tagreader.readtag()
                    if number:
                        send(number)
                    time.sleep(0.1)
                    i += 1
            except (serial.SerialException, requests.exceptions.RequestException), e:
                logn(e)
    except KeyboardInterrupt:
        pass
