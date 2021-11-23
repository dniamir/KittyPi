from chip_systems import ProjectSystem
from chip_systems import InertialSensors
from HC_SR04 import HC_SR04
import RPi.GPIO as GPIO
import time

import smbus
import time

class KittyPi(ProjectSystem.ProjectSystem):
	
	BOWL_MAX_DISTANCE = 100  # cm
	BOWL_MIN_DISTANCE = 50  # cm
	BOWL_WATER_REFILL_DISTANCE = 60  # cm
	DRINK_WATER_PIN = 4
	FOOD_WATER_PIN = 5
	
	def __init__(self):
		self.i2c_bus = smbus.SMBus(1)
		
		self.imu = InertialSensors.ICM20649(self.i2c_bus)
		self.SetupIMU()
		
		self.ultrasonic_sensor = HC_SR04.HCSR04(trigger_pin=20, echo_pin=16)
		
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.DRINK_WATER_PIN, GPIO.OUT)
		GPIO.setup(self.FOOD_WATER_PIN, GPIO.OUT)
		
		GPIO.output(self.DRINK_WATER_PIN, False)
		GPIO.output(self.FOOD_WATER_PIN, False)
		
		self.drink_flag = False
	
	def SetupSystem(self):
		pass
	
	def SetupIMU(self):
		
		self.imu.WriteRegisters('DEVICE_RESET', 1)
		time.sleep(0.2)
		
		self.imu.WriteRegisters('USER_BANK', 0)
		self.imu.WriteRegisters('SLEEP', 0)
		self.imu.WriteRegisters('DISABLE_ACCEL', 0)
		self.imu.WriteRegisters('DISABLE_GYRO', 0)
		time.sleep(0.2)
		
		self.SetupGyro()
		self.SetupAccel()
		self.SetupTemp()
	
	def SetupAccel(self):
		
		self.imu.WriteRegisters('ACCEL_FS_SEL', 0)
		self.imu.WriteRegisters('ACCEL_FCHOICE', 1)
		self.imu.WriteRegisters('ACCEL_DLPFCFG', 0)
		self.imu.WriteRegisters('ACCEL_SMPLRT_DIV_1', 0)
		self.imu.WriteRegisters('ACCEL_SMPLRT_DIV_2', 1)
		time.sleep(0.2)
		
	def SetupGyro(self):
		
		self.imu.WriteRegisters('USER_BANK', 2)
		self.imu.WriteRegisters('GYRO_FS_SEL', 0)
		self.imu.WriteRegisters('GYRO_FCHOICE', 1)
		self.imu.WriteRegisters('GYRO_DLPFCFG', 0)
		self.imu.WriteRegisters('GYRO_SMPLRT_DIV', 1)
		time.sleep(0.2)
		
	def SetupTemp(self):
		self.imu.WriteRegisters('TEMP_DLPFCFG', 2)
	
	def ReadOutputs(self):
		pass
	
	def ReadDistance(self, averages=5):
		
		distance = 0
		
		for i in range(averages):
			distance += self.ultrasonic_sensor.GetDistance()
			time.sleep(0.1)
		
		distance /= averages
		
		return distance
	
	def MonitorWaterLevel(self):
		
		water_reading_cm = self.ReadDistance(50)
		
		check1 = water_reading_cm > self.BOWL_MAX_DISTANCE
		check2 = water_reading_cm < self.BOWL_MIN_DISTANCE
		check3 = water_reading_cm > self.BOWL_WATER_REFILL_DISTANCE
		
		if check1 and check2 and check3:
			flag = True
		else:
			flag = False
			
		return flag
		
	def ActivateDrinkPump(self, activate=True):
		
		GPIO.output(self.DRINK_WATER_PIN, activate)
	
	def ActivateFoodPump(self, activate=True):
		
		GPIO.output(self.FOOD_WATER_PIN, activate)

	def ManageWater(self):
		
		self.drink_flag = self.MonitorWaterLevel()
		
		if self.drink_flag:
			self.ActivateDrinkPump(activate=True)
			time.sleep(2)
			self.ActivateDrinkPump(activate=False)
			
