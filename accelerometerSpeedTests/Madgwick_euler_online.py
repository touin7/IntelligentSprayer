import imufusion
import numpy as np
import sys
import math
import time
import board
import adafruit_fxos8700
import adafruit_fxas21002c


sample_rate = 100  # 100 Hz

# Instantiate algorithms
offset = imufusion.Offset(sample_rate)
ahrs = imufusion.Ahrs()

ahrs.settings = imufusion.Settings(0.5,  # gain
                                   10,  # acceleration rejection
                                   20,  # magnetic rejection
                                   5 * sample_rate)  # rejection timeout = 5 seconds


gEarth = 9.80665

### def IMUs
i2c = board.I2C()  # uses board.SCL and board.SDA
sensorFxAccelMag = adafruit_fxos8700.FXOS8700(i2c)

sensorFxGyro = adafruit_fxas21002c.FXAS21002C(i2c)

### variables
radToDegConst = 180/math.pi
msTogConst = 1/9.80665

sys.path.insert(0, '/home/raspberry/Desktop/github/IntelligentSprayer')

### button deff
import hwButton

# data saving variables
savingButton = hwButton.HWButton(21)
resetButton = hwButton.HWButton(20)
activeSaving = False
fileNumber = 0
startTime = time.time()

def updateMadgwick(timeDiff, gyro, accel, mag):
    gyroscope = offset.update(gyro)
    ahrs.update(gyro, accel, mag, timeDiff)
    euler = ahrs.quaternion.to_euler()
    
    #ahrs_internal_states = ahrs.internal_states
    #ahrs_flags = ahrs.flags
    
    return euler
    
lastTime = time.time()    
while True:
    # Read acceleration & magnetometer.
    accel_x, accel_y, accel_z = sensorFxAccelMag.accelerometer
    mag_x, mag_y, mag_z = sensorFxAccelMag.magnetometer
    gyro_x, gyro_y, gyro_z = sensorFxGyro.gyroscope
    
    accel = np.array([accel_x, accel_y, accel_z])
    mag = np.array([mag_x, mag_y, mag_z])
    gyro = np.array([gyro_x, gyro_y, gyro_z])
    
    gyro = gyro*radToDegConst
    
    accel = accel*msTogConst
    
    # Print values.
    timeDiff = time.time() - lastTime
    lastTime = time.time()
    eulers = updateMadgwick(timeDiff, gyro, accel, mag)
    
    if activeSaving:
        dataStringFx = str("%.9f" %gyro_x + ";%.9f" %gyro_y + ";%.9f" %gyro_z + ";%.9f" %accel_x + ";%.9f" %accel_y + ";%.9f" %accel_z + ";%.9f" %mag_x + ";%.9f" %mag_y + ";%.9f" %mag_z)
        timeMeasurement = time.time() - startTime
        outFile.write(str(time.perf_counter()) + ',' + dataStringFx + '\n')

    print("EulerAngles [deg] - Roll: %.3f" %eulers(0) + " - Pitch: %.3f" %eulers(1) + " - Yaw: %.3f" %eulers(2))

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
            outFile.write("Fx...Data G Units:rad/s - A Units:m/s^2 - m Units:gausss...")
            outFile.write("time;Fx-Gx;Fx-Gy;Fx-Gz;Fx-Ax;Fx-Ay;Fx-Az;Fx-Mx;Fx-My;Fx-Mz\n")
            
            activeSaving = True
            fileNumber = fileNumber + 1
            print("New data file is created: ", outputFileDataName)
            print("Saving will start in 1 second...")
            time.sleep(1)
            print("Saving has started!!")


