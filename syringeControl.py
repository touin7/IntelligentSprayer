import time
import RPi.GPIO as GPIO
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

import hwButton
import hwPWMOutput


class SyringeControl:
    def __init__(self):
        #general variables
        #self.VERBOSE = verbose
        self.moveEnabled = False
        self.inMove = False
        self.remainSteps = 0
        self.moveSpeed = 0
        self.timeOfLastMove = time.time()

        
        
        ###################################
        #Pins
        self.buttonPin = 23 # GPIO = 23, Board = 16
        servoPin = 12 # GPIO = 12, Board = 32 
        
        self.out1 = 17 #Board = 11, GPIO = 17
        self.out2 = 27 #Board = 13, GPIO = 27
        self.out3 = 18 #Board = 12, GPIO = 18
        self.out4 = 22 #Board = 15, GPIO = 22
        
        ###################################
        #Setup - Servo
        factory = PiGPIOFactory()
        self.servo = Servo(servoPin, min_pulse_width=0.5/1000, max_pulse_width=2.2/1000, pin_factory=factory)
        
        #Setup - Stepper
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.out1,GPIO.OUT)
        GPIO.setup(self.out2,GPIO.OUT)
        GPIO.setup(self.out3,GPIO.OUT)
        GPIO.setup(self.out4,GPIO.OUT)
        
        #Setup - Callibration button
        GPIO.setup(self.buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # move Enable button
        self.moveEnButton = hwButton.HWButton(21)
        self.moveEnLed = hwPWMOutput.HWPWMOut(13) 

        ##################################
        #Variables - Servo
        self.serPosOn = 1
        self.serPosOff = 0.5
        self.serPosVar = 0.5
        
        self.servo.value = self.serPosOff

        #Variables - Stepper
        self.stepCurrPos = 0
        self.stepStartPos = 1760
        self.stepEndPos = 4800

        self.stepMoveSpeed = 1000 # ... steps per one second
        self.stepSpraySpeed = 100
        self.stepCallibSpeed = 200
        
    def waitForEnable(self):
        startTime = time.time()
        while self.moveEnabled == False:
            if time.time() - startTime > 1:
                print("In move mode, waiting for pressing move enable button!!")
                startTime = time.time()
            time.sleep(0.001)
        
    def stepperNoMove(self):
        GPIO.output( self.out1, GPIO.LOW )
        GPIO.output( self.out2, GPIO.LOW )
        GPIO.output( self.out3, GPIO.LOW )
        GPIO.output( self.out4, GPIO.LOW )
        
        
    def stepperMove(self, numSteps, moveFr):
        if numSteps == 0:
            return
        self.inMove = True
        if numSteps > 0:
            self.remainSteps = numSteps
            self.backMove = False
            print("Forward move...")
        else:
            self.remainSteps = -1*numSteps
            self.backMove = True
            print("Backward move...")
        self.moveSpeed = 1/moveFr
        self.timeOfLastMove = 0
        
        
    def updateMove(self):
        if self.inMove:
            self.moveEnLed.ledOn()
        else:
            self.moveEnLed.ledOff()

        self.moveEnabled = not self.moveEnButton.readButton()
        if self.inMove and ((time.time() - self.timeOfLastMove) > 1):
            print("In move mode - press Enable move button for move")
            self.timeOfLastMove = time.time()
        
        if self.inMove and self.moveEnabled and ((time.time() - self.timeOfLastMove) >= self.moveSpeed):
            if self.backMove is False:
                i = self.remainSteps
                if i%8==0:
                    GPIO.output( self.out4, GPIO.HIGH )
                    GPIO.output( self.out3, GPIO.LOW )
                    GPIO.output( self.out2, GPIO.LOW )
                    GPIO.output( self.out1, GPIO.LOW )
                elif i%8==1:
                    GPIO.output( self.out4, GPIO.HIGH )
                    GPIO.output( self.out3, GPIO.LOW )
                    GPIO.output( self.out2, GPIO.LOW )
                    GPIO.output( self.out1, GPIO.HIGH )
                elif i%8==2:
                    GPIO.output( self.out4, GPIO.LOW )
                    GPIO.output( self.out3, GPIO.LOW )
                    GPIO.output( self.out2, GPIO.LOW )
                    GPIO.output( self.out1, GPIO.HIGH )
                elif i%8==3:
                    GPIO.output( self.out4, GPIO.LOW )
                    GPIO.output( self.out3, GPIO.LOW )
                    GPIO.output( self.out2, GPIO.HIGH )
                    GPIO.output( self.out1, GPIO.HIGH )
                elif i%8==4:
                    GPIO.output( self.out4, GPIO.LOW )
                    GPIO.output( self.out3, GPIO.LOW )
                    GPIO.output( self.out2, GPIO.HIGH )
                    GPIO.output( self.out1, GPIO.LOW )
                elif i%8==5:
                    GPIO.output( self.out4, GPIO.LOW )
                    GPIO.output( self.out3, GPIO.HIGH )
                    GPIO.output( self.out2, GPIO.HIGH )
                    GPIO.output( self.out1, GPIO.LOW )
                elif i%8==6:
                    GPIO.output( self.out4, GPIO.LOW )
                    GPIO.output( self.out3, GPIO.HIGH )
                    GPIO.output( self.out2, GPIO.LOW )
                    GPIO.output( self.out1, GPIO.LOW )
                elif i%8==7:
                    GPIO.output( self.out4, GPIO.HIGH )
                    GPIO.output( self.out3, GPIO.HIGH )
                    GPIO.output( self.out2, GPIO.LOW )
                    GPIO.output( self.out1, GPIO.LOW )
                print('\r',' [', str(self.stepCurrPos), '/', str(self.stepCurrPos+self.remainSteps), '/', str(self.remainSteps), ']', sep='', end='', flush=True)
                self.stepCurrPos = self.stepCurrPos + 1
                self.remainSteps = self.remainSteps - 1
            else:
                i = self.remainSteps
                if i%8==0:
                    GPIO.output( self.out4, GPIO.HIGH )
                    GPIO.output( self.out3, GPIO.LOW )
                    GPIO.output( self.out2, GPIO.LOW )
                    GPIO.output( self.out1, GPIO.LOW )
                elif i%8==1:
                    GPIO.output( self.out4, GPIO.HIGH )
                    GPIO.output( self.out3, GPIO.HIGH )
                    GPIO.output( self.out2, GPIO.LOW )
                    GPIO.output( self.out1, GPIO.LOW )
                elif i%8==2:
                    GPIO.output( self.out4, GPIO.LOW )
                    GPIO.output( self.out3, GPIO.HIGH )
                    GPIO.output( self.out2, GPIO.LOW )
                    GPIO.output( self.out1, GPIO.LOW )
                elif i%8==3:
                    GPIO.output( self.out4, GPIO.LOW )
                    GPIO.output( self.out3, GPIO.HIGH )
                    GPIO.output( self.out2, GPIO.HIGH )
                    GPIO.output( self.out1, GPIO.LOW )
                elif i%8==4:
                    GPIO.output( self.out4, GPIO.LOW )
                    GPIO.output( self.out3, GPIO.LOW )
                    GPIO.output( self.out2, GPIO.HIGH )
                    GPIO.output( self.out1, GPIO.LOW )
                elif i%8==5:
                    GPIO.output( self.out4, GPIO.LOW )
                    GPIO.output( self.out3, GPIO.LOW )
                    GPIO.output( self.out2, GPIO.HIGH )
                    GPIO.output( self.out1, GPIO.HIGH )
                elif i%8==6:
                    GPIO.output( self.out4, GPIO.LOW )
                    GPIO.output( self.out3, GPIO.LOW )
                    GPIO.output( self.out2, GPIO.LOW )
                    GPIO.output( self.out1, GPIO.HIGH )
                elif i%8==7:
                    GPIO.output( self.out4, GPIO.HIGH )
                    GPIO.output( self.out3, GPIO.LOW )
                    GPIO.output( self.out2, GPIO.LOW )
                    GPIO.output( self.out1, GPIO.HIGH )
                print('\r',' [', str(self.stepCurrPos), '/', str(self.stepCurrPos-self.remainSteps), '/', str(self.remainSteps), ']', sep='', end='', flush=True)
                self.stepCurrPos = self.stepCurrPos - 1
                self.remainSteps = self.remainSteps - 1
            self.timeOfLastMove = time.time()
        if self.inMove and (self.remainSteps == 0):
            self.inMove = False
            #self.stepperNoMove()
            print("Move is finished!!!")
            
        
    def printCurrentPos(self):
        print("Current position: ", self.stepCurrPos)

    def stepInitPos(self):
        print("Going to the initial position...")
        self.printCurrentPos()
        steps = self.stepStartPos - self.stepCurrPos
        steps = steps + steps%8
        self.stepperMove(steps,self.stepMoveSpeed)

    def sprayingStepper(self):
        if self.stepCurrPos != self.stepStartPos:
            print("Follower is not in the start position --> return")
            return
        print("Start spraying...")
        steps = self.stepEndPos - self.stepStartPos
        self.stepperMove(steps,self.stepSpraySpeed)


#    def stepCalibration(self):
#        print("MODE: Calibration...")
#        print("Going back, waiting for endpoint...")
#        isPressed = GPIO.input(self.buttonPin)
#        while isPressed == GPIO.HIGH:
#            self.stepperMove(-4,self.stepCallibSpeed)
#            isPressed = GPIO.input(self.buttonPin)
#
#        print("Stepper motor is calibrated!!")
#        self.stepCurrPos = 0
#        self.stepInitPos()
        
    def servoMove(self,mode): #0 - off (NoAir), 1 - on (Spraying-Air)
        if mode == 0:
            self.servo.value = self.serPosOff
        elif mode == 1:
            self.servo.value = self.serPosOn
