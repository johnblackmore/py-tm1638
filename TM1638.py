#!/usr/bin/env python
# vim: set fileencoding=utf-8 expandtab shiftwidth=4 tabstop=4 softtabstop=4:

# A library for controlling TM1638 displays from a Raspberry Pi
# Based on original work in C from https://code.google.com/p/tm1638-library/
# Converted to python by Jacek Fedorynski <jfedor@jfedor.org> (common cathode)
# Converted for TM1638 common anode by John Blackmore <john@johnblackmore.com>

import RPi.GPIO as GPIO

GPIO.setwarnings(False) # suppresses warnings on RasPi


class TM1638(object):

    FONT = {
        '0': 0b00111111,
        '1': 0b00000110,
        '2': 0b01011011,
        '3': 0b01001111,
        '4': 0b01100110,
        '5': 0b01101101,
        '6': 0b01111101,
        '7': 0b00000111,
        '8': 0b01111111,
        '9': 0b01101111,
        'a': 0b01110111,
        'b': 0b01111100,
        'c': 0b01011000,
        'd': 0b01011110,
        'e': 0b01111001,
        'f': 0b01110001,
        'g': 0b01011111,
        'h': 0b01110100,
        'i': 0b00010000,
        'j': 0b00001110,
        'l': 0b00111000,
        'n': 0b01010100,
        'o': 0b01011100,
        'p': 0b01110011,
        'r': 0b01010000,
        's': 0b01101101,
        't': 0b01111000,
        'u': 0b00111110,
        'y': 0b01101110,
        'C': 0b00111001,
        'P': 0b01110011,
        'U': 0b00111110
    }

    def __init__(self, dio, clk, stb):
        self.dio = dio
        self.clk = clk
        self.stb = stb

    def enable(self, intensity=7):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dio, GPIO.OUT)
        GPIO.setup(self.clk, GPIO.OUT)
        GPIO.setup(self.stb, GPIO.OUT)

        GPIO.output(self.stb, True)
        GPIO.output(self.clk, True)

        self.send_command(0x40)
        self.send_command(0x80 | 8 | min(7, intensity))

        GPIO.output(self.stb, False)
        self.send_byte(0xC0)
        for i in range(16):
            self.send_byte(0x00)
        GPIO.output(self.stb, True)

    def send_command(self, cmd):
        GPIO.output(self.stb, False)
        self.send_byte(cmd)
        GPIO.output(self.stb, True)

    def send_data(self, addr, data):
        self.send_command(0x44)
        GPIO.output(self.stb, False)
        self.send_byte(0xC0 | addr)
        self.send_byte(data)
        GPIO.output(self.stb, True)

    def send_byte(self, data):
        for i in range(8):
            GPIO.output(self.clk, False)
            GPIO.output(self.dio, (data & 1) == 1)
            data >>= 1
            GPIO.output(self.clk, True)

    def set_led(self, n, color):
        self.send_data((n << 1) + 1, color)

    def send_char(self, pos, data, dot=False):
        self.send_data(pos << 1, data | (128 if dot else 0))

    def set_digit(self, pos, digit, dot=False):
        for i in range(0, 6):
            self.send_char(i, self.get_bit_mask(pos, digit, i), dot)
    
    def get_bit_mask(self, pos, digit, bit):
        return ((self.FONT[digit] >> bit) & 1) << pos

    def set_text(self, text):
        dots = 0b00000000
        pos = text.find('.')
        if pos != -1:
            dots = dots | (128 >> pos+(8-len(text)))
            text = text.replace('.', '')

        self.send_char(7, self.rotate_bits(dots))
        text = text[0:8]
        text = text[::-1]
        text += " "*(8-len(text))
        for i in range(0, 7):
            byte = 0b00000000;
            for pos in range(8):
                c = text[pos]
                if c == 'c':
                    byte = (byte | self.get_bit_mask(pos, c, i))
                elif c != ' ':
                    byte = (byte | self.get_bit_mask(pos, c, i))
            self.send_char(i, self.rotate_bits(byte))

    def receive(self):
        temp = 0
        GPIO.setup(self.dio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for i in range(8):
            temp >>= 1
            GPIO.output(self.clk, False)
            if GPIO.input(self.dio):
                temp |= 0x80
            GPIO.output(self.clk, True)
        GPIO.setup(self.dio, GPIO.OUT)
        return temp

    def get_buttons(self):
        keys = 0
        GPIO.output(self.stb, False)
        self.send_byte(0x42)
        for i in range(4):
            keys |= self.receive() << i
        GPIO.output(self.stb, True)
        return keys

    def rotate_bits(self, num):
        for i in range(0, 4):
            num = self.rotr(num, 8)
        return num

    def rotr(self, num, bits):
        num &= (2**bits-1)
        bit = num & 1
        num >>= 1
        if bit:
            num |= (1 << (bits-1))
        return num
