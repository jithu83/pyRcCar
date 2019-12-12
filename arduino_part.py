import time

def map_range(x, X_min, X_max, Y_min, Y_max):
    ''' 
    Linear mapping between two ranges of values 
    '''
    X_range = X_max - X_min
    Y_range = Y_max - Y_min
    XY_ratio = X_range/Y_range

    y = ((x-X_min) / XY_ratio + Y_min) // 1

    return int(y)

class ArduinoFirmata:
    ''' 
    PWM motor controler using PCA9685 boards. 
    This is used for most RC Cars
    '''
    def __init__(self, servo_pin, esc_pin):
        from pymata_aio.pymata3 import PyMata3
        self.board = PyMata3()
        self.board.sleep(0.015)
        self.servo_pin = servo_pin
        self.esc_pin = esc_pin
        self.board.servo_config(servo_pin)
        self.board.servo_config(esc_pin)
        
    def set_pulse(self, pin, angle):
        try:
            self.board.analog_write(pin, int(angle))
        except:
            self.board.analog_write(pin, int(angle))
    
    def set_servo_pulse(self, angle):
        self.set_pulse(self.servo_pin, int(angle))
   
    def set_esc_pulse(self, angle):
        self.set_pulse(self.esc_pin, int(angle))
    #def run(self, angle):
    #    self.set_pulse(angle)


class PWMSteering:
    """
    Wrapper over a PWM motor controller to convert angles to PWM pulses.
    """
    LEFT_ANGLE = -1
    RIGHT_ANGLE = 1

    def __init__(self,
                 controller=None,
                 left_pulse=60,
                 right_pulse=120):

        self.controller = controller
        self.left_pulse = left_pulse
        self.right_pulse = right_pulse
        self.pulse = map_range(0, self.LEFT_ANGLE, self.RIGHT_ANGLE,
                                        self.left_pulse, self.right_pulse)
        self.running = True
        print('PWM Steering created')

    def update(self):
        while self.running:
            self.controller.set_servo_pulse(self.pulse)

    def run_threaded(self, angle):
        # map absolute angle to angle that vehicle can implement.
        self.pulse = map_range(angle,
                               self.LEFT_ANGLE, self.RIGHT_ANGLE,
                               self.left_pulse, self.right_pulse)

    def run(self, angle):
        self.run_threaded(angle)
        self.controller.set_servo_pulse(self.pulse)

    def shutdown(self):
        # set steering straight - Jithu map range needed ?
        #self.pulse = 0
        time.sleep(0.3)
        self.running = False



class PWMThrottle:

    """
    Wrapper over a PWM motor controller to convert -1 to 1 throttle
    values to PWM pulses.
    """
    MIN_THROTTLE = -1
    MAX_THROTTLE = 1

    def __init__(self,
                 controller=None,
                 max_pulse=105,
                 min_pulse=75,
                 zero_pulse=90):

        self.controller = controller
        self.max_pulse = max_pulse
        self.min_pulse = min_pulse
        self.zero_pulse = zero_pulse
        self.pulse = zero_pulse

        # send zero pulse to calibrate ESC
        print("Init ESC")
        self.controller.set_esc_pulse(self.max_pulse)
        time.sleep(0.01)
        self.controller.set_esc_pulse(self.min_pulse)
        time.sleep(0.01)
        self.controller.set_esc_pulse(self.zero_pulse)
        time.sleep(1)
        self.running = True
        print('PWM Throttle created')

    def update(self):
        while self.running:
            self.controller.set_esc_pulse(self.pulse)

    def run_threaded(self, throttle):
        if throttle > 0:
            self.pulse = map_range(throttle, 0, self.MAX_THROTTLE,
                                   self.zero_pulse, self.max_pulse)
        else:
            self.pulse = map_range(throttle, self.MIN_THROTTLE, 0,
                                   self.min_pulse, self.zero_pulse)

    def run(self, throttle):
        self.run_threaded(throttle)
        self.controller.set_esc_pulse(self.pulse)

    def shutdown(self):
        # stop vehicle
        self.run(0)
        self.running = False
    
