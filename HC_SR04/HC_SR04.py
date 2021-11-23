import RPi.GPIO as GPIO
import time


class HCSR04(object):
    """Class for HC_SR04 ultrasonic sensor

    Args:
        trigger_pin: int. BCM pin to trigger the ultrasonic ping
        echo_pin: int. BCM pin to sense the ultrasonic ping
    """
    PULSE_LENGTH = 10 * 1e-6  # 10us
    SOUND_SPEED = 34300  # cm / s

    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def GetDistance(self):
        """Get distance as read by the ultrasonic sensor

        Outputs:
            distance: float. Distance to nearest object as read by the sensor in cm
        """
        # set Trigger to HIGH
        GPIO.output(self.trigger_pin, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(self.PULSE_LENGTH)
        GPIO.output(self.trigger_pin, False)

        start_time = time.time()
        stop_time = time.time()

        # save StartTime
        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()

        # save time of arrival
        while GPIO.input(self.echo_pin) == 1:
            stop_time = time.time()

        # time difference between start and arrival
        duration = stop_time - start_time
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (duration * self.SOUND_SPEED) / 2
        
        return distance
