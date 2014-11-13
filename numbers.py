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



display.send_char(0, 0b11110110)
display.send_char(1, 0b00111111)
display.send_char(2, 0b11111011)
display.send_char(3, 0b11010110)
display.send_char(4, 0b01010100)
display.send_char(5, 0b11010001)
display.send_char(6, 0b11010111)

