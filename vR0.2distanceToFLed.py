import time
import cv2 as cv
from isort import code
import numpy as np

import cameraHandler
import laserDistance
import sensorsRaspberry
import hwButton
import hwPWMOutput


win_name = 'Camera Matching'

#cameraNumber = 1 #0-laptopCam, 1-webCam
#camera = cameraHandler.CameraHandler(cameraNumber,raspberry=True)

#laserDist = laserDistance.LaserDistance(camera.getFocalLengthX())
#laserDist.VERBOSE_IMAGE = False

sensors = sensorsRaspberry.SensorsRaspberry(ultrasound=True, tof=True)

ultrasoundData = 0
tofData = 0

endButton = hwButton.HWButton(21)

plusLed = hwPWMOutput.HWPWMOut(19)
minusLed = hwPWMOutput.HWPWMOut(26)

# save video and data
fourcc = cv.VideoWriter_fourcc('P','I','M','1')
activeSaving = False
videoNumber = 0

#INIT - first images
#frame = camera.newImage()

while True:       
    exTime = time.perf_counter()
    
    # sensor read
    #ultrasoundData = sensors.distanceUltrasound()
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
    
    if endButton.readButton() == 0:
        print("End button is pressed!!")
        break

print("End of the program")
plusLed.close()

