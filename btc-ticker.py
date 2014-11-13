#!/usr/bin/env python
# vim: set fileencoding=utf-8 expandtab shiftwidth=4 tabstop=4 softtabstop=4:

# Bitcoin price ticker for a TM1638 display

# Jacek Fedorynski <jfedor@jfedor.org>

import TM1638
import urllib2
import json
import traceback
import time

# These are the pins the display is connected to. Adjust accordingly.
# In addition to these you need to connect to 5V and ground.

DIO = 17
CLK = 21
STB = 22

display = TM1638.TM1638(DIO, CLK, STB)

display.enable()

source = 'https://www.bitstamp.net/api/ticker/'

while True:
    try:
        data = json.loads(urllib2.urlopen(source).read())
        dotpos = data['last'].find(".")-1
        text = (data['last'].replace(".",""))[0:8]
        for i in range(8-len(text)):
            display.send_char(i, 0)
        for i in range(len(text)):
            display.set_digit(8-len(text)+i, int(text[i]), i==dotpos)
    except:
        print traceback.format_exc()
    time.sleep(30)

