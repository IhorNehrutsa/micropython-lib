from machine import Pin, PWM, Signal
from time import sleep_us

from HBridge_common import *

'''
             Vcc
              |
         +----+----+
         |         |
     ---S1         S3---
         +--motor--+
     ---S2         S4---
         |         |
         +----+----+
              |
             GND

| PWM1 | PWM2 | PWM3 | PWM4 | Function                             |
|:----:|:----:|:----:|:----:|--------------------------------------|
|  S1  |  S2  |  S3  |  S4  |                                      |
|------|------|------|------|--------------------------------------|
|   1  |   0  |   0  |  PWM | Motor moves forward                  |
|  PWM |   0  |   0  |   1  | -/-                                  |
|   0  |  PWM |   1  |   0  | Motor moves backward                 |
|   0  |   1  |  PWM |   0  | -/-                                  |
|   0  |   0  |   0  |   0  | Motor coasts (free runs)             |
|   1  |   0  |   0  |   0  | -/-                                  |
|   0  |   1  |   0  |   0  | -/-                                  |
|   0  |   0  |   1  |   0  | -/-                                  |
|   0  |   0  |   0  |   1  | -/-                                  |
|   1  |   0  |   1  |   0  | Brakes(decelerates) on the high side |
|   0  |   1  |   0  |   1  | Brakes(decelerates) on the low side  |
|   1  |   1  |   X  |   X  | Short circuit!                       |
|   X  |   X  |   1  |   1  | -/-                                  |
'''
class HBridge4Pwm:

    def __init__(self, pwm1, pwm2, pwm3, pwm4, reverse=False, freq=5_000, dead_time_us=1_000):
        if isinstance(pwm1, PWM):
            self.pwm1 = pwm1  # any states(0, 1, PWM) are possible at the start
        else:
            self.pwm1 = PWM(Pin(pwm1), freq=freq, duty_u16=0)  # low level at the start

        if isinstance(pwm2, PWM):
            self.pwm2 = pwm2  # any states(0, 1, PWM) are possible at the start
        else:
            self.pwm2 = PWM(Pin(pwm2), freq=freq, duty_u16=0)  # low level at the start

        if isinstance(pwm3, PWM):
            self.pwm3 = pwm3  # any states(0, 1, PWM) are possible at the start
        else:
            self.pwm3 = PWM(Pin(pwm3), freq=freq, duty_u16=0)  # low level at the start

        if isinstance(pwm4, PWM):
            self.pwm4 = pwm4  # any states(0, 1, PWM) are possible at the start
        else:
            self.pwm4 = PWM(Pin(pwm4), freq=freq, duty_u16=0)  # low level at the start

        self.reverse = reverse

        self.dead_time_us = dead_time_us

    def __repr__(self) -> str:
        return f'HBridge4Pwm({self.pwm1}, {self.pwm2}, {self.pwm3}, {self.pwm4}, reverse={self._reverse}, dead_time_us={self.dead_time_us})'

    def deinit(self) -> None:
        try:
            self.pwm1.deinit()
        except:
            pass
        try:
            self.pwm2.deinit()
        except:
            pass
        try:
            self.pwm3.deinit()
        except:
            pass
        try:
            self.pwm4.deinit()
        except:
            pass

    @property
    def reverse(self):
        return self._reverse

    @reverse.setter
    def reverse(self, reverse):
        self._reverse = bool(reverse)

    def stop(self):
        self.coast0()

    def coast0(self):
        self.pwm1.duty_u16(0)
        self.pwm3.duty_u16(0)
        self.pwm2.duty_u16(0)
        self.pwm4.duty_u16(0)
        sleep_us(self.dead_time_us)

    def forward(self, speed):
        self.pwm3.duty_u16(0)
        self.pwm2.duty_u16(0)
        sleep_us(self.dead_time_us)
        self.pwm1.duty_u16(U16)
        self.pwm4.duty_u16(speed)

    def backward(self, speed):
        self.pwm1.duty_u16(0)
        self.pwm4.duty_u16(0)
        sleep_us(self.dead_time_us)
        self.pwm3.duty_u16(U16)
        self.pwm2.duty_u16(speed)

    def breakh(self):
        self.pwm2.duty_u16(0)
        self.pwm4.duty_u16(0)
        sleep_us(self.dead_time_us)
        self.pwm1.duty_u16(U16)
        self.pwm3.duty_u16(U16)

    def breakl(self):
        self.pwm1.duty_u16(0)
        self.pwm3.duty_u16(0)
        sleep_us(self.dead_time_us)
        self.pwm2.duty_u16(U16)
        self.pwm4.duty_u16(U16)

    def coast1(self):
        self.pwm3.duty_u16(0)
        self.pwm2.duty_u16(0)
        self.pwm4.duty_u16(0)
        sleep_us(self.dead_time_us)
        self.pwm1.duty_u16(U16)

    def coast2(self):
        self.pwm1.duty_u16(0)
        self.pwm3.duty_u16(0)
        self.pwm4.duty_u16(0)
        sleep_us(self.dead_time_us)
        self.pwm2.duty_u16(U16)

    def coast3(self):
        self.pwm1.duty_u16(0)
        self.pwm2.duty_u16(0)
        self.pwm4.duty_u16(0)
        sleep_us(self.dead_time_us)
        self.pwm3.duty_u16(U16)

    def coast4(self):
        self.pwm1.duty_u16(0)
        self.pwm3.duty_u16(0)
        self.pwm2.duty_u16(0)
        sleep_us(self.dead_time_us)
        self.pwm4.duty_u16(U16)

    def go(self, speed: int | None) -> None:
        if speed is not None:  # Other than STOP mode
            if speed > 0:
                if self._reverse:
                    self.backward(speed)
                else:
                    self.forward(speed)
            elif speed < 0:
                if self._reverse:
                    self.forward(-speed)
                else:
                    self.backward(-speed)
            else:
                self.stop()
        else:
            self.stop()
