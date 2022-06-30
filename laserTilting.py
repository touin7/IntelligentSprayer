import cv2 as cv
import numpy as np


class LaserTilting:
    def __init__(self, focalLenX):
        self.VERBOSE_IMAGE = False
        self.distZ = 0
        
    def update(self, newImage):
        image = np.copy(newImage)
        #grey = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        #blue = image[:,:,0]
        green = image[:,:,1]
        #red = image[:,:,2]
        
        th, threshed = cv.threshold(green, 220, 250, cv.THRESH_BINARY)
        cnts,hierarchy = cv.findContours(threshed, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        dotPos = []
        self.distZ = 0
        h,w, = image.shape[:2]

        for cnt in cnts:
            (x,y),radius = cv.minEnclosingCircle(cnt)
            x = int(x)
            y = int(y)
            dotPos.append([x,y])
        
        if len(cnts) > 1:
            centerPoint = np.array([int(w/2), int(h/2)])
            npDots = np.array(dotPos)
            deltas = np.linalg.norm(centerPoint-npDots, axis=1)
            sortedIndexes = np.argsort(deltas)
        
            deltas = np.linalg.norm(npDots[sortedIndexes[0]]-npDots, axis=1)
            sortedIndexes = np.argsort(deltas)
        
            # searching the closest point which is further than 30 pixels
            secID = 1
            while True:
                if deltas[sortedIndexes[secID]] > 30:
                    break
            
                secID = secID + 1 
            
                if sortedIndexes.size == secID:
                    secID = 1
                    break
                    
            if self.VERBOSE_IMAGE:
                for i in range(0,sortedIndexes.size):
                    cv.circle(image,(npDots[sortedIndexes[i],0],npDots[sortedIndexes[i],1]),20,(255,0,0),3)
                    cv.putText(image,"NumCenter: " + str(i), (npDots[sortedIndexes[i],0],npDots[sortedIndexes[i],1]),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
    
                cv.circle(image,(npDots[sortedIndexes[0],0],npDots[sortedIndexes[0],1]),10,(0,0,255),5)
                cv.circle(image,(npDots[sortedIndexes[secID],0],npDots[sortedIndexes[secID],1]),10,(0,0,255),5)


            
        if self.VERBOSE_IMAGE: 
            cv.imshow("Tilting detection Class", image)
                
        return image