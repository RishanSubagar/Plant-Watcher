import RPi.GPIO as GPIO
import time

pir_sensor = 20
piezo = 5

GPIO.setmode(GPIO.BCM)

GPIO.setup(piezo,GPIO.OUT)

GPIO.setup(pir_sensor, GPIO.IN)

current_state = 0

try:
    while True:
        time.sleep(0.1)
        current_state = GPIO.input(pir_sensor)
        if current_state == 1:
            print(f"GPIO pin {pir_sensor} is {current_state}")
            GPIO.output(piezo,True)
            time.sleep(1)
            GPIO.output(piezo,False)
            time.sleep(2)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
