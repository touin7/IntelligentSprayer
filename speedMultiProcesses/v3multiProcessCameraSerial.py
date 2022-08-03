import sys;
import multiprocessing
import time


sys.path.insert(0, '/home/raspberry/Desktop/github/IntelligentSprayer')
#sys.path.insert(0,'D:\Erasmus - Master\Work\MEDICATION\GitHub\IntelligentSprayer')

import cameraHandler
import featureSpeedDetection as fs
import serialESP8266

def cameraProcess(connection,cameraNumber=1,verb=False,verbIm=False):
    print('--Camera - Sender Process: Running', flush=True)
    
    camera = cameraHandler.CameraHandler(cameraNumber,raspberry=True)
    featureSpeed = fs.FeatureSpeedDetection(camera.getFocalLengthX(),savedSamples=5)
    featureSpeed.VERBOSE = verb
    featureSpeed.VERBOSE_IMAGE = verbIm
    
    # INIT - first image
    frame = camera.newImage()
    featureSpeed.updateFirstImage(frame)
    
    while True:
        frame = camera.newImage()
        speed = featureSpeed.update(frame,30) #Add data about the distance
        connection.send(speed)
        
        if connection.poll():
            item = connection.recv()
            print(f'>Camera - Sender Process got {item}', flush=True)
            if item is None:
                break
    
    connection.send(None)
    print('--Camera - Sender Process: Done', flush=True)
    
def serialProcess(connection):
    print('--Serial - Sender Process: Running', flush=True)
    
    ser = serialESP8266.SerialESP8266(rawOutput=True,verbose=False)
    rawData = 0
    ser.openSerial(com='/dev/ttyUSB0')
    
    while True:
        
        rawData = ser.readSerial()
        connection.send(rawData)
        
        if connection.poll():
            item = connection.recv()
            print(f'>Serial - Sender Process got {item}', flush=True)
            if item is None:
                break
    
    ser.closeSerial()
    connection.send(None)
    print('--Serial - Sender Process: Done', flush=True)
    

if __name__ == '__main__':
    #print("Number of cpu : ", multiprocessing.cpu_count()) # laptop - 12
    
    # create the pipe
    connCameraRec, connCameraSend = multiprocessing.Pipe(duplex=True)
    connSerialRec, connSerialSend = multiprocessing.Pipe(duplex=True)
    
    # start the camera sender process
    camera = multiprocessing.Process(target=cameraProcess, args=(connCameraSend,))
    camera.start()
    
    # start the serial sender process
    serial = multiprocessing.Process(target=serialProcess,args=(connSerialSend,))
    serial.start()
    
    cnt = 0
    cntMes = 0
    timeStamp = time.time()
    
    velCamX = 0
    velCamY = 0
    velSerX = 0
    velSerY = 0
    
    while True:
        cnt += 1
        
        if connCameraRec.poll():
            item = connCameraRec.recv()
            #print(f'>main got from Camera {item}', flush=True)
            if item is not None:
                velCamX = item[0]
                velCamY = item[1]
                print("  --> main camera: ", velCamX, " - ", velCamY)
            cntMes += 1
            if item is None:
                break
            
            
        if connSerialRec.poll():
            item = connSerialRec.recv()
            #print(f'>main got from Serial {item}', flush=True)
            if item is not None:
                lines = str(item)
                lines = lines.split(';')
                velSerX = lines[0].split(' ')
                if len(velSerX) == 3:
                    velSerX = float(velSerX[1])
                velSerY = lines[1].split(' ')
                if len(velSerY) == 2:
                    velSerY = velSerY[1].split('\\')
                    velSerY = float(velSerY[0])
                #print("  --> main serial: ", velSerX, " - ", velSerY)
        
        if (time.time() - timeStamp) >= 1:
            #print("I have done ", cnt, " cycles.")
            cnt = 0
            timeStamp = time.time()
            
        if cntMes == 100:
            print("I received 100 messages --> send terminate command")
            connCameraRec.send(None)
            connSerialRec.send(None)
            cntMes = 0
    
    camera.join()   
    serial.join()
    