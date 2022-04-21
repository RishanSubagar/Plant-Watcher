import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    text = input('New data:')
    print("Now place your tag to write.")
    reader.write(text)
    print("Written")
finally:
    GPIO.cleanup()

try:
    print("Place tag to read data.")
    id, text = reader.read()
    print(id)
    print(text)
finally:
    GPIO.cleanup()
