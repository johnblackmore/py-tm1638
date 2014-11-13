#!/usr/bin/env python

# CPU Temp
# Grabs the RasPi cpu temp and outputs to TM1638 display to 1 decimal place

import TM1638
import time
import os

# These are the pins the display is connected to. Adjust accordingly.
# In addition to these you need to connect to 5V and ground.

DIO = 17
CLK = 21
STB = 22

display = TM1638.TM1638(DIO, CLK, STB)
display.enable(1)

while True:
    res = os.popen('cat /sys/class/thermal/thermal_zone0/temp').readline()
    res = res.replace('\n', '')
    #print "%0.1fc" % (float(res)/1000)
    display.set_text("%0.1fc" % (float(res)/1000))
    time.sleep(2)

