import RPi.GPIO as GPIO
import time
import adafruit_dht
from board import *
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN) #button
GPIO.setup(19,GPIO.OUT) #led

DHT_pin = D16 # temp/humidity sensor
dhtDevice = adafruit_dht.DHT11(DHT_pin, use_pulseio=False)

toggle_val = 1

# clear console function
clear = lambda: os.system('clear')

def toggle_functions():
    if (toggle_val % 2) == 0:
        # Turn on LED
        GPIO.output(19, GPIO.HIGH)
        
        import main
    else:
        GPIO.output(19, GPIO.LOW) # Off LED
    

while True:
    if (GPIO.input(21)):
        toggle_val += 1

    else:
        pass

    time.sleep(0.12) # Button delay
    
    toggle_functions()
