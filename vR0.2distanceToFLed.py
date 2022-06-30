import time
import cv2 as cv
from isort import code
import numpy as np

import cameraHandler
import laserDistance
import sensorsRaspberry


win_name = 'Camera Matching'

cameraNumber = 1 #0-laptopCam, 1-webCam
camera = cameraHandler.CameraHandler(cameraNumber,raspberry=True)

laserDist = laserDistance.LaserDistance(camera.getFocalLengthX())
laserDist.VERBOSE_IMAGE = False

sensors = sensorsRaspberry.SensorsRaspberry(ultrasound=True, tof=True)

ultrasoundData = 0
tofData = 0

# save video and data
fourcc = cv.VideoWriter_fourcc('P','I','M','1')
activeSaving = False
videoNumber = 0

#INIT - first images
frame = camera.newImage()

while True:       
    exTime = time.perf_counter()
    
    # sensor read
    #ultrasoundData = sensors.distanceUltrasound()
    tofData = sensors.distanceToF()
    
           
    #if activeSaving:
    #    out.write(frame)
    #    outFile.write(str(time.perf_counter()) + ';' + str(exTime) + ';' + str(ultrasoundData) + ';' + str(tofData) + ';' + str(distZ))
        
        
    #    outFile.write('\n')

    exTime = time.perf_counter() - exTime    

    #cv.putText(frame, "Execution time [ms]: %.2f Potential frame rate: %d"% (exTime*1000, 1/exTime), (20,20),cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))        
    
    #cv.imshow(win_name, frame)
    
    print("Execution time [ms]: %.2f Potential frame rate: %d"% (exTime*1000, 1/exTime))


print("End of the program")

