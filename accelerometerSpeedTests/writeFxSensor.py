# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the FXOS8700 accelerometer and magnetometer.
# Will print the acceleration and magnetometer values every second.
import math
import time
import sys
import board
import adafruit_fxos8700
import adafruit_fxas21002c


# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_fxos8700.FXOS8700(i2c)
# Optionally create the sensor with a different accelerometer range (the
# default is 2G, but you can use 4G or 8G values):
# sensor = adafruit_fxos8700.FXOS8700(i2c, accel_range=adafruit_fxos8700.ACCEL_RANGE_4G)
# sensor = adafruit_fxos8700.FXOS8700(i2c, accel_range=adafruit_fxos8700.ACCEL_RANGE_8G)

sensor2 = adafruit_fxas21002c.FXAS21002C(i2c)
# Optionally create the sensor with a different gyroscope range (the
# default is 250 DPS, but you can use 500, 1000, or 2000 DPS values):
# sensor = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=adafruit_fxas21002c.GYRO_RANGE_500DPS)
# sensor = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=adafruit_fxas21002c.GYRO_RANGE_1000DPS)
# sensor = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=adafruit_fxas21002c.GYRO_RANGE_2000DPS)

# Main loop will read the acceleration and magnetometer values every second
# and print them out.

radToDegConst = 180/math.pi

msTogConst = 1/9.80665

sys.path.insert(0, '/home/raspberry/Desktop/github/IntelligentSprayer')

import hwButton

# data saving variables
savingButton = hwButton.HWButton(21)
activeSaving = False
fileNumber = 0
startTime = time.time()

def printValues():
    print(
        "Gyroscope (deg/s): ({0:0.3f},  {1:0.3f},  {2:0.3f})".format(
            gyro_x, gyro_y, gyro_z
        )
    )
    print(
        "Acceleration (g): ({0:0.3f}, {1:0.3f}, {2:0.3f})".format(
            accel_x, accel_y, accel_z
        )
    )
    print(
        "Magnetometer (uTesla): ({0:0.3f}, {1:0.3f}, {2:0.3f})".format(
            mag_x, mag_y, mag_z
        )
    )

while True:
    # Read acceleration & magnetometer.
    accel_x, accel_y, accel_z = sensor.accelerometer
    mag_x, mag_y, mag_z = sensor.magnetometer
    gyro_x, gyro_y, gyro_z = sensor2.gyroscope
    
    gyro_x = gyro_x*radToDegConst
    gyro_y = gyro_y*radToDegConst
    gyro_z = gyro_z*radToDegConst
    
    accel_x = accel_x*msTogConst
    accel_y = accel_y*msTogConst
    accel_z = accel_z*msTogConst
    
    # Print values.

    
    if activeSaving:
        dataStringFx = str("%.9f" %gyro_x + ";%.9f" %gyro_y + ";%.9f" %gyro_z + ";%.9f" %accel_x + ";%.9f" %accel_y + ";%.9f" %accel_z + ";%.9f" %mag_x + ";%.9f" %mag_y + ";%.9f" %mag_z)
        timeMeasurement = time.time() - startTime
        outFile.write(str(time.perf_counter()) + ',' + dataStringFx + '\n')
    else:
        printValues()



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

