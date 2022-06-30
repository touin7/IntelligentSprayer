import time
import numpy as np
import cv2 as cv

class CameraHandler:
    def __init__(self, cameraNumber = 0, imagePath=None, raspberry=False):
        self.cameraNumber = cameraNumber
        self.imagePath = imagePath
        
        if cameraNumber == -1:
            self.cameraNumber = self.imageInit()
            if self.cameraNumber == -1:
                return
        
        print("Opening stream...")
        if raspberry is False:
            self.cap = cv.VideoCapture(1,cv.CAP_DSHOW)
            if not self.cap.isOpened():
                print("Just one camera is connected --> laptop cam")
                self.cameraNumber = 0
                self.cap = cv.VideoCapture(0,cv.CAP_DSHOW)
            elif cameraNumber == 0:
                print("Two cameras are connected --> laptop cam")
                self.cameraNumber = 0
                self.cap = cv.VideoCapture(1,cv.CAP_DSHOW)
            elif cameraNumber == 1:
                print("Two cameras are connected --> web cam")
                self.cameraNumber = 1
                self.cap = cv.VideoCapture(0,cv.CAP_DSHOW)
        else:
            print("Raspberry is True --> trying to open USB cam")
            self.cap = cv.VideoCapture(0)
            time.sleep(1)
            if not self.cap.isOpened():
                print("No camera is connected --> exit")
                exit()
            else:
                self.cameraNumber = 1
        
        if self.cameraNumber == 1:
            with np.load('CalDataWebCamAruco.npz') as X:
                self.mtx, self.dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]
            
        else:
            with np.load('CalDataLaptopCamAruco.npz') as X:
                self.mtx, self.dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

                
        
        print("Video stream is opened!")        
        
        
        if self.cameraNumber == 1:
            self.cap.set(cv.CAP_PROP_FRAME_WIDTH,1280)
            self.cap.set(cv.CAP_PROP_FRAME_HEIGHT,720)
        else:
            self.cap.set(cv.CAP_PROP_FRAME_WIDTH,640)
            self.cap.set(cv.CAP_PROP_FRAME_HEIGHT,480)
            
        if not self.cap.isOpened():
            print("Cannot open camera --> exit")
            exit() #CHANGE TO SOMETHING DIFFERENT
            
        self.frame_width = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)
        self.frame_heigth = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)
        camera_fps = self.cap.get(cv.CAP_PROP_FPS)

        print("Video size: ", self.frame_width, self.frame_heigth, " fps: ", camera_fps)
        
        ret, frame = self.cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
    
        h,  w = frame.shape[:2]
        self.newcameramtx, roi = cv.getOptimalNewCameraMatrix(self.mtx, self.dist, (w,h), 1, (w,h))

        #print("mtx---------------------")
        #print(self.mtx)
        print("newmtx------------------")
        print(self.newcameramtx)
        #print("dist--------------------")
        #print(self.dist)
        print("------------------------")
        
        
    def imageInit(self):
        
        print("Image Evaluation...")
        
        img = cv.imread(self.imagePath)
        if img is None:
            print("Could not read the image.")
            return 0
            
        with np.load('CalDataWebCamAruco.npz') as X:
            self.mtx, self.dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

        self.frame_heigth, self.frame_width = img.shape[:2]

        print("Image size: ", self.frame_width, self.frame_heigth)
        
        self.newcameramtx, roi = cv.getOptimalNewCameraMatrix(self.mtx, self.dist, (self.frame_width,self.frame_heigth), 1, (self.frame_width,self.frame_heigth))
        
        print("newmtx------------------")
        print(self.newcameramtx)
        print("------------------------")
        return -1
        
    def newImage(self):
        if self.cameraNumber == -1:
            img = cv.imread(self.imagePath)
            undstImage = cv.undistort(img, self.mtx, self.dist, None, self.newcameramtx)
            return undstImage
            
        ret, frame = self.cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            return None
            
        # undistortion of the current frame
        undstImage = cv.undistort(frame, self.mtx, self.dist, None, self.newcameramtx)
        # crop the image - oriznuti obrazku
        #x, y, w, h = roi
        #image = undstImage[y:y+h, x:x+w]
        
        return undstImage
    
    def getFocalLengthX(self):
        return self.newcameramtx[0][0]
    
    def close(self):
        if self.cameraNumber != -1:
            self.cap.release()