#smokesensor 
#2-vcc 6-GND 11-Output
#pip commands
#sudo apt update
#sudo apt install python3-rpi.gpio
#pip3 install RPi.GPIO
# LED:
# Pin 13→ Resistor → LED long short → Pin 9 (GND)
import RPi.GPIO as GPIO
import time
SMOKE_DO = 17      # MQ module DO pin connected to GPIO17
LED_PIN = 27       # LED connected to GPIO27
GPIO.setmode(GPIO.BCM)
GPIO.setup(SMOKE_DO, GPIO.IN)          
GPIO.setup(LED_PIN, GPIO.OUT)
print("Smoke Sensor (MQ) is warming up... Please wait 20 seconds")
GPIO.output(LED_PIN, GPIO.LOW)
time.sleep(20)
print("System Ready")
print("Monitoring smoke/gas... (Press CTRL+C to exit)")
try:
    while True:
        smoke_detected = (GPIO.input(SMOKE_DO) == 0)

        if smoke_detected:
            print("SMOKE/GAS DETECTED!")
            GPIO.output(LED_PIN, GPIO.HIGH)
        else:
            print("Air is clean")
            GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting... Cleaning up GPIO")
#-----LED -
#PIN CONNECTIONS
#19 - MOSI (DIN)
#23 - CLK (CLK)
#24 - CE0 (CS)
#2  - VCC (5V)1
#6  - GND
#pip commands
#sudo apt update
#pip3 install luma.led_matrix
#pip3 install luma.core
#pip3 install pillow
#sudo raspi-config  (enable SPI)
from luma.core.interface.serial import spi, noop
from luma.led_matrix.device import max7219
from luma.core.render import canvas
from luma.core.legacy import show_message, text
from luma.core.legacy.font import proportional, CP437_FONT
import time

serial = spi(port=0, device=0, gpio=noop())

device = max7219(serial, cascaded=1, block_orientation=90, rotate=0)
device.contrast(50)

print("MAX7219 8x8 Matrix Ready...")
def blink_dot():
    with canvas(device) as draw:
        draw.point((3,3), fill="white")
        draw.point((4,3), fill="white")
        draw.point((4,4), fill="white")
        draw.point((3,4), fill="white")
def diagonal_line():
    with canvas(device) as draw:
        for i in range(8):
            draw.point((i, i), fill="white")
def border_box():
    with canvas(device) as draw:
        for x in range(8):
            draw.point((x, 0), fill="white")
            draw.point((x, 7), fill="white")
        for y in range(8):
            draw.point((0, y), fill="white")
            draw.point((7, y), fill="white")
def show_letter_A():
    with canvas(device) as draw:
        points = [(1,7),(1,6),(1,5),(1,4),(1,3),(1,2),(1,1),(2,0),(3,0),(4,0),(5,0),
                  (6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),
                  (2,7),(2,6),(2,5),(2,4),(2,3),(2,2),(2,1),(3,1),(4,1),(5,1),
                  (5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(3,4),(4,4)]
        for p in points:
            draw.point(p, fill="white")
try:
    while True:
        device.clear()
        blink_dot()
        time.sleep(1)

        device.clear()
        diagonal_line()
        time.sleep(1)

        device.clear()
        border_box()
        time.sleep(1)

        device.clear()
        show_letter_A()
        time.sleep(2)

        device.clear()
        show_message(device, "RUJA CS-IT", fill="white",
                     font=proportional(CP437_FONT),
                     scroll_delay=0.1)

        time.sleep(1)

except KeyboardInterrupt:
    device.clear()
    print("\nStopped. Display cleared.")

#----flame sensor
#Flame Sensor:
#2 - VCC
#6 - GND
#11 - OUTPUT (DO → GPIO17)
#12 - + - resistor - LED - 14
import RPi.GPIO as GPIO
import time
FLAME_DO = 17    # Pin 11 (GPIO17)
ALERT = 18       # Pin 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLAME_DO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ALERT, GPIO.OUT)
GPIO.output(ALERT, False)
print("Flame Sensor Ready...")
try:
    while True:
        value = GPIO.input(FLAME_DO)
        print("Sensor Output =", value)
        if value == 0:
            GPIO.output(ALERT, True)
            print("Flame Detected!")
        else:
            GPIO.output(ALERT, False)
            print("No Flame")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
#-----temp humidity
#2 - VCC
#6 - GND
#7 - DATA (GPIO4)
#sudo apt install python3-pip
#pip3 install Adafruit_DHT
import Adafruit_DHT
import time
sensor = Adafruit_DHT.DHT11
gpio_pin = 4      # GPIO4 (Pin 7)
print("DHT11 Sensor Reading... (Press CTRL+C to exit)")
while True:
    humidity, temperature = Adafruit_DHT.read(sensor, gpio_pin)
    if humidity is not None and temperature is not None:
        print("Temperature = {:.1f}°C".format(temperature))
        print("Humidity = {:.1f}%".format(humidity))
        print("----------------------------")
    else:
        print("Failed to retrieve data from sensor")
    time.sleep(0.5)
#-----IR sensor
#4 - VCC
#6 - GND
#16 - OUTPUT
#LED:
#18 - + - resistor - LED - 20 (GND)
import RPi.GPIO as GPIO
import time
# Use BCM mode (recommended)
GPIO.setmode(GPIO.BCM)
# GPIO Pins
sensor = 23   # GPIO23 → Physical Pin 16
led = 24      # GPIO24 → Physical Pin 18
# Setup
GPIO.setup(sensor, GPIO.IN)
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, False)
print("IR Sensor Ready...")
try:
    while True:
        if GPIO.input(sensor) == 0:   # ACTIVE LOW
            print("Object Detected")
            GPIO.output(led, True)
        else:
            print("No Object")
            GPIO.output(led, False)
        time.sleep(0.3)
except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    GPIO.output(led, False)
    GPIO.cleanup()
#-----telegram#TELEGRAM LED CONTROL

#PIN CONNECTIONS

#LED 1 (Red):
#15 - + - resistor - LED - 9 (GND)   → GPIO22

#LED 2 (Yellow):
#16 - + - resistor - LED - 6 (GND)   → GPIO23


#pip commands
#sudo apt update
#sudo apt install python3-pip
#pip3 install telepot

#---------------- STEPS ----------------#
#1 Install Telegram app on mobile
#2 Open Telegram and search "BotFather"
#3 Type /start
#4 Type /newbot
#5 Give bot name and username
#6 Copy the TOKEN given by BotFather
#7 Paste that TOKEN in Python code
#8 Install telepot library on Raspberry Pi
#9 Run the Python program
#10 Open your bot in Telegram and send commands:
#   "on red", "off red", "on yellow", "off yellow"
#LED 1 (Red):
#15 - + - resistor - LED - 9 (GND)   → GPIO22
#LED 2 (Yellow):
#16 - + - resistor - LED - 6 (GND)   → GPIO23
#sudo apt update
#sudo apt install python3-pip
#pip3 install telepot
#sudo reboot
import telepot
from telepot.loop import MessageLoop
from datetime import datetime
import RPi.GPIO as GPIO
from time import sleep
red = 22
yellow = 23
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(yellow, GPIO.OUT)
GPIO.output(red, 0)
GPIO.output(yellow, 0)
def action(msg):
    chat_id = msg["chat"]["id"]
    command = msg.get("text", "")
    print("Received:", command)
    message = ""
    if "on" in command.casefold():
        message = "Turned ON"
        if "red" in command.casefold():
            GPIO.output(red, 1)
            message += " red"
        elif "yellow" in command.casefold():
            GPIO.output(yellow, 1)
            message += " yellow"
        message += " light(s)"
        telegram_bot.sendMessage(chat_id, message)
    elif "off" in command.casefold():
        message = "Turned OFF"
        if "red" in command.casefold():
            GPIO.output(red, 0)
            message += " red"
        elif "yellow" in command.casefold():
            GPIO.output(yellow, 0)
            message += " yellow"
        message += " light(s)"
        telegram_bot.sendMessage(chat_id, message)
# BOT START
telegram_bot = telepot.Bot("YOUR_TOKEN_HERE")
print("Bot started...")
print(telegram_bot.getMe())
MessageLoop(telegram_bot, action).run_as_thread()
try:
    while True:
        sleep(10)
except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    GPIO.output(red, 0)
    GPIO.output(yellow, 0)
    GPIO.cleanup()
#-----LED
#15 - + - resistor - LED - 6 (GND)   → GPIO22
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
ledPin = 22
GPIO.setup(ledPin, GPIO.OUT)
print("LED Blinking... Press CTRL+C to stop")
try:
    while True:
        GPIO.output(ledPin, True)   # LED ON
        sleep(1)
        GPIO.output(ledPin, False)  # LED OFF
        sleep(1)
except KeyboardInterrupt:
    print("\nProgram stopped")
finally:
    GPIO.output(ledPin, False)
    GPIO.cleanup()
#-------------
man ls

ls
ls -l
ls -a

cd /home/pi
cd ..

pwd

mkdir myfolder

rmdir myfolder

rm file.txt
rm -r folder/

cp file.txt /home/pi/
cp -r folder/ backup/

mv file.txt /home/pi/
mv oldname.txt newname.txt

touch newfile.txt

cat file.txt

head file.txt
head -n 20 file.txt

tail file.txt
tail -f logfile.log

chmod 755 script.sh
chmod +x script.sh

ssh pi@192.168.1.10

df -h

dd if=image.iso of=/dev/sdX bs=4M

tree

zip archive.zip file1 file2
unzip archive.zip

tar -cvf archive.tar folder/
tar -xvf archive.tar
tar -czvf archive.tar.gz folder/

#----------
ifconfig

nano /etc/dhcpcd.conf

sudo reboot
interface eth0
static ip_address=192.168.0.67/24
static routers=192.168.1.1
static domain_name_servers=8.8.8.8