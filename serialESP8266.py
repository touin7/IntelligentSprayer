import time
import serial

# class is not properly written - add return numbers when serial port is not available/connected

class SerialESP8266:
    def __init__(self, rawOutput=False, verbose=False):
        self.ultrasoundData = 0
        self.tofData = 0
        self.activeSerialPort = False
        self.ser = None
        self.rawData = rawOutput
        self.VERBOSE = verbose
        
    def openSerial(self,com='COM3',boudRate=115200):
        if self.VERBOSE: print("SERIAL READ - Tring to open Serial port...")
        try:
            self.ser = serial.Serial(com, boudRate, timeout=1)
            print(self.ser)
            if self.VERBOSE: print("SERIAL READ - Serial port state after opening: ", str(self.ser.isOpen()))
            self.activeSerialPort = True
            self.ser.flushInput()
        except:
            if self.VERBOSE: print("SERIAL READ - Serial port is not available!!")
        return
            
    def closeSerial(self):
        if self.ser is not None:
            self.ser.close()
            self.activeSerialPort = False
            if self.VERBOSE: print("SERIAL READ - Serial port is closed.")
            return
        else:
            if self.VERBOSE: print("SERIAL READ - Serial object is None")
        return
    
    
    def readSerial(self):        
        if self.activeSerialPort:
            if self.rawData:
                if self.VERBOSE: print("SERIAL READ - waiting for new data")
                while self.ser.inWaiting() < 20:
                    pass
                time.sleep(0.01)
                bufferString = str(self.ser.read(self.ser.inWaiting()))
                return bufferString
            else:
                bufferString = str(self.ser.read(self.ser.inWaiting()))
                lines = bufferString.split(';')
                if len(lines) > 4:
                    if "Ultrasound" in lines[1]:
                        ultrasoundDataR = (lines[1].split(':'))
                        if len(ultrasoundDataR) == 2:
                            self.ultrasoundData = float(ultrasoundDataR[1])
                    if "ToF" in lines[2]:
                        tofDataR = (lines[2].split(':'))
                        if len(tofDataR) == 2:
                            self.tofData = float(tofDataR[1])
        else:
            return None
        return
    
