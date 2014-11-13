#!/usr/bin/env python

# Load Average
# Grabs the RasPi 1 minute load average outputs to TM1638 display, updates every 2 secs

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
    res = os.popen('uptime').readline()
    res = res.replace('\n', '')
    pos = res.index('age:')
    load = res[pos+5:pos+9]
    display.set_text("load %s" % (load))
    time.sleep(2)

