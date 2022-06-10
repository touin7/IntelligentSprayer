import time
import cv2 as cv
import numpy as np
import featureSpeedDetection as fs
import cameraHandler
import laserDistance

win_name = 'Camera Matching'

cameraNumber = 1 #0-laptopCam, 1-webCam
camera = cameraHandler.CameraHandler(cameraNumber)

featureSpeed = fs.FeatureSpeedDetection(camera.getFocalLengthX())
featureSpeed.VERBOSE = False
featureSpeed.VERBOSE_IMAGE = False

laserDist = laserDistance.LaserDistance(camera.getFocalLengthX())
laserDist.VERBOSE_IMAGE = False

#INIT - first images
frame = camera.newImage()
    
featureSpeed.updateFirstImage(frame)

while True:       
    frame = camera.newImage()
    
    
    exTime = time.perf_counter()
    
    distZ = laserDist.update(frame)
    speed = featureSpeed.update(frame,distZ)
    
    exTime = time.perf_counter() - exTime  
    
    cv.putText(frame, "Execution time [ms]: %.2f Potential frame rate: %d"% (exTime*1000, 1/exTime), (20,20),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))    
    cv.putText(frame, "Speed-x: %.3f - y: %.3f" % (speed[0],speed[1]), (20,50),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))   
    cv.putText(frame, "Distance-z: %.3f" % (distZ), (20,80),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0)) 
    
    cv.imshow(win_name, frame)
    
    
    key = cv.waitKey(1)
    if key == 27:    # Esc
            break          
    #elif key == ord(' '): # set new feature for search 
    

print("can't open camera.")
camera.close()                         
cv.destroyAllWindows()
