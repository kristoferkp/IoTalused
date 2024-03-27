import network
from machine import Pin, SoftI2C
import ssd1306
import dht
import bmp280
try:
  import usocket as socket
except:
  import socket


WiFi_SSID = "SSID" 
WiFi_PASS = "PASSWORD"

displayI2C = SoftI2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 64, displayI2C)
  
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(WiFi_SSID, WiFi_PASS)
        while not wlan.isconnected():
            pass                              
    print('network config:', wlan.ifconfig())
    
    display.text("IP address: ", 0, 0, 1)
    display.text(wlan.ifconfig()[0], 0, 10, 1)
    display.show()

do_connect()

dht22 = dht.DHT22(Pin(19))
bus = SoftI2C(scl=Pin(27), sda=Pin(26)) 
bmp = bmp280.BMP280(bus)

led = Pin(22, Pin.OUT)
led.on()

button = Pin(14, Pin.IN)
