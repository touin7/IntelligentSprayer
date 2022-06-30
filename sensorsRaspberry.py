import RPi.GPIO as GPIO
import board
import adafruit_vl53l1x
import time

class SensorsRaspberry:
    def __init__(self,ultrasound=False, tof=False):
        GPIO.setmode(GPIO.BCM)

        self.GPIO_TRIGGER = 15
        self.GPIO_ECHO = 14

        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)


        i2c = board.I2C()

        self.vl53 = adafruit_vl53l1x.VL53L1X(i2c)

        # OPTIONAL: can set non-default values
        self.vl53.distance_mode = 1
        self.vl53.timing_budget = 100

        print("VL53L1X Simple Test.")
        print("--------------------")
        model_id, module_type, mask_rev = self.vl53.model_info
        print("Model ID: 0x{:0X}".format(model_id))
        print("Module Type: 0x{:0X}".format(module_type))
        print("Mask Revision: 0x{:0X}".format(mask_rev))
        print("Distance Mode: ", end="")
        if self.vl53.distance_mode == 1:
            print("SHORT")
        elif self.vl53.distance_mode == 2:
            print("LONG")
        else:
            print("UNKNOWN")
        print("Timing Budget: {}".format(self.vl53.timing_budget))
        print("--------------------")

        self.vl53.start_ranging()

    def distanceToF(self):
        if self.vl53.data_ready:
            distance = self.vl53.distance
            self.vl53.clear_interrupt()
        else:
            distance = -1
        
        return distance


    def distanceUltrasound(self):
        GPIO.output(self.GPIO_TRIGGER, True)

        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()

        TestTime = time.time()

        TimeoutTime = time.time()

        while GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()
            if (StartTime - TimeoutTime) > 0.5:
                return -1

        TimeoutTime = time.time()

        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()
            if (StopTime - TimeoutTime) > 0.5:
                return -1


        TimeElapsed = StopTime - StartTime

        distance = (TimeElapsed * 34300) / 2

        return distance