import time
import smbus
import sys

import board
import adafruit_lsm9ds1
import adafruit_fxos8700
import adafruit_fxas21002c


sys.path.insert(0, '/home/raspberry/Desktop/github/IntelligentSprayer')

import hwButton

### MPU6050 functions and variables
#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value


bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

i2c = board.I2C()  # uses board.SCL and board.SDA
sensorLsm = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
sensorFxos = adafruit_fxos8700.FXOS8700(i2c)
sensorFxas = adafruit_fxas21002c.FXAS21002C(i2c)

print (" Reading Data of Gyroscope and Accelerometer")


# data saving variables
savingButton = hwButton.HWButton(21)
activeSaving = False
fileNumber = 0


while True:
    
    #reading sensor data
    #Read Accelerometer raw value
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
	
	#Read Gyroscope raw value
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)
	
	#Full scale range +/- 250 degree/C as per sensitivity scale factor
    Ax = acc_x/16384.0
    Ay = acc_y/16384.0
    Az = acc_z/16384.0
	
    Gx = gyro_x/131.0
    Gy = gyro_y/131.0
    Gz = gyro_z/131.0

    ###################################Lsm9ds1 Reading
    accel_x, accel_y, accel_z = sensorLsm.acceleration
    mag_x, mag_y, mag_z = sensorLsm.magnetic
    gyro_x, gyro_y, gyro_z = sensorLsm.gyro
    temp = sensorLsm.temperature
    dataStringLSM9DS1 = str("%.3f" %gyro_x + ";%.3f" %gyro_y + ";%.3f" %gyro_z + ";%.3f" %accel_x + ";%.3f" %accel_y + ";%.3f" %accel_z + ";%.3f" %mag_x + ";%.3f" %mag_y + ";%.3f" %mag_z)
    #print(dataStringLSM9DS1)

    ####################################fxas/fxos Reading
    accel_x, accel_y, accel_z = sensorFxos.accelerometer
    mag_x, mag_y, mag_z = sensorFxos.magnetometer
    gyro_x, gyro_y, gyro_z = sensorFxas.gyroscope
    dataStringFx = str("%.3f" %gyro_x + ";%.3f" %gyro_y + ";%.3f" %gyro_z + ";%.3f" %accel_x + ";%.3f" %accel_y + ";%.3f" %accel_z + ";%.3f" %mag_x + ";%.3f" %mag_y + ";%.3f" %mag_z)
    #print(dataStringFx)
    
    
    dataStringMPU6050 = str("%.3f" %Gx + ";%.3f" %Gy + ";%.3f" %Gz + ";%.3f" %Ax + ";%.3f" %Ay + ";%.3f" %Az)
    #print(dataStringMPU6050) 	

    time.sleep(0.0001) #10kHz sampling frequency
    
    if activeSaving:
        outFile.write(str(time.perf_counter()) + ';' + dataStringMPU6050 + ';' + dataStringLSM9DS1 + ';' + dataStringFx + '\n') #dataStringMPU6050, dataStringLSM9DS1, dataStringFx


    key = savingButton.readButton()
    if key == 0:
        if activeSaving:
            outFile.close()
            activeSaving = False
            print("Data will be saved wait 1 second and release button...")
            time.sleep(1)
            print("Data file is saved")
        else:
            outputFileDataName = "data/" + str(fileNumber) + 'output.txt'
            outFile = open(outputFileDataName, 'w+')
            outFile.write("MPUData GUnits:" + u'\u00b0'+ "/s - AUnits:g" + "\n")
            outFile.write("LSM9DS1Data G Units:rad/s - A Units:m/s^2 - m Units:gausss" + "\n")
            outFile.write("Fx...Data G Units:rad/s - A Units:m/s^2 - m Units:gausss" + "\n")
            outFile.write("time;MPU-Gx;MPU-Gy;MPU-Gz;MPU-Ax;MPU-Ay;MPU-Az;")
            outFile.write("LSM-Gx;LSM-Gy;LSM-Gz;LSM-Ax;LSM-Ay;LSM-Az;LSM-Mx;LSM-My;LSM-Mz")
            outFile.write(";Fx-Gx;Fx-Gy;Fx-Gz;Fx-Ax;Fx-Ay;Fx-Az;Fx-Mx;Fx-My;Fx-Mz\n")
            
            activeSaving = True
            fileNumber = fileNumber + 1
            print("New data file is created: ", outputFileDataName)
            print("Saving will start in 1 second...")
            time.sleep(1)
            print("Saving has started!!")
    