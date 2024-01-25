from machine import Pin,UART
import machine
import utime
from dfplayermini import Player

from mymodule1 import opcc
utime.sleep(2)
out,size=opcc("BaatCheet.txt")
utime.sleep(2)

music = Player(pin_TX=17, pin_RX=16)
music.volume(20)

i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21))
rtc_address = 0x68

def bcd_to_decimal(val):
    return (val >> 4) * 10 + (val & 0x0F)

def rtct():
    data = i2c.readfrom_mem(rtc_address, 0, 7)
    seconds = bcd_to_decimal(data[0] & 0x7F)
    minutes = bcd_to_decimal(data[1] & 0x7F)
    hours = bcd_to_decimal(data[2] & 0x3F)
    return hours,minutes

while True:
    hour=rtct()[0]
    minute=rtct()[1]
    hlist=[5,6,19]
    mlist=[0,30,0]
    for i in range(0,len(hlist),1):
        if hlist[i]==hour and mlist[i]==minute:
            music.play(i+1)
    if minute == 0:
        music.play(5)
    utime.sleep(60)
