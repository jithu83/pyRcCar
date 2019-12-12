

#VEHICLE
DRIVE_LOOP_HZ = 20   # the vehicle loop will pause if faster than this speed.
MAX_LOOPS = None     # the vehicle loop can abort after this many iterations, when given a positive integer.

#STEERING (aka servo)
STEERING_ARDUINO_PIN = 6  # the Arduino pin to which steering is connected
STEERING_LEFT_PWM = 120   # One end of steering 
STEERING_RIGHT_PWM = 60   # Other end of the steering
 
#THROTTLE (aka ESC)
THROTTLE_ARDUINO_PIN = 5  # the Arduino pin to which throttle is connected
THROTTLE_FORWARD_PWM = 75 # Max forward throttle config
THROTTLE_STOPPED_PWM = 90 # Stopped throttle config 
THROTTLE_REVERSE_PWM = 105 # Max reverse throttle config

#JOYSTICK
JOYSTICK_MAX_THROTTLE = 0.8         #this scalar is multiplied with the -1 to 1 throttle value to limit the maximum throttle. This can help if you drop the controller or just don't need the full speed available.
JOYSTICK_THROTTLE_DIR = -1.0        # use -1.0 to flip forward/backward, use 1.0 to use joystick's natural forward/backward