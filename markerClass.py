import numpy as np

class OneMarker:
    def __init__(self, id, savedSamples=10, subPos=True):
        self.id = id
        self.speed = np.array([np.NaN,np.NaN,np.NaN]) #[x,y,z]
        self.positions = np.array([[0,0,0,0]]) #it will be full of 4x1 vectors [difTime, x, y, z]
        self.substractPositions = subPos # True - we have positions, False - we have differences
        self.numSavedSamples = savedSamples
        
        
    def checkSamples(self):
        if self.positions.shape[0] > self.numSavedSamples:
            self.positions = np.delete(self.positions,0,0) #delete the first item
            
    def speedCalculation(self):
        if self.positions.shape[0] < (self.numSavedSamples - 1):
            self.speed = np.array([np.NaN,np.NaN,np.NaN])
            return # not enough possitions for calculation
        
        movedArray = np.delete(self.positions,0,0)
        modArray = np.delete(self.positions,self.positions.shape[0]-1,0)

        difArray = np.delete(movedArray,np.s_[:1],1) - np.delete(modArray,np.s_[:1],1)

        # extract first row of positions = times between positions
        time = self.positions[:,0]

        if self.substractPositions:
            time = np.delete(time,0,0)
            speed = np.array([difArray[:,0]/time, difArray[:,1]/time, difArray[:,2]/time])
        else:
            speed = np.array([self.positions[:,1]/time, self.positions[:,2]/time, self.positions[:,3]/time])
        
        #TO-DO: come clever of signal processing, for example weighted average
        self.speed =  np.sum(speed,1)/time.size
     
    def getID(self):
        return self.id    
            
    def getSpeed(self):
        return self.speed      
        
    def writePosition(self, position): #position [numOfFrame, x, y, z]
        self.positions = np.append(self.positions, position, axis=0)
        self.checkSamples()
        
    def getPosition(self):
        return self.positions
        
        
class Markers:
    def __init__(self):
        self.markers = []
        
    def getSpeed(self, id):
        for mr in self.markers:
            if mr.getID() == id:
                mr.speedCalculation()
                return mr.getSpeed()
        return 0
    
    def writePos(self, id, position, numSavedSamples = 10):
        for mr in self.markers:
            if mr.getID() == id:
                mr.numSavedSamples = numSavedSamples
                mr.writePosition(position)
                return 1
        if id >= 0:
            newMarker = OneMarker(id, savedSamples=numSavedSamples)
        else:
            newMarker = OneMarker(id, savedSamples=numSavedSamples, subPos=False)
        newMarker.writePosition(position)
        self.markers.append(newMarker)
        return 0
        
    def printAll(self):
        for mark in self.markers:
            print("ID: ", mark.getID())
            print("Positions: ", mark.getPosition())
            print("Speed: ", mark.getSpeed())
            print()