# -*- encoding: utf-8 -*-
import json
import platform
import time
import serial

BAUD_RATE = 9600

PLATFORM_DARWIN = 'Darwin'
PLATFORM_LINUX = 'Linux'

PORT_DARWIN = "/dev/tty.usbmodem1411"
PORT_LINUX = "/dev/ttyUSB0"


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
    readtag()
