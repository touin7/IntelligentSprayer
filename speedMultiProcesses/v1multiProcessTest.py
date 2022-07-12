import random
import sys;
import multiprocessing
import time

from matplotlib.pyplot import connect

#sys.path.insert(0, '/home/raspberry/Desktop/github/IntelligentSprayer')
sys.path.insert(0,'D:\Erasmus - Master\Work\MEDICATION\GitHub\IntelligentSprayer')

import cameraHandler
import featureSpeedDetection as fs

def cameraProcess(connection,cameraNumber=1):
    print('Camera - Sender Process: Running', flush=True)
    
    #win_name = 'Camera Matching'
    camera = cameraHandler.CameraHandler(cameraNumber)
    featureSpeed = fs.FeatureSpeedDetection(camera.getFocalLengthX())
    featureSpeed.VERBOSE = False
    featureSpeed.VERBOSE_IMAGE = False
    
    # INIT - first image
    frame = camera.newImage()
    featureSpeed.updateFirstImage(frame)
    
    cnt = 0
    while True:
        frame = camera.newImage()
        speed = featureSpeed.update(frame,30)
        connection.send(speed)
        cnt =+ 1
        
        #if connection.poll():
        #    item = connCameraRec.recv()
        #    print(f'>main got {item}', flush=True)
        #    if item is None:
        #        break
        
        if cnt == 100:
            break
    
    connection.send(None)
    print('Camera - Sender Process: Done', flush=True)
    
    

if __name__ == '__main__':
    #print("Number of cpu : ", multiprocessing.cpu_count()) # laptop - 12
    
    # create the pipe
    connCameraRec, connCameraSend = multiprocessing.Pipe(duplex=True)
    
    # start the camera sender
    camera = multiprocessing.Process(target=cameraProcess, args=(connCameraSend,))
    camera.start()
    
    
    cnt = 0
    timeStamp = time.time()
    while True:
        cnt += 1
        
        if connCameraRec.poll():
            item = connCameraRec.recv()
            print(f'>main got {item}', flush=True)
            if item is None:
                break
        
        if (time.time() - timeStamp) >= 1:
            print("I have done ", cnt, " cycles.")
            cnt = 0
            timeStamp = time.time()
    
    camera.join()   
    