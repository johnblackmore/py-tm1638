#!/usr/bin/env python

# TM1638 playground

import TM1638
import time

# These are the pins the display is connected to. Adjust accordingly.
# In addition to these you need to connect to 5V and ground.

DIO = 17
CLK = 21
STB = 22

display = TM1638.TM1638(DIO, CLK, STB)

display.enable(1)

last = 6
for j in range(1, 10):
    for i in range(6):
        display.send_char(last, 0x00)
        display.send_char(i, 128 >> j-1)
        last = i
        time.sleep(0.05)

display.set_text('')


