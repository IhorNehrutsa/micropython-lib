from machine import Pin, PWM, Signal
from time import sleep, sleep_us
from sys import print_exception

from HBridge_common import *
from HBridge4Pwm import HBridge4Pwm

try:
    pwm1 = 22  # IN1 grey
    pwm2 = 4   # IN3 brown
    pwm3 = 23  # IN2 white
    pwm4 = 2   # IN4 orange
    motor = HBridge4Pwm(pwm1, pwm2, pwm3, pwm4)
    print('motor=', motor)
    sleep(1)

    motor.stop()
    motor.breakh()
    motor.breakl()
    motor.coast1()
    motor.coast2()
    motor.coast3()
    motor.coast4()

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
