import time
import cv2 as cv
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

    #frame = camera.newImage()
    
    # sensor read
    ultrasoundData = sensors.distanceUltrasound()
    tofData = sensors.distanceToF()
    
    #distZ = laserDist.update(frame)
    
      
    
    #cv.putText(frame, "LASER   - Distance-z: %.3f" % (distZ), (20,50),cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0)) 
    
    
    #cv.putText(frame, "Ultrasound - Distance-z: " + str(ultrasoundData), (20,80),cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0))
    #cv.putText(frame, "ToF Laser  - Distance-z: " + str(tofData), (20,110),cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0))
       
    #if activeSaving:
    #    out.write(frame)
    #    outFile.write(str(time.perf_counter()) + ';' + str(exTime) + ';' + str(ultrasoundData) + ';' + str(tofData) + ';' + str(distZ))
        
        
    #    outFile.write('\n')

    exTime = time.perf_counter() - exTime    

    #cv.putText(frame, "Execution time [ms]: %.2f Potential frame rate: %d"% (exTime*1000, 1/exTime), (20,20),cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))        
    
    #cv.imshow(win_name, frame)
    
    print("Execution time [ms]: %.2f Potential frame rate: %d"% (exTime*1000, 1/exTime))

    '''
    key = cv.waitKey(1)
    if key == 27:    # Esc
        break          
    #elif key == ord('m'): 
    #    distSpeedMarker.VERBOSE_IMAGE = not distSpeedMarker.VERBOSE_IMAGE
    #    print("MAIN - Marker window was changed: ", distSpeedMarker.VERBOSE_IMAGE)
    #    if distSpeedMarker.VERBOSE_IMAGE is False:
    #        cv.destroyAllWindows()
            
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
            outFile.write("time;ExecutionTime;Ultrasound;Tof;posZ-laser;ID1;dist1;ID2;dist2;ID3;dist3;ID4;dist4;ID5;dist5;ID6;dist6\n")
            activeSaving = True
            videoNumber = videoNumber + 1
            print("New video is capturing: ", outputFileVideoName, " - New data file is created: ", outputFileDataName)
            
      '''

print("End of the program")
camera.close()                         
cv.destroyAllWindows()
