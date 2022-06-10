import math
import time
import cv2 as cv
import numpy as np
import featureSpeedDetection as fs
import cameraHandler
import laserDistance
import markerDistSpeed
import serialESP8266


win_name = 'Camera Matching'

cameraNumber = 1 #0-laptopCam, 1-webCam
camera = cameraHandler.CameraHandler(cameraNumber)

#featureSpeed = fs.FeatureSpeedDetection(camera.getFocalLengthX())
#featureSpeed.VERBOSE = False
#featureSpeed.VERBOSE_IMAGE = False

laserDist = laserDistance.LaserDistance(camera.getFocalLengthX())
laserDist.VERBOSE_IMAGE = False

distSpeedMarker = markerDistSpeed.MarkerDistSpeed(camera.newcameramtx, camera.dist)
distSpeedMarker.VERBOSE = False
distSpeedMarker.VERBOSE_IMAGE = False
markID = 0
markPos = [0,0,0]
markSpeed = [0,0,0]
markRot = [0,0,0]

# Serial port
ser = serialESP8266.SerialESP8266()
ultrasoundData = 0
tofData = 0

# save video and data
fourcc = cv.VideoWriter_fourcc('P','I','M','1')
activeSaving = False
videoNumber = 0

#INIT - first images
frame = camera.newImage()
    
#featureSpeed.updateFirstImage(frame)

while True:       
    frame = camera.newImage()
    
    exTime = time.perf_counter()
    
    # serial read
    ser.readSerial()
    ultrasoundData = ser.ultrasoundData
    tofData = ser.tofData
    
    distZ = laserDist.update(frame)
    #speed = featureSpeed.update(frame,distZ)
    markerData = distSpeedMarker.update(frame)
    
    if markerData is not None:
        markID, markPos, markSpeed, markRot = markerData
    
    exTime = time.perf_counter() - exTime  
    
    cv.putText(frame, "Execution time [ms]: %.2f Potential frame rate: %d"% (exTime*1000, 1/exTime), (20,20),cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))    
    cv.putText(frame, "LASER   - Distance-z: %.3f" % (distZ), (20,50),cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0)) 
    cv.putText(frame, "MARKER  - Distance-z: %.3f" % (markPos[2]), (20,80), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0))
    cv.putText(frame, "MARKER  - Rotation X: %.3f - Y: %.3f - Z: %.3f" % (markRot[0]/math.pi*180,markRot[1]/math.pi*180,markRot[2]/math.pi*180), (20,110), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0))
    #cv.putText(frame, "FEATURE - Speed-x: %.3f - y: %.3f" % (speed[0],speed[1]), (20,110),cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0))   
    #cv.putText(frame, "MARKER  - Speed-x: %.3f - y: %.3f" % (markSpeed[0],markSpeed[1]), (20,140),cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0))
    if ser.activeSerialPort:
        cv.putText(frame, "Ultrasound - Distance-z: " + str(ultrasoundData), (20,170),cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0))
        cv.putText(frame, "ToF Laser  - Distance-z: " + str(tofData), (20,200),cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0))
    
    if activeSaving:
        out.write(frame)
        outFile.write(str(time.perf_counter()) + ';' + str(exTime) + ';' + str(markPos[2]) + ';' + str(distZ) + ';'
                      + str(ultrasoundData) + ';' + str(tofData) + ';' + str(markRot[0]/math.pi*180) + ';' + str(markRot[1]/math.pi*180) + ';' + str(markRot[2]/math.pi*180) + '\n')
    
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
            
    #elif key == ord('f'): 
    #    featureSpeed.VERBOSE_IMAGE = not featureSpeed.VERBOSE_IMAGE
    #    print("MAIN - Feature speed window was changed: ", featureSpeed.VERBOSE_IMAGE)
    #    if featureSpeed.VERBOSE_IMAGE is False:
    #        cv.destroyAllWindows()
            
    elif key == ord('v'):
        if activeSaving:
            out.release()
            outFile.close()
            activeSaving = False
            print("Video is stoped and saved, Data file is saved")
        else:
            outputFileVideoName = "data/" + str(videoNumber) + 'output.avi'
            outputFileDataName = "data/" + str(videoNumber) + 'output.txt'
            out = cv.VideoWriter(outputFileVideoName, fourcc, 20.0, (int(camera.frame_width),int(camera.frame_heigth)))
            outFile = open(outputFileDataName, 'w+')
            outFile.write("time;ExecutionTime;posZ-marker;posZ-laser;Ultrasound;Tof;RotX;RotY;RotZ\n")
            activeSaving = True
            videoNumber = videoNumber + 1
            print("New video is capturing: ", outputFileVideoName, " - New data file is created: ", outputFileDataName)
    
    elif key == ord('s'):
        if ser.activeSerialPort is not True:
            ser.openSerial()
        else:
            ser.closeSerial()
            
        
    
if (ser.activeSerialPort is True):
    ser.closeSerial()
print("End of the program")
camera.close()                         
cv.destroyAllWindows()
