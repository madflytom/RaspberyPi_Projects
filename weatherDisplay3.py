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

url = 'http://dataservice.accuweather.com/currentconditions/v1/2109247'
apiKey = ''

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

# wipe LCD screen before we start
lcd.clear()
timeout = time.time() + 60*60 #in one hour
weather = get(url+'?apikey='+apiKey+'&details=true').json()

while True:

    if time.time() > timeout:
        weather = get(url+'?apikey='+apiKey+'&details=true').json()
        timeout = time.time() + 60*60 #in one hour
        print('Reset timeout to: ' + str(timeout)

    temp = weather[0]['Temperature']['Imperial']['Value']
    text = weather[0]['WeatherText']
    relativeHumidity = weather[0]['RelativeHumidity']
    uvIndex = weather[0]['UVIndexText']
    wind = weather[0]['Wind']['Speed']['Imperial']['Value']
    baro = weather[0]['PressureTendency']['LocalizedText']
    date = datetime.now().strftime('%b %d  %H:%M:%S')
        
    # date and time
    #lcd_line_1 = datetime.now().strftime('%b %d  %H:%M:%S\n')
    lcd_line_1 = "Temp: " + str(temp) + "F\n"

    # current ip address
    lcd_line_2 = text

    # combine both lines into one update to the display
    lcd.message = lcd_line_1 +'\n'+ lcd_line_2

    sleep(5)

    for i in range(len(lcd_line_2)):
        time.sleep(0.2)
        lcd.move_left()

    lcd.clear()

    lcd_line_3 = 'UV Ind: ' + uvIndex
    lcd_line_4 = 'Wind: ' + str(wind) + 'mi/h'

    # combine both lines into one update to the display
    lcd.message = lcd_line_3 +'\n'+ lcd_line_4

    sleep(5)

    for i in range(len(lcd_line_4)):
        time.sleep(0.2)
        lcd.move_left()

    lcd.clear()

    lcd_line_5 = 'Baro: ' + baro
    lcd_line_6 = date

    # combine both lines into one update to the display
    lcd.message = lcd_line_5 +'\n'+ lcd_line_6

    sleep(5)

    for i in range(len(lcd_line_6)):
        time.sleep(0.2)
        lcd.move_left()

    
