#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import DCMotor

#imports for camera and API functionality
from pixy2 import Pixy2
import json
import urequests
import utime

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# URL for API call (Localhost for now, will be changed domain name when hosted)
url = 'gps.bassilyounes/api/camdata'  

# Establish connection to EV3 Brick
ev3 = EV3Brick()

# Establish connection to Pixy2
pixy2 = Pixy2(port=1, i2c_address=0x54)

# Get Pixy2 frame resolution
frame = pixy2.get_resolution()

print("W:", frame.width)
print("H:", frame.height)

# define function to send data to API
def sendData(x, y):
    # print("Sending data to API")
    dataObj = {'X': x, 'Y': y}
    json_data = json.dumps(dataObj).encode('utf-8')
    response = urequests.post(url, data=json_data, headers={'Content-Type': 'application/json'})
    response_data = response.text
    print(response_data)

# Set interval for data to be sent to API
interval = .5

# Set number of blocks to be detected
numBlocks = 5

# Main loop
while True:
    # Get number of blocks and block data
    try:
        nr_blocks, blocks = pixy2.get_blocks(1, numBlocks)
        # Rest of your code here
    except OSError as e:
        # Handle the specific exception
        print("An error occurred during get_blocks():", e)
        # Perform any necessary cleanup or fallback actions


    # Format and output data to console and send data to API
    for i in range(nr_blocks):
        sig = blocks[i].sig
        x = blocks[i].x_center
        y = blocks[i].y_center
        print("cords{}: {}, {}".format(i+1, x, y))
        sendData(x, y)
            

    # Delay for set amount of seconds
    utime.sleep(interval)
