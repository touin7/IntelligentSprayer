import time
import cv2 as cv
import numpy as np

import sensorsRaspberry
import hwButton
import hwPWMOutput
import syringeControl

import RPi.GPIO as GPIO

#it is a bit mess, change syringe control - stepper move

sensors = sensorsRaspberry.SensorsRaspberry(ultrasound=True, tof=True)

ultrasoundData = 0
tofData = 0

sprayButton = hwButton.HWButton(20)

plusLed = hwPWMOutput.HWPWMOut(19)
minusLed = hwPWMOutput.HWPWMOut(26)

syringe = syringeControl.SyringeControl()

sprayingMode = 0

# Move enable button definition
buttonPin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def buttonEventOn(channel):
    syringe.moveEnabled = True
    
def buttonEventOff(channel):
    syringe.moveEnabled = False

def calibration():
    print("MODE: Calibration...")
    print("Going back, waiting for endpoint...")
    while True:
        isPressed = GPIO.input(syringe.buttonPin)
        if isPressed == GPIO.LOW:
            syringe.inMove = False
            break
            
        if syringe.inMove is False:
            syringe.stepperMove(-4,syringe.stepCallibSpeed)

        syringe.updateMove()

    print("Stepper motor is calibrated!!")
    syringe.stepCurrPos = 0
    syringe.stepInitPos()
    
if __name__ == '__main__':
    GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback = buttonEventOn, bouncetime=300)
    GPIO.add_event_detect(buttonPin, GPIO.RISING, callback = buttonEventOff, bouncetime=300)
    calibration()
    while True:       
        exTime = time.perf_counter()
        
        # sensor read
        newTofData = sensors.distanceToF()
        if (newTofData != None):
            tofData = newTofData
        
        
        if tofData > 40:
            minusLed.blink()
        elif tofData < 20:
            plusLed.blink()
        elif tofData >= 30: # distance is in between 30cm and 40cm
            minusLed.dim((tofData-30)*10)
            plusLed.dim(0)
        elif tofData < 30: # distance is in between 20cm and 30cm
            minusLed.dim(0)
            plusLed.dim((30-tofData)*10)

        
        exTime = time.perf_counter() - exTime    
        
        #print("Execution time [ms]: %.2f Potential frame rate: %d"% (exTime*1000, 1/exTime))
        
        if sprayingMode == 1: #going to the initial position
            if syringe.inMove == False:
                print("Initial position reached")
                syringe.servoMove(1)
                print("Valve is closed - ready for spraying")
                time.sleep(2)
                syringe.sprayingStepper()
                sprayingMode = 2
        elif sprayingMode == 2:
            if syringe.inMove == False:
                print("Spraying ended")
                time.sleep(1)
                syringe.servoMove(0)
                sprayingMode = 0
                
            
        syringe.updateMove()
        
        if sprayButton.readButton() == 0:

            print("Spray button is pressed!!")
            if sprayingMode == 0:
                syringe.stepInitPos()
                sprayingMode = 1
            else:
                print("Spraying has already started!!")
            
            
            
            
            
            
            

    print("End of the program")
    plusLed.close()

