from machine import Pin, PWM, Signal

from HBridge_common import *

'''
| Dir | PWM | Function       |
|:---:|:---:|----------------|
|  1  | PWM | Motor forward  |
|  0  | PWM | Motor backward |
|  X  |  0  | Park brake     |
'''
class HBridgeDirPwm:

    def __init__(self, dir, pwm, reverse=False, freq=5_000) -> None:
        if isinstance(dir, Pin):
            self.dir = dir  # any level is possible at the start
        else:
            self.dir = Pin(dir, mode=Pin.OUT, value=0)  # low level at the start

        if isinstance(pwm, PWM):
            self.pwm = pwm  # any states(0, 1, PWM) are possible at the start
        else:
            if not isinstance(pwm, Pin):
                pwm = Pin(pwm)
            self.pwm = PWM(pwm, freq=freq, duty_u16=0)  # low level at the start

        self.reverse = reverse

    def __repr__(self) -> str:
        return f'HBridgeDirPwm({self.dir}, {self.pwm}, reverse={self._reverse})'

    def deinit(self) -> None:
        try:
            self.pwm.deinit()
        except:
            pass

    @property
    def reverse(self):
        return self._reverse

    @reverse.setter
    def reverse(self, reverse):
        self._reverse = bool(reverse)

    def stop(self):
        self.pwm.duty_u16(0)

    def go(self, speed: int | None) -> None:
        if speed is not None:                       # Other than STOP mode
            self.dir((speed > 0) != self._reverse)  # self.dir(True) switches to high == Forward
            self.pwm.duty_u16(abs(speed))
        else:
            self.stop()
