import RPi.GPIO as GPIO
import time
import requests
import datetime
GPIO.setmode(GPIO.BCM)

API_ENDPOINT = "https://sumplevelsapi.azurewebsites.net/api/WaterLevels"

TRIG = 23
ECHO = 24

print("Distance Measurement In Progress")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)
print("Waiting For Sensor to Settle")
time.sleep(2)

GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

while GPIO.input(ECHO)==0:
    pulse_start = time.time()

while GPIO.input(ECHO)==1:
    pulse_end = time.time()

pulse_duration = pulse_end - pulse_start

distance = pulse_duration * 17150
distance = round(distance,2)

print("Distance: ",distance,"cm")

GPIO.cleanup()

print("Sending data to cloud...")

data = {'LoggedTime': datetime.datetime.now(),
        'Measurement': distance}

r = requests.post(url = API_ENDPOINT, data = data)

print(r.text)
