import json
import os
from threading import Timer
from copy import deepcopy

from Adafruit_IO import Client

ADAFRUIT_IO_USERNAME = 'ngocquy25'

ADAFRUIT_IO_KEY = os.getenv("ADAFRUIT_IO_KEY")

TIME_OPEN = 5

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

relay = aio.feeds('bkad.iot-relay')
speaker = aio.feeds('bkad.iot-speaker')
lcd = aio.feeds('bkad.iot-lcd')


relay_value = {"id": "1", "name": "RELAY", "data": "", "unit": ""}
speaker_value = {"id": "2", "name": "SPEAKER", "data": "", "unit": ""}
lcd_value = {"id": "3", "name": "LCD", "data": "", "unit": ""}


def retrieve_data(msg):
    obj = json.loads(msg)
    return obj["data"]


def switch_device(on, automatic=False):
    if not on:
        relay_value['data'] = "0"
        aio.send(relay.key, json.dumps(relay_value))

        speaker_value['data'] = '0'                         # Set buzzer OFF
        aio.send(speaker.key, json.dumps(speaker_value))

        lcd_value['data'] = 'without mask'
        aio.send(lcd.key, json.dumps(lcd_value))
    else:
        relay_value['data'] = "1"
        aio.send(relay.key, json.dumps(relay_value))

        speaker_value['data'] = '1'                         # Set buzzer ON
        aio.send(speaker.key, json.dumps(speaker_value))

        lcd_value['data'] = 'with mask'
        aio.send(lcd.key, json.dumps(lcd_value))

    if automatic:
        print('Close the door automatically')


def open_door(relay_data):
    is_on = relay_data == 1
    print('Relay value is:', relay_data, is_on)

    switch_device(is_on)

    if is_on:
        r = Timer(TIME_OPEN, switch_device, (False, True))
        r.start()
