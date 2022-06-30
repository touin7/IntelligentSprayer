import RPi.GPIO as GPIO

class HWButton:
    def __init__(self, buttonPin):
        GPIO.setmode(GPIO.BCM)
        
        self.buttonPin = buttonPin
        
        GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    def readButton(self):
        return GPIO.input(self.buttonPin)