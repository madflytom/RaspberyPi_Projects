from gpiozero import LED, Button
from time import sleep
from random import uniform
from signal import pause

led = LED(4)
blueLed = LED(20)
redLed = LED(21)
right_button = Button(17)
left_button = Button(18)
game_button = Button(16)

def playGame():
    
    blueLed.off()
    redLed.off()
    led.on()
    sleep(uniform(5, 10))
    led.off()

def pressed(button):
    print(str(button.pin.number) + ' won the game')
    if button.pin.number == 17:
        blueLed.blink(0.2,0.2,5,True)
    if button.pin.number == 18:
        redLed.blink(0.2,0.2,5,True)
    sleep(4)

right_button.when_pressed = pressed
left_button.when_pressed = pressed

game_button.when_pressed = playGame
