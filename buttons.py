# KY040 Python Class
# Martin O'Hanlon
# stuffaboutcode.com

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

class Buttons:
    CLOCKWISE = 1
    ANTICLOCKWISE = -1

    def __init__(self, callback_map):
        self.map = callback_map
        for pin, callback in callback_map.items():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin,
                                  GPIO.FALLING,
                                  callback=callback,
                                  bouncetime=250)

    def stop(self):
        for pin in self.map.keys():
            GPIO.remove_event_detect(pin)
        GPIO.cleanup()

# test
if __name__ == "__main__":

    def moveLeft():
        print "Move Left"


    def moveRight():
        print "Move Right"


    def drop():
        print "Drop"


    def rotate():
        print "Rotate"


    buttons = Buttons({21: rotate, 26:moveLeft, 19:moveRight, 16:drop})

    try:
        while True:
            sleep(0.1)
    finally:
        buttons.stop()
        GPIO.cleanup()
