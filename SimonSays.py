from gpiozero import LED, Button
from time import sleep
from random import uniform
from signal import pause
import array as arr
import itertools
from random import randint

greenLed = LED(4)
blueLed = LED(20)
redLed = LED(21)
blue_button = Button(17)
red_button = Button(18)
white_button = Button(16)
red_round_button = Button(26)
blue_round_button = Button(19)
inputArray = []
gameArray = []

def playGame():
    redLed.off()
    inputArray.clear()
    gameArray.clear()
    availableArray = [17, 16, 26]
    for x in range(5):
        gameArray.append(availableArray[randint(0, 2)])
    print(gameArray)
    print('go!')

    for x in gameArray:
        if x == 17:
            blueLed.blink(0.2,0.2,1,False)
            sleep(0.3)
        if x == 26:
            redLed.blink(0.2,0.2,1,False)
            sleep(0.3)
        if x == 16:
            greenLed.blink(0.2,0.2,1,False)
            sleep(0.3)

def pressed(button):
    print(str(button.pin.number) + ' pressed')
    inputArray.append(button.pin.number)
    print(inputArray)
    if button.pin.number == 17:
        blueLed.on()
    if button.pin.number == 26:
        redLed.on()
    if button.pin.number == 16:
        greenLed.on()

def released(button):
    blueLed.off()
    redLed.off()
    greenLed.off()

def checkAnswer():
    if inputArray == gameArray:
        print('You did it!')
        greenLed.blink(0.1,0.1,15,True)
    else:
        print ('Sorry, maybe next time!')
        redLed.on()

red_round_button.when_pressed = pressed
blue_button.when_pressed = pressed
white_button.when_pressed = pressed
red_round_button.when_released = released
blue_button.when_released = released
white_button.when_released = released

red_button.when_released = checkAnswer
blue_round_button.when_released = playGame
