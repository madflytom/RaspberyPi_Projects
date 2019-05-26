from subprocess import Popen, PIPE
from time import sleep
from datetime import datetime
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from requests import get
import json
from pprint import pprint
from haversine import haversine

stations = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getallstations'
weather = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getlatestmeasurements/'

my_lat = 39.788952
my_lon = -86.367086

all_stations = get(stations).json()['items']

def find_closest():
    smallest = 20036
    for station in all_stations:
        station_lon = station['weather_stn_long']
        station_lat = station['weather_stn_lat']
        distance = haversine(my_lon, my_lat, station_lon, station_lat)
        if distance < smallest:
            smallest = distance
            closest_station = station['weather_stn_id']
    return closest_station

closest_stn = find_closest()

weather = weather + str(closest_stn)

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# compatible with all versions of RPI as of Jan. 2019
# v1 - v3B+
lcd_rs = digitalio.DigitalInOut(board.D2)
lcd_en = digitalio.DigitalInOut(board.D3)
lcd_d4 = digitalio.DigitalInOut(board.D7)
lcd_d5 = digitalio.DigitalInOut(board.D8)
lcd_d6 = digitalio.DigitalInOut(board.D11)
lcd_d7 = digitalio.DigitalInOut(board.D9)


# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                      lcd_d7, lcd_columns, lcd_rows)

print("clearing screen")

# wipe LCD screen before we start
lcd.clear()

while True:

    my_weather = get(weather).json()['items']
    pprint(my_weather)

    temp = float(my_weather[0]['ambient_temp'])*(9/5)+32

    # date and time
    lcd_line_1 = datetime.now().strftime('%b %d  %H:%M:%S\n')

    # current ip address
    lcd_line_2 = "Temp: " + str(temp) + "F"

    # combine both lines into one update to the display
    lcd.message = lcd_line_1 + lcd_line_2

    sleep(90)

    for i in range(len(lcd_line_2)):
        time.sleep(0.2)
        lcd.move_left()

    lcd.clear()
