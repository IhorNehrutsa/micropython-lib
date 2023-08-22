from machine import Pin, PWM, Signal
from time import sleep, sleep_us
from sys import print_exception

from HBridge_common import *
from HBridgeDirPwm import HBridgeDirPwm

try:
    dir = 22
    pwm = 23
    motor = HBridgeDirPwm(dir, pwm)
    print('motor=', motor)
    sleep(1)

    speed = U16 // 2
    motor.forward(speed)
    sleep(1)
    motor.backward(speed)
    sleep(1)

    print('motor.go(percentages_to_i16(30)')
    motor.go(percentages_to_i16(30))
    sleep(1)

    print('motor.go(0)')
    motor.go(0)
    sleep(1)

    print('motor.go(percentages_to_i16(-30)')
    motor.go(percentages_to_i16(-30))
    sleep(1)

    print('motor.stop()')
    motor.stop()
    sleep(1)

    print('motor.go(U16 // 2)')
    motor.go(U16 // 2)
    sleep(1)

    speed = 0
    speed_min = 10_000
    speed_max = 65_530
    delta = 10
    while 1:
        motor.go(speed)

        if speed % 1000 == 0:
            print(speed, end='  \r')

        speed += delta
        if delta > 0:
            if  -speed_min < speed < speed_min:
                speed = speed_min
                print(speed, ' ')
        else:
            if -speed_min < speed < speed_min:
                speed = -speed_min
                print(speed, ' ')
        if speed > speed_max:
            speed = speed_max
            print(speed, ' ')
            delta = -delta
        elif speed < -speed_max:
            speed = -speed_max
            print(speed, ' ')
            delta = -delta

        sleep_us(200)

except Exception as e:
    print_exception(e)

finally:
    try:
        motor.stop()
        print('motor.stop()')
    except:
        pass
