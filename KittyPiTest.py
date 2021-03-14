import KittyPi
from chip_systems import ProjectSystem
import time
from datetime import datetime

# Get date and time
now = datetime.now()
datetime_date = now.strftime("%d/%m/%Y")
datetime_time = now.strftime("%H:%M:%S")

kittypi = KittyPi.KittyPi()

kittypi.imu.WriteRegisters('DEVICE_RESET', 1)
time.sleep(0.2)

kittypi.imu.WriteRegisters('USER_BANK', 0)
kittypi.imu.WriteRegisters('SLEEP', 0)
kittypi.imu.WriteRegisters('DISABLE_ACCEL', 0)
kittypi.imu.WriteRegisters('DISABLE_GYRO', 0)
time.sleep(0.2)

kittypi.imu.WriteRegisters('USER_BANK', 2)
kittypi.imu.WriteRegisters('GYRO_FS_SEL', 0)
kittypi.imu.WriteRegisters('GYRO_FCHOICE', 1)
kittypi.imu.WriteRegisters('GYRO_DLPFCFG', 0)
kittypi.imu.WriteRegisters('GYRO_SMPLRT_DIV', 1)
time.sleep(0.2)

kittypi.imu.WriteRegisters('ACCEL_FS_SEL', 0)
kittypi.imu.WriteRegisters('ACCEL_FCHOICE', 1)
kittypi.imu.WriteRegisters('ACCEL_DLPFCFG', 0)
kittypi.imu.WriteRegisters('ACCEL_SMPLRT_DIV_1', 0)
kittypi.imu.WriteRegisters('ACCEL_SMPLRT_DIV_2', 1)
time.sleep(0.2)

kittypi.imu.WriteRegisters('TEMP_DLPFCFG', 2)

afs = 4 * 1e3
gfs = 500

kittypi.imu.WriteRegisters('USER_BANK', 0)
ax_lsb = kittypi.imu.ReadRegisters('ACCEL_XOUT_H', 2)[1]
ax_lsb = ProjectSystem.TwosComp(int(ax_lsb, 2), bits=16)
ax_mgee = ax_lsb * afs / 2 ** 15

ay_lsb = kittypi.imu.ReadRegisters('ACCEL_YOUT_H', 2)[1]
ay_lsb = ProjectSystem.TwosComp(int(ay_lsb, 2), bits=16)
ay_mgee = ay_lsb * afs   / 2 ** 15

az_lsb = kittypi.imu.ReadRegisters('ACCEL_ZOUT_H', 2)[1]
az_lsb = ProjectSystem.TwosComp(int(az_lsb, 2), bits=16)
az_mgee = az_lsb * afs / 2 ** 15

gx_lsb = kittypi.imu.ReadRegisters('GYRO_XOUT_H', 2)[1]
gx_lsb = ProjectSystem.TwosComp(int(gx_lsb, 2), bits=16)
gx_dps = gx_lsb * gfs / 2 ** 15

gy_lsb = kittypi.imu.ReadRegisters('GYRO_YOUT_H', 2)[1]
gy_lsb = ProjectSystem.TwosComp(int(gy_lsb, 2), bits=16)
gy_dps = gy_lsb * gfs / 2 ** 15

gz_lsb = kittypi.imu.ReadRegisters('GYRO_ZOUT_H', 2)[1]
gz_lsb = ProjectSystem.TwosComp(int(gz_lsb, 2), bits=16)
gz_dps = gz_lsb * gfs / 2 ** 15

temp_lsb = kittypi.imu.ReadRegisters('TEMP_OUT_H', 2)[1]
temp_lsb = ProjectSystem.TwosComp(int(temp_lsb, 2), bits=16)

temp_degc = (temp_lsb - 25) / 333.87 + 0

print('test1')

while True:
	print('%.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f' %  kittypi.imu.ReadAllSensors())
	time.sleep(0.5)

print('test2')