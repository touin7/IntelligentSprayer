import time
import serial

class SerialESP8266:
    def __init__(self):
        self.ultrasoundData = 0
        self.tofData = 0
        self.activeSerialPort = False
        self.ser = None
        
    def openSerial(self,com='COM3',boudRate=115200):
        print("Tring to open Serial port...")
        try:
            self.ser = serial.Serial(com, boudRate, timeout=1)
            print(self.ser)
            print("Serial port state after opening: ", str(self.ser.isOpen()))
            self.activeSerialPort = True
            self.ser.flushInput()
        except:
            print("Serial port is not available!!")
        return
            
    def closeSerial(self):
        if self.ser is not None:
            self.ser.close()
            self.activeSerialPort = False
            print("Serial port is closed.")
            return
        else:
            print("Serial object is None")
        return
    
    
    def readSerial(self):
        if self.activeSerialPort:
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
        return
    
