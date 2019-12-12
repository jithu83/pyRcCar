#!/usr/bin/env python3
"""
Scripts to drive a donkey 2 car

Usage:
    js_drive.py

Options:
    -h --help          Show this screen.
"""
import os
import time

from docopt import docopt

import read_config as conf
from vehicle import Vehicle
from joystick_part import LogitechJoystickController
from arduino_part import ArduinoFirmata, PWMSteering, PWMThrottle


def drive():
    '''
    Construct a working robotic vehicle from many parts.
    Each part runs as a job in the Vehicle loop, calling either
    it's run or run_threaded method depending on the constructor flag `threaded`.
    All parts are updated one after another at the framerate given in
    cfg.DRIVE_LOOP_HZ assuming each part finishes processing in a timely manner.
    Parts may have named outputs and inputs. The framework handles passing named outputs
    to parts requesting the same named input.
    '''

    # Initialize car
    V = Vehicle()

    f710 = LogitechJoystickController(
        auto_record_on_throttle=False, steering_scale=1,
        throttle_scale=cfg.JOYSTICK_MAX_THROTTLE,
        throttle_dir=cfg.JOYSTICK_THROTTLE_DIR)

    V.add(f710,
          outputs=['user/angle', 'user/throttle', 'user/mode', 'recording'],
          threaded=True)

    # Drive train setup
    arduino_controller = ArduinoFirmata(
        servo_pin=cfg.STEERING_ARDUINO_PIN, esc_pin=cfg.THROTTLE_ARDUINO_PIN)
    steering = PWMSteering(controller=arduino_controller,
                           left_pulse=cfg.STEERING_LEFT_PWM,
                           right_pulse=cfg.STEERING_RIGHT_PWM)

    throttle = PWMThrottle(controller=arduino_controller,
                           max_pulse=cfg.THROTTLE_FORWARD_PWM,
                           zero_pulse=cfg.THROTTLE_STOPPED_PWM,
                           min_pulse=cfg.THROTTLE_REVERSE_PWM)

    V.add(steering, inputs=['user/angle'])
    V.add(throttle, inputs=['user/throttle'])

    # run the vehicle
    V.start(rate_hz=cfg.DRIVE_LOOP_HZ,
            max_loop_count=cfg.MAX_LOOPS)


if __name__ == '__main__':
    args = docopt(__doc__)
    cfg = conf.load_config("config.py")

    drive()
