import time
import cv2 as cv
import numpy as np
import featureSpeedDetection as fs
import cameraHandler
import laserDistance
import markerDistSpeed

#Add: serialport, videosaving, datafilesaving

#upravit: 
# vytisknout pattern na zed, obrazek
# test laser distance
# na testy prilepit lasery at jsou zaple
# fast camera opening - different APi - cv.CAP_VFW,cv.CAP_V4L,cv.CAP_V4L2,cv.CAP_QT,cv.CAP_UNICAP

# for faster SW
# featureSpeedDetection limit the size of the window for finding features - show the field in the main image

win_name = 'Camera Matching'

cameraNumber = 0 #0-laptopCam, 1-webCam
camera = cameraHandler.CameraHandler(cameraNumber)

featureSpeed = fs.FeatureSpeedDetection(camera.getFocalLengthX())
featureSpeed.VERBOSE = False
featureSpeed.VERBOSE_IMAGE = False

laserDist = laserDistance.LaserDistance(camera.getFocalLengthX())
laserDist.VERBOSE_IMAGE = False

distSpeedMarker = markerDistSpeed.MarkerDistSpeed(camera.newcameramtx, camera.dist)
distSpeedMarker.VERBOSE = False
distSpeedMarker.VERBOSE_IMAGE = False
markID = 0
markPos = [0,0,0]
markSpeed = [0,0,0]

#INIT - first images
frame = camera.newImage()
    
featureSpeed.updateFirstImage(frame)

while True:       
    frame = camera.newImage()
    
    
    exTime = time.perf_counter()
    
    distZ = laserDist.update(frame)
    speed = featureSpeed.update(frame,distZ)
    markerData = distSpeedMarker.update(frame)
    
    if markerData is not None:
        markID, markPos, markSpeed = markerData
    
    exTime = time.perf_counter() - exTime  
    
    cv.putText(frame, "Execution time [ms]: %.2f Potential frame rate: %d"% (exTime*1000, 1/exTime), (20,20),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))    
    cv.putText(frame, "LASER   - Distance-z: %.3f" % (distZ), (20,50),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0)) 
    cv.putText(frame, "MARKER  - Distance-z: %.3f" % (markPos[2]), (20,80), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
    cv.putText(frame, "FEATURE - Speed-x: %.3f - y: %.3f" % (speed[0],speed[1]), (20,110),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))   
    cv.putText(frame, "MARKER  - Speed-x: %.3f - y: %.3f" % (markSpeed[0],markSpeed[1]), (20,140),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
    
    cv.imshow(win_name, frame)
    
    
    key = cv.waitKey(1)
    if key == 27:    # Esc
        break          
    elif key == ord('m'): 
        distSpeedMarker.VERBOSE_IMAGE = not distSpeedMarker.VERBOSE_IMAGE
        print("MAIN - Marker window was changed: ", distSpeedMarker.VERBOSE_IMAGE)
        if distSpeedMarker.VERBOSE_IMAGE is False:
            cv.destroyAllWindows()
            
    elif key == ord('l'): 
        laserDist.VERBOSE_IMAGE = not laserDist.VERBOSE_IMAGE
        print("MAIN - Laser distance window was changed: ", laserDist.VERBOSE_IMAGE)
        if laserDist.VERBOSE_IMAGE is False:
            cv.destroyAllWindows()
            
    elif key == ord('f'): 
        featureSpeed.VERBOSE_IMAGE = not featureSpeed.VERBOSE_IMAGE
        print("MAIN - Feature speed window was changed: ", featureSpeed.VERBOSE_IMAGE)
        if featureSpeed.VERBOSE_IMAGE is False:
            cv.destroyAllWindows()
            
    

print("End of the program")
camera.close()                         
cv.destroyAllWindows()
