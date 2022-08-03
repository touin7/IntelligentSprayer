import multiprocessing
import time
import cv2 as cv
import numpy as np

import sensorsRaspberry
import hwButton
import hwPWMOutput
import syringeControl

import RPi.GPIO as GPIO

#it is a bit mess, change syringe control - stepper move
# UDELAT VLAKNO PRO STEPPER MOTOR!!!!!!!!!!!!!!!!!!! a otestovat + test ToF senzoru když se sprayuje a když né

sensors = sensorsRaspberry.SensorsRaspberry(ultrasound=True, tof=True)

ultrasoundData = 0
tofData = 0

wantedDistance = 39

sprayButton = hwButton.HWButton(20)

plusLed = hwPWMOutput.HWPWMOut(19)
minusLed = hwPWMOutput.HWPWMOut(26)



sprayingMode = 0


def syringeProcess(connection):
    print('--Syringe Process: Running', flush=True)
    syringe = syringeControl.SyringeControl()
    
    calibration(syringe)
    
    timeSendInMove = time.time()
    
    while True:
        
        if connection.poll():
            item = connection.recv()
            print(" -- Syringe Process recceived: ", item)
            if item == 's0':
                syringe.servoMove(0)
                connection.send(syringe.inMove)
            elif item == 's1':
                syringe.servoMove(1)
                connection.send(syringe.inMove)
            elif item == 'm0':
                syringe.stepperNoMove()    
                connection.send(syringe.inMove)
            elif item == 'm1':
                syringe.sprayingStepper()
                connection.send(syringe.inMove)
            elif item == 'm2':
                syringe.stepInitPos()
                connection.send(syringe.inMove)
            elif item == None:
                syringe.stepperNoMove()
                syringe.inMove = False
                break
        
        syringe.updateMove()
        
        if (time.time() - timeSendInMove) > 0.1:
            timeSendInMove = time.time()
            connection.send(syringe.inMove)
            
    print('--Syringe Process: Done', flush=True)
    

def calibration(syringe):
    print("MODE: Calibration...")
    print("Going back, waiting for endpoint...")
    while True:
        isPressed = GPIO.input(syringe.buttonPin)
        if isPressed == GPIO.LOW:
            syringe.inMove = False
            break
            
        if syringe.inMove is False:
            syringe.stepperMove(-8,syringe.stepCallibSpeed)

        syringe.updateMove()

    print("Stepper motor is calibrated!!")
    syringe.stepCurrPos = 0
    syringe.stepInitPos()
    
    
    
def sendMessageToProcess(connection, message):
    while connSyringeRec.poll():
        connSyringeRec.recv()
        print("In connection buffer: ", inMoveSyringe)

    connection.send(message)
        
    while not connection.poll():
        pass
        
    return connection.recv()
    
if __name__ == '__main__': 
    
    # create the pipe
    connSyringeRec, connSyringeSend = multiprocessing.Pipe(duplex=True)
    
    syringeProc = multiprocessing.Process(target=syringeProcess, args=(connSyringeSend,))
    syringeProc.start()
    
    inMoveSyringe = connSyringeRec.recv()
    
    programEnd = False
    
    
    outputFileDataName = 'data/outputTof.txt'
    outFile = open(outputFileDataName, 'w+')
    outFile.write("time;ToF[cm]\n")
    print("New data file is created: ", outputFileDataName)
    
    while True:       
        exTime = time.perf_counter()
        
        # sensor read
        newTofData = sensors.distanceToF()
        if (newTofData != None):
            tofData = newTofData
        
        
        if tofData > (wantedDistance+10):
            minusLed.blink()
        elif tofData < (wantedDistance-10):
            plusLed.blink()
        elif tofData >= wantedDistance: # distance is in between 30cm and 40cm
            minusLed.dim((tofData-wantedDistance)*10)
            plusLed.dim(0)
        elif tofData <= wantedDistance: # distance is in between 20cm and 30cm
            minusLed.dim(0)
            plusLed.dim((wantedDistance-tofData)*10)

        outFile.write(str(time.time()) + ';' + str(tofData) + '\n')
        
        exTime = time.perf_counter() - exTime    
        
        #print(syringe.moveEnabled)
        #print("Execution time [ms]: %.2f Potential frame rate: %d"% (exTime*1000, 1/exTime))
        
        if connSyringeRec.poll():
            inMoveSyringe = connSyringeRec.recv()
            #print("--Main process received: ", inMoveSyringe)
        
        
        if sprayingMode == 1: #going to the initial position
            if inMoveSyringe == False:
                print("Initial position reached")
                inMoveSyringe = sendMessageToProcess(connSyringeRec, 's1')#syringe.servoMove(1) # s1
                print("Valve is closed - ready for spraying")
                inMoveSyringe = sendMessageToProcess(connSyringeRec, 'm1')#syringe.sprayingStepper() # m1
                sprayingMode = 2
        elif sprayingMode == 2:
            if inMoveSyringe == False:
                print("Spraying ended")
                inMoveSyringe = sendMessageToProcess(connSyringeRec, 'm0')#syringe.stepperNoMove() # m0
                time.sleep(1)
                inMoveSyringe = sendMessageToProcess(connSyringeRec, 's0')#syringe.servoMove(0) # s0
                sprayingMode = 3
        elif sprayingMode == 3:
                print("Syringe was removed ;)")
                inMoveSyringe = sendMessageToProcess(connSyringeRec, 'm2')#syringe.stepInitPos() # m2
                sprayingMode = 4
                time.sleep(1)
        elif sprayingMode == 4:
            if inMoveSyringe == False:
                inMoveSyringe = sendMessageToProcess(connSyringeRec, 'm0')#syringe.stepperNoMove() # m0
                print("Sprayer is in initial position")
                print("...Insert full syringe!!!")
                sprayingMode = 0
                
        
        if sprayButton.readButton() == 0:

            #print("Spray button is pressed!!")
            if sprayingMode == 0:
                inMoveSyringe = sendMessageToProcess(connSyringeRec, 'm2')#syringe.stepInitPos() # m2
                sprayingMode = 1
            elif sprayingMode == 4:
                print("Do you really want to end program????")
                actualTime = time.time()
                time.sleep(0.5)
                print("For end of the program press the button again.")
                while (time.time() - actualTime) < 2:
                    if sprayButton.readButton() == 0:
                        print("PROGRAM ENDS")
                        programEnd = True
                        break
                print("Button was not pressed - program continue.")
            else:
                print("Spraying has already started!!")
                
        
        if programEnd:
            connSyringeRec.send(None)
            break
           
    outFile.close()
    print("Data file is saved") 
    syringeProc.join()
    print("End of the program")
    plusLed.close()

