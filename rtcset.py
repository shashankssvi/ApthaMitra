import machine
import utime

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
rtc_address = 0x68

def decimal_to_bcd(val):
    return (val // 10 << 4) + (val % 10)

def set_rtc_time(year, month, day, hour, minute, second):
    rtc_time = bytearray([
        decimal_to_bcd(second),
        decimal_to_bcd(minute),
        decimal_to_bcd(hour),
        decimal_to_bcd(day),
        decimal_to_bcd(month),
        decimal_to_bcd(year % 100)
    ])

    i2c.writeto_mem(rtc_address, 0, rtc_time)
    print("RTC time set manually to:", "{:02}:{:02}:{:02} - {} {} {}".format(hour, minute, second, day, month, year))

set_rtc_time(year=2000, month=1, day=00, hour=00, minute=00, second=0)
