import math
import time
import numpy as np
import cv2 as cv
import cv2.aruco as aruco
import markerClass

class MarkerDistSpeed:
    def __init__(self, newMtx, dist):
        self.arucoDict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self.newCameraMtx = newMtx
        self.dist = dist
        self.VERBOSE = False
        self.VERBOSE_IMAGE = False
        # speed variables
        self.markers = markerClass.Markers()
        self.imageTime = time.perf_counter()
    
    def update(self, newFrame):
        diffTime = time.perf_counter() - self.imageTime
        self.imageTime = time.perf_counter()
        
        image = np.copy(newFrame)
        grey = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
        # finding corners of the markers
        corners, ids, rejectedImgPoints = aruco.detectMarkers(grey, self.arucoDict)
        if self.VERBOSE_IMAGE: 
            image = aruco.drawDetectedMarkers(image, corners) # marker körvonalak
            cv.putText(image, str(int(1/diffTime)),(20,20),cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0))
    
        # defining world position of markers
        size_of_marker =  0.05
        rvec, tvec ,_ = aruco.estimatePoseSingleMarkers(corners, size_of_marker, self.newCameraMtx, self.dist)
    
        # I CAN SENT JUST POSITION OF ONE MARKER
        output = []
    
        if ids is not None:
            for i in range(0, ids.size):

                position = np.array([[diffTime,tvec[i][0][0],tvec[i][0][1],tvec[i][0][2]]])
                ret = self.markers.writePos(ids[i][0],position)
                if ret == 0 and self.VERBOSE:
                    print("MARKER DIST SPEED - Array with a new ID ", ids[i][0], " was created")
                
                speed = self.markers.getSpeed(ids[i][0])

                if self.VERBOSE_IMAGE:
                    cv.putText(image,"ID: %.0f Position-x: %.3f - y: %.3f - z: %.3f" % (ids[i][0],(tvec[i][0][0]),(tvec[i][0][1]),(tvec[i][0][2])), (int(corners[i][0][0][0]),int(corners[i][0][0][1])),cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0))
                    aruco.drawAxis(image, self.newCameraMtx, self.dist, rvec[i], tvec[i], 0.05) # np.array([0.0, 0.0, 0.0])
                    #cv.putText(image,"ID: %.0f Position-z: %.3f" % (ids[i][0],(tvec[i][0][2])), (int(corners[i][0][0][0]),int(corners[i][0][0][1])),cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0))
                    cv.putText(image, "Rotation - X %.0f - Y %.0f deg" % ((rvec[0][0][0] / math.pi * 180), (rvec[0][0][2] / math.pi * 180)), (int(corners[i][0][0][0]),int(corners[i][0][0][1]) + 20), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0))
                    cv.putText(image,"Speed-x: %.3f - y: %.3f - z: %.3f" % (speed[0],speed[1],speed[2]), (int(corners[i][0][0][0]),int(corners[i][0][0][1]) + 40),cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0))
                
                output.append([ids[i][0],tvec[i][0],speed, rvec[i][0]])

            if self.VERBOSE_IMAGE: cv.imshow("Marker Distance and Speed Class Image", image)

        return output    