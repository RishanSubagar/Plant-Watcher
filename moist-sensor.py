import signal
import sys
import time
import spidev
import RPi.GPIO as GPIO

# NEED CHIP TO READ ANALOG DATA

"""# Pin 12 on Raspberry Pi corresponds to GPIO 22
LED1 = 12
spi_ch = 0
# Enable SPI
spi = spidev.SpiDev(0, spi_ch)
spi.max_speed_hz = 1200000
# to use Raspberry Pi GPIO numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# set up GPIO output channel
GPIO.setup(LED1, GPIO.OUT)
def close(signal, frame):
    GPIO.output(LED1, 0)
    sys.exit(0)
signal.signal(signal.SIGINT, close)
def valmap(value, istart, istop, ostart, ostop):
    value = ostart + (ostop - ostart) * ((value - istart) / (istop - istart))
    if value > ostop:
       value = ostop
    return value
def get_adc(channel):
    # Make sure ADC channel is 0 or 1
    if channel != 0:
        channel = 1
    # Construct SPI message
    #  First bit (Start): Logic high (1)
    #  Second bit (SGL/DIFF): 1 to select single mode
    #  Third bit (ODD/SIGN): Select channel (0 or 1)
    #  Fourth bit (MSFB): 0 for LSB first
    #  Next 12 bits: 0 (don't care)
    msg = 0b11
    msg = ((msg << 1) + channel) << 5
    msg = [msg, 0b00000000]
    reply = spi.xfer2(msg)
    # Construct single integer out of the reply (2 bytes)
    adc = 0
    for n in reply:
        adc = (adc << 8) + n
    # Last bit (0) is not part of ADC value, shift to remove it
    adc = adc >> 1
    # Calculate voltage form ADC value
    # considering the soil moisture sensor is working at 5V
    voltage = (5 * adc) / 1024
    return voltage
if __name__ == '__main__':
    # Report the channel 0 and channel 1 voltages to the terminal
    try:
        while True:
            adc_0 = get_adc(0)
            adc_1 = get_adc(1)
            sensor1 = round(adc_0, 2)
            if sensor1 < 0.5:
                moisture1 = 0
            else:
                moisture1 = round(valmap(sensor1, 5, 3.5, 0, 100), 0)
            print(f"Soil Moisture Sensor 1: {moisture1}%")
            
            if moisture1 < 40:
                GPIO.output(LED1, 1)
            else:
                GPIO.output(LED1, 0)
            time.sleep(0.5)
    finally:
        GPIO.cleanup()"""


import RPi.GPIO as GPIO
import time

moist_sensor_pin = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(moist_sensor_pin, GPIO.IN)

def callback(moist_sensor_pin):
    if GPIO.input(moist_sensor_pin):
        print("No water detected")
    else:
        print("Water detected.")

GPIO.add_event_detect(moist_sensor_pin, GPIO.BOTH, bouncetime = 300)
GPIO.add_event_callback(moist_sensor_pin, callback)

while True:
    time.sleep(1)
