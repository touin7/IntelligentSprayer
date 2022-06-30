import time
import RPi.GPIO as GPIO

class HWPWMOut:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(pin, GPIO.OUT)
        
        self.led = GPIO.PWM(pin,100)
        self.led.start(0)
        
        self.blink = False
        self.blinkPer = 0.5
        self.lastBlinkTime = time.time()
        self.ledState = True
        
    def dim(self, percent):
        self.blink = False
        self.led.ChangeDutyCycle(percent)
        
    def setBlink(self, start=False, timeCycle=0.5):
        self.blink = start
        self.blinkPer = timeCycle
        self.lastBlinkTime = time.time()
        self.led.ChangeDutyCycle(100)
        
    def updateLed(self):
        if self.blink:
            if (time.time() - self.lastBlinkTime) > self.blinkPer:
                self.ledState = ~self.ledState
                if self.ledState is True:
                    self.led.ChangeDutyCycle(100)
                else:
                    self.led.ChangeDutyCycle(0)
                self.lastBlinkTime = time.time()
        
    def close(self):
        GPIO.cleanup()

        