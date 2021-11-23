import HC_SR04
import time

averages = 5

ultrasonic_sensor = HC_SR04.HCSR04(trigger_pin=20, echo_pin=16)

while True:
    
    distance = 0
    
    for i in range(averages):
        distance += ultrasonic_sensor.GetDistance()
        time.sleep(0.1)
      
    distance /= averages
      
    print('%.1fcm' % distance)