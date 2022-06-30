import time
import RPi.GPIO as GPIO

class HWPWMOut:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(pin, GPIO.OUT)
        
        self.led = GPIO.PWM(pin,100)
        self.led.start(0)
        
        self.blinkPer = 0.1
        self.lastBlinkTime = time.time()
        self.ledState = True
        
    def dim(self, percent):
        self.led.ChangeDutyCycle(percent)
        
    def blink(self, timeCycle=0.1):
        self.blinkPer = timeCycle
        if (time.time() - self.lastBlinkTime) > self.blinkPer:
            self.ledState = not self.ledState
            if self.ledState is True:
                self.led.ChangeDutyCycle(100)
            else:
                self.led.ChangeDutyCycle(0)
            self.lastBlinkTime = time.time()
        
        
    def close(self):
        GPIO.cleanup()

        