# Plant Watcher

Mini security system for your plant using Raspberry Pi and Tkinter.

## Getting Started

## Setup

Make sure you have updated and upgraded your Raspberry Pi to the latest release.

### Parts

- Switch (optional)
- LED (optional)
- Moisture sensor
- DHT11 or DHT22 (temperature/humidity sensor)
- Distance sensor
- PIR sensor
- Buzzer 

### Prerequisites

Please be sure to install the following before running the program.

- Python 3.x
- RPi.GPIO
- Tkinter
- time
- adafruit_dht
- smtplib
- email.message
- board

## Usage

- Start the program by executing the main.py file or on-off.py if you would like on/off functionality.
- Once the program is running, enter your password or use your RFID tag to access your plant info.
- Place your moisture sensor in your plant's soil and DHT11 (or DHT22) near your plant.
- The GUI will automatically update the status of uour plant's surrounding temperature and humidity: also detect its moisture.
- You will be notified via email or SMS if your plant is too hot, no mmoisture detected, etc.
  - In settings you can change the wanted conditions and range of change.
- You will also be notifited if someone is too close to your plant or if your plant has been moved.
  - THe buzzer will go off if your plant has been compromised.

## Author

- **Rishan Subagar**

## License

This project is licensed under the [MIT License](LICENSE) 
