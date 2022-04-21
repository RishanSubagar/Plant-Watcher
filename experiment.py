import RPi.GPIO as GPIO
import time

mic_pin = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(mic_pin, GPIO.IN)

def callback(mic_input):
    if GPIO.input(mic_pin):
        print("Sound detected ^_*")
    else:
        print("Sound detected ^_*")
        
GPIO.add_event_detect(mic_pin, GPIO.BOTH, bouncetime=300) # let us know when GPIO is HIGH or LOW
GPIO.add_event_callback(mic_pin, callback) # assign function to mic_pin, run funtion on change

while True:
    time.sleep(1)
