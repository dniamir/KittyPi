from chip_systems import ProjectSystem
import smbus
import time

from chip_systems import InertialSensors

class KittyPi(ProjectSystem.ProjectSystem):
	
	def __init__(self):
		self.i2c_bus = smbus.SMBus(1)
		self.imu = InertialSensors.ICM20649(self.i2c_bus)
	
	def SetupSystem(self):
		pass
	
	def ReadOutputs(self):
		pass
