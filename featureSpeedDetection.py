import time
import cv2 as cv
import numpy as np
import markerClass

#what functions are used: 
# cv.ORB_create
# cv.FlannBasedMatcher
# cv.findHomography
# cv.perspectiveTransform
# sources:
# https://github.com/dltpdn/opencv-python_edu/blob/master/08.match_track/match_camera.py
# ORB: https://docs.opencv.org/4.x/d1/d89/tutorial_py_orb.html
# Matcher: https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html
# Homografy: https://docs.opencv.org/4.x/d1/de0/tutorial_py_feature_homography.html

class FeatureSpeedDetection():
    def __init__(self, focalLengthX):
        #constants
        self.MIN_MATCH = 10
        self.VERBOSE = False
        self.VERBOSE_IMAGE = False
        self.ratio = 0.75
        self.focalLengthX = focalLengthX
        
        #variables
        self.img1 = None
        self.img1Borders = np.float32([ [[0,0]],[[0,0]],[[0,0]],[[0,0]],[[0,0]] ])
        self.oneFrameTime = 0
        self.speed = None
        self.enoughMatches = False
        
        #openCV objects
        self.detector = cv.ORB_create(1000)
        FLANN_INDEX_LSH = 6
        index_params= dict(algorithm = FLANN_INDEX_LSH,
                   table_number = 6,
                   key_size = 12,
                   multi_probe_level = 1)
        search_params=dict(checks=32) #processing time highly depends on this number
        self.matcher = cv.FlannBasedMatcher(index_params, search_params)
        
        #objects
        self.markers = markerClass.Markers()
        
    
    def update(self,newFrame, zDistance):
        if self.img1 is None:
           self.updateFirstImage(newFrame)
           return None

        img1 = self.img1
        img2 = newFrame
        gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
        gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
        
        #kp - key points, desc - descriptors
        kp1, desc1 = self.detector.detectAndCompute(gray1, None) 
        kp2, desc2 = self.detector.detectAndCompute(gray2, None)
           
        if (desc1 is None) or (desc2 is None):
            if self.VERBOSE: print('FEATURE SPEED - No descriptors')
            self.updateFirstImage(newFrame)
            self.enoughMatches = False
            return self.speed
        
        if (len(desc1) < self.MIN_MATCH) or (len(desc2) < self.MIN_MATCH):
            if self.VERBOSE: print('FEATURE SPEED - Not enough descriptors')
            self.updateFirstImage(newFrame)
            self.enoughMatches = False
            return self.speed
         
        self.enoughMatches = True   
        matches = self.matcher.knnMatch(desc1, desc2, 2)
        good_matches = [m[0] for m in matches 
                        if len(m) == 2 and m[0].distance < m[1].distance * self.ratio]
        
        if self.VERBOSE: print('FEATURE SPEED - good matches:%d/%d' %(len(good_matches),len(matches)))        
        
        matchesMask = np.zeros(len(good_matches)).tolist()
        
        if len(good_matches) > self.MIN_MATCH:
            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good_matches ])
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good_matches ])
            
            mtrx, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
            accuracy=float(mask.sum()) / mask.size
            
            if self.VERBOSE: print("FEATURE SPEED - accuracy: %d/%d(%.0f%%)"% (mask.sum(), mask.size, accuracy*100))
            
            matchesMask = mask.ravel().tolist()
            
            h,w, = img1.shape[:2]
            pts = np.float32([ [[0,0]],[[0,h-1]],[[w-1,h-1]],[[w-1,0]],[[w/2,h/2]] ])
            dst = cv.perspectiveTransform(pts,mtrx)
            
            cornerDistances = dst-self.img1Borders
            maskAvr = np.float32([0.1,0.1,0.1,0.1,0.6]) # use weigths 0.6*center 0.1*corners
            
            xDistance = 0
            yDistance = 0
            for i in range(len(cornerDistances)):
                xDistance = xDistance + cornerDistances[i,0,0]*maskAvr[i]
                yDistance = yDistance + cornerDistances[i,0,1]*maskAvr[i]
            
            if (zDistance > 1) or (zDistance < 0.1):
                zDistance = 0.30
            #dX = dx*(dZ/fx)
            
            if self.VERBOSE: print("FEATURE SPEED - used Z-distance: %0.3f" % (zDistance))
            
            self.oneFrameTime = time.perf_counter() - self.oneFrameTime
            
            xDistanceW = xDistance*(zDistance/self.focalLengthX)
            yDistanceW = yDistance*(zDistance/self.focalLengthX) #change to focalLengthY!!!!!!!!!!
            
            position = np.array([[self.oneFrameTime,xDistanceW,yDistanceW,0]])
            
            self.markers.writePos(-1,position)
            
            self.oneFrameTime = time.perf_counter()
            
        else:
            matchesMask = None
        
        self.speed = self.markers.getSpeed(-1)
        
        draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)
        
        res = cv.drawMatches(img1, kp1, img2, kp2, good_matches, None, **draw_params)
        
        if self.VERBOSE_IMAGE: 
            cv.putText(res, "Speed-x: %.3f - y: %.3f" % (self.speed[0],self.speed[1]), (20,70),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))   
            cv.imshow("Feature Speed Detection Class Image", res)
    
        if self.VERBOSE: print("FEATURE SPEED - SpeedX: %.3f" % (self.speed[0]))
        
        self.updateFirstImage(newFrame)
        
        return self.speed
        
    
    def updateFirstImage(self,newImg):#1280x720,640x480
        img = np.copy(newImg)
        h,w = img.shape[:2]
        h = h - 100
        w = w - 100
        x = 50
        y = 50
        self.img1 = img[y:y+h, x:x+w]
        self.img1Borders = np.float32([ [[x,y]],[[x,y+h]],[[x+w,y+h]],[[x+w,y]],[[x+w/2,y+h/2]] ])
        return
