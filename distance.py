import RPi.GPIO as GPIO
import time
import smtplib
from email.message import EmailMessage

while True:
    try:
        GPIO.setmode(GPIO.BCM)

        PIN_TRIGGER = 4
        PIN_ECHO = 17

        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        print("Waiting for sensor to settle")

        time.sleep(2)

        print("Calculating distance")

        GPIO.output(PIN_TRIGGER, GPIO.HIGH)

        time.sleep(0.00001)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time

        distance = round(pulse_duration * 17150, 2)

        print(f"Distance: {distance}cm")
    finally:
        GPIO.cleanup()

    def email_alert(subject, body, to):
        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = subject
        msg['to'] = to

        user = "watcherplant@gmail.com"
        msg['from'] = user
        password = "istmegkvutekvllc"

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(user, password)
        server.send_message(msg)

        server.quit()

    if distance <= 3.5:
        email_alert("Hey", "Hello World", "your_email")
        email_alert("Hey", "Hello World", "phone_number_cellular_email") # using phone number
