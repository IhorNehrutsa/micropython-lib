from machine import Pin, Signal
from esp32 import MCPWM
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
|   1  |   0  | _PWM |  PWM | Motor moves forward                  |
|  PWM | _PWM |   0  |   1  | -/-                                  |
| _PWM |  PWM |   1  |   0  | Motor moves backward                 |
|   0  |   1  |  PWM | _PWM | -/-                                  |
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
class HBridge2McPwm:

    def __init__(self, mcpwm1h, mcpwm1l, mcpwm2h, mcpwm2l, reverse=False, freq=5_000, dead_time_us=1_000):
        self.mcpwm1 = PWM(0, mcpwm1h, mcpwm1l, freq=freq, duty_u16=0)  # low level at the start
        self.mcpwm2 = PWM(1, mcpwm2h, mcpwm2l, freq=freq, duty_u16=0)  # low level at the start

        self.reverse = reverse

        self.dead_time_us = dead_time_us

    def __repr__(self) -> str:
        return f'HBridge2McPwm({self.mcpwm1}, {self.mcpwm2}, reverse={self._reverse}, dead_time_us={self.dead_time_us})'

    def deinit(self) -> None:
        try:
            self.mcpwm1.deinit()
        except:
            pass
        try:
            self.mcpwm2.deinit()
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
        self.mcpwm1.duty_u16(0)
        self.mcpwm2.duty_u16(0)
        sleep_us(self.dead_time_us)

    def forward(self, speed):
        self.mcpwm2.duty_u16(0)
        sleep_us(self.dead_time_us)
        self.mcpwm1.duty_u16(U16)

    def backward(self, speed):
        self.mcpwm1.duty_u16(0)
        sleep_us(self.dead_time_us)
        self.mcpwm2.duty_u16(speed)

    def breakh(self):
        self.mcpwm2.duty_u16(0)
        sleep_us(self.dead_time_us)
        self.mcpwm1.duty_u16(U16)

    def breakl(self):
        self.mcpwm1.duty_u16(0)
        sleep_us(self.dead_time_us)
        self.mcpwm2.duty_u16(U16)

    def coast1(self):
        self.mcpwm2.duty_u16(0)
        sleep_us(self.dead_time_us)
        self.mcpwm1.duty_u16(U16)

    def coast2(self):
        self.mcpwm1.duty_u16(0)
        sleep_us(self.dead_time_us)
        self.mcpwm2.duty_u16(U16)

    def coast3(self):
        self.mcpwm1.duty_u16(0)
        self.mcpwm2.duty_u16(0)
        sleep_us(self.dead_time_us)

    def coast4(self):
        self.mcpwm1.duty_u16(0)
        self.mcpwm2.duty_u16(0)
        sleep_us(self.dead_time_us)

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



from time import sleep
m = MCPWM(0, (16,17), waveform=14, deadtime=2**16//8)
print(m)
print(dir(m))
1/0
m.force00()
m.force01()
m.force10()
m.force_10()
m.force0_1()
m.force_1_1()
m.pause()
m.resume()
m.freq(1000)
