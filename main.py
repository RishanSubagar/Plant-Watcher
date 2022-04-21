import RPi.GPIO as GPIO
from tkinter import *
import time
import smtplib
from email.message import EmailMessage
import adafruit_dht
from board import *
import password # password window

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Senosrs
moist_sensor_pin = 12 # moisture sensor
GPIO.setup(moist_sensor_pin, GPIO.IN)

DHT_pin = D16 # temp/humidity sensor
dhtDevice = adafruit_dht.DHT11(DHT_pin, use_pulseio=False)

pir_sensor = 20 # motion sensor
piezo = 5 # buzzer
GPIO.setup(piezo,GPIO.OUT)
GPIO.setup(pir_sensor, GPIO.IN)
current_state = 0 # set state to no motion detected

# Settings
temp_set = 22.0
temp_range = 3.0

humid_set = 35.0
humid_range = 3.0

dist_set = 3.5

time_val = 0

# Info
email = "rishans48@gmail.com"
number = "2899438471@txt.freedommobile.ca"

##############################################################################


# Send email/SMS
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


# Check moisture in plant
def callback(moist_sensor_pin):
    if GPIO.input(moist_sensor_pin):
        print("No water detected")
        moist_status = "No water detected"
        moist_box.config(text=moist_status) # Configure box
    else:
        print("Water detected.")
        moist_status = "Water detected"
        moist_box.config(text=moist_status) # Configure box


# Calculate distance between person and plant
def distance_sensor():
    global distance

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

        time.sleep(0.1)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time

        distance = round(pulse_duration * 17150, 2)

        print(f"Distance: {distance}cm")

        time.sleep(1)

        # Send msg if too close to plant
        if distance <= dist_set:
            email_alert("Suspicious Activity", "Somebody is getting really close to your plant!", email)
            email_alert("Suspicious Activity", "Somebody is getting really close to your plant!", number) # <- using phone number
        else:
            pass

        root.after(10, distance_sensor)

        return distance

    finally:
        GPIO.cleanup(PIN_TRIGGER)


# Get temperature and humidity from sensor
def temp_humid():
    global temperature_c, humidity
    try:
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity

        # Configure boxes
        temp_box.config(text=f"{temperature_c}" + "° C")
        humid_box.config(text=f"{humidity}" + "%")

        # Update every 0.1 seconds
        time.sleep(0.1)

        # Rerun function
        root.after(10, temp_humid)

        return temperature_c, humidity

    except RuntimeError as error:
        print(error.args[0])

        # Configure boxes
        temp_box.config(text="One Second")
        humid_box.config(text="One Second")

        root.after(5, temp_humid)

    except Exception as error:
        root.after(5, temp_humid)
        

    time.sleep(1)


def motion_alarm():
    try:
        time.sleep(0.1)
        current_state = GPIO.input(pir_sensor)
        if current_state == 1:
            print(f"GPIO pin {pir_sensor} is {current_state}")
            GPIO.output(piezo,True)
            time.sleep(1)
            GPIO.output(piezo,False)
            time.sleep(2)
        root.after(5, motion_alarm)
    except KeyboardInterrupt:
        pass
    except RuntimeError:
        print("something wrong PIR")
    finally:
        GPIO.cleanup(pir_sensor)


def condition_change():
    global temp_state, humid_state

    temperature_c = dhtDevice.temperature
    humidity = dhtDevice.humidity

    temp_state = None
    humid_state = None

    # Temperature change
    if temperature_c < temp_set - temp_range:
        temp_box.config(fg="blue")
        temp_state = "cold"
    elif temperature_c > temp_set + temp_range:
        temp_box.config(fg="red")
        temp_state = "hot"    
    else:
        temp_box.config(fg="black")
        temp_state = None

    # HUmidity Change
    if humidity < humid_set - humid_range:
        humid_box.config(fg='blue')
        humid_state = "cold"
    elif humidity > humid_set + humid_range:
        humid_box.config(fg='red')
        humid_state = "hot"
    else:
        humid_box.config(fg='black')
        humid_state = None

    root.after(100, condition_change)


def send_msg():
    if time_val % 10 == 0:
        # Temperature change
        if temp_state == 'cold':
            email_alert("Too Cold!", "Your plant is freezing", number)
            time.sleep(100)
        elif temp_state == 'hot':
            email_alert("Too Hot!", "Your plant is on fire", number)
            time.sleep(100)
        else:
            temp_box.config(fg="black")

        # HUmidity Change
        if humid_state == 'cold':
            email_alert("Not Humid Enough", "Your plant needs a more humid environment", number)
            time.sleep(100)
        elif humid_state == 'hot':
            email_alert("So Humid!", "Your plant needs a less humid environment", number)
            time.sleep(100)
        else:
            humid_box.config(fg='black')
    else:
        pass


def timer():
    global time_val
    time_val += 1
    time.sleep(1)
    root.after(1000, timer)


def set_vals():
    global temp_set, temp_range, humid_set, humid_range, dist_set

    # Set values to what is in entries
    temp_set = ts_val.get()
    temp_range = tr_val.get()
    humid_set = hs_val.get()
    humid_range = hr_val.get()
    dist_set = ds_val.get()

    # Update condition change function
    condition_change()


def settings():
    global ts_val, tr_val, hs_val, hr_val, ds_val, settings_win

    settings_win = Toplevel(root, height=300, width=550)
    settings_win.title("Settiings")

    bg = "#2e2e2e"
    fg= "white"
    settings_win.config(bg=bg)

    # Labels
    device_lbl = Label(settings_win, text="Device:", font=24, bg=bg, fg=fg)
    device_lbl.place(x=10, y=10)

    change_lbl = Label(settings_win, text="Change:", font=24, bg=bg, fg=fg)
    change_lbl.place(x=200, y=10)

    temp = Label(settings_win, text="Temperature", font=24, bg=bg, fg=fg)
    temp.place(x=10, y=50)

    humid = Label(settings_win, text="Humidity", font=24, bg=bg, fg=fg)
    humid.place(x=10, y=90)

    dist = Label(settings_win, text="Distance", font=24, bg=bg, fg=fg)
    dist.place(x=10, y=130)

    # Entry Labels
    ts = Label(settings_win, text="Set:", font=24, bg=bg, fg=fg)
    ts.place(x=200, y=50)

    tr = Label(settings_win, text="Range:", font=24, bg=bg, fg=fg)
    tr.place(x=300, y=50)

    hs = Label(settings_win, text="Set:", font=24, bg=bg, fg=fg)
    hs.place(x=200, y=90)

    hr = Label(settings_win, text="Range:", font=24, bg=bg, fg=fg)
    hr.place(x=300, y=90)

    ds = Label(settings_win, text="Set:", font=24, bg=bg, fg=fg)
    ds.place(x=200, y=130)

    # Entry boxes
    ts_val = IntVar()
    hs_val = IntVar()
    tr_val = IntVar()
    hr_val = IntVar()
    ds_val = IntVar()

    ts_entry = Entry(settings_win, textvariable=ts_val, width=5)
    ts_entry.place(x=245, y=50)

    tr_entry = Entry(settings_win, textvariable=tr_val, width=5)
    tr_entry.place(x=370, y=50)

    hs_entry = Entry(settings_win, textvariable=hs_val, width=5)
    hs_entry.place(x=245, y=90)

    hr_entry = Entry(settings_win, textvariable=hr_val, width=5)
    hr_entry.place(x=370, y=90)

    ds_entry = Entry(settings_win, textvariable=ds_val, width=5)
    ds_entry.place(x=245, y=130)

    # Insert data
    ts_entry.insert(0, temp_set)
    tr_entry.insert(0, temp_range)
    hs_entry.insert(0, humid_set)
    hr_entry.insert(0, humid_range)
    ds_entry.insert(0, dist_set)

    # Set button
    set_btn = Button(settings_win, text="Set", command=set_vals)
    set_btn.place(x=200, y=200)


####################################################################

# Create window
root = Tk()
root.title("Plant Watcher")
root.geometry("800x200")
root.resizable(False, False)

bg_cololur = "#1d6630"
root.config(bg=bg_cololur)

# Title
title = Label(root, text="Plant Watcher", font=("Helvetica", 32, "bold"), fg="white", bg=bg_cololur)
title.pack(pady=10, anchor=N)

# Labels
temp_lbl = Label(text=" Temperature ", font=24, bg="cornsilk")
temp_lbl.pack(padx=80, pady=10, anchor=N, side=LEFT)

humid_lbl = Label(text=" Humidity ", font=24, bg="cornsilk")
humid_lbl.pack(padx=80, pady=10, anchor=N, side=LEFT)

moist_lbl = Label(text=" Moisture ", font=24, bg="cornsilk")
moist_lbl.pack(padx=80, pady=10, anchor=N, side=LEFT)

# Updated Labels
temp_box = Label(root, text='', width=15, justify="center", bg="white", fg="black")
temp_box.place(x=70, y=120)

humid_box = Label(root, text='', width=15, justify="center", bg="white", fg="black")
humid_box.place(x=330, y=120)

moist_box = Label(root, text='Place Sensor', width=15, justify="center", bg="white", fg="black")
moist_box.place(x=575, y=120)

# Menu
upper_menu = Menu(root)
root.config(menu=upper_menu)
options_menu = Menu(upper_menu)
upper_menu.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Settings", command=settings)

# Call functions:
root.after(1000, distance_sensor) 
root.after(5, temp_humid) 
root.after(5, motion_alarm)

GPIO.add_event_detect(moist_sensor_pin, GPIO.BOTH, bouncetime = 300)
GPIO.add_event_callback(moist_sensor_pin, callback)

condition_change()

timer()

send_msg()

root.mainloop()
