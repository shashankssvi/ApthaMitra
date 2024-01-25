import machine
import utime

i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21))
rtc_address = 0x68       #changes for different module

def bcd_to_decimal(val):
    return (val >> 4) * 10 + (val & 0x0F)

def rtct():
    data = i2c.readfrom_mem(rtc_address, 0, 7)
    seconds = bcd_to_decimal(data[0] & 0x7F) 
    minutes = bcd_to_decimal(data[1] & 0x7F)  
    hours = bcd_to_decimal(data[2] & 0x3F)
    return hours,minutes,seconds

while True:
    hour=rtct()[0]
    minute=rtct()[1]
    seconds=rtct()[2]
    print("RTC time set manually to:", "{:02}:{:02}:{:02} ".format(hour, minute, seconds))
    utime.sleep(2)

