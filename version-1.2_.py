from machine import Pin,UART
import machine
import utime
from time import sleep
from dfplayermini import Player
import umail
import network
from mymodule1 import opcc
out,size=opcc("BaatCheet.txt")

ssid = ''
password = ''

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

def connect_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

sender_email = ''
sender_name =  ''
sender_password = ''
recipient_email = ['example@gmail.com','example1@gmail.com'] #more than 1 person
email_subject = 'BaatCheet English'

position=0
connect_wifi(ssid, password)

while True:
    hour=rtct()[0]
    minute=rtct()[1]
    hlist=[5,6,19]
    mlist=[0,30,0]
    al=[4,8,12,16,20,24]
    for i in range(0,len(hlist),1):
        if hlist[i]==hour and mlist[i]==minute:
            sleep(2)
            music.play(i+1)
    sleep(1)
    if minute==0:
        sleep(2)
        music.play(5)
    sleep(1)
    for k in range(0,len(al),1):
        if hour == al[k] and minute==0:
            for i in range(0,len(recipient_email),1):
                connect_wifi(ssid, password)
                smtp = umail.SMTP('smtp.mailgun.org', 465, ssl=True)
                smtp.login(sender_email, sender_password)
                smtp.to(recipient_email[i])
                smtp.write("Subject:" + email_subject + "\n")
                email_body=out[position]
                smtp.write(email_body)
                smtp.send()
                position=(position+1)%size
                smtp.quit()
                music.play(4)
    utime.sleep(50)

