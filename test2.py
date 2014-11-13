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



for i in range(8):
    for j in range(7):
	m = 128 >> j;
        display.send_char(i-1, m)
        time.sleep(0.02)

#for j in range(0, 8):
#    for i in range(0, 10):
#        display.set_digit(j, i)
#        time.sleep(0.1)

count = 0
while True:
    display.set_text(str(count))
    count += 100
    time.sleep(0.02)

