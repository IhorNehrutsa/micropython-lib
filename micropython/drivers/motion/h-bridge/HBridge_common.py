from machine import Pin, Signal

# Constants for Modes of the motor.go() function:
STOP = None  # Usually the driver outputs in high impedance, free running of the motor
BRAKE = 0    # Usually the driver outputs in short brake

# The maximum parameter for PWM.duty_u16(): in some ports 2**16 - 1, in others 2**16.
U16 = 2**16

# Use these functions to convert percentages to i16 duty and back:

def percentages_to_i16(percentages: int) -> int:
    # percentages range from -100 to 100
    return min(max((percentages * U16 + 50) // 100, -U16), U16)

def i16_to_percentages(u16: int) -> int:
    return min(max((u16 * 100 + U16 // 2) // U16, -U16), U16)


class HBridgeEn:

    def __init__(self, motor, en):
        self.motor = motor

        if isinstance(en, Signal):
            self.en = en  # any level is possible at the start, low level as enable is possible
        elif isinstance(en, Pin):
            self.en = en  # any level is possible at the start
        else:
            self.en = Pin(en, mode=Pin.OUT, value=1)  # high level at the start

    def __repr__(self):
        return f'HBridgeEn({self.motor}, {self.en})'

    def deinit(self):
        self.motor.deinit()

    def stop(self):
        self.motor.stop()
        self.en(0)

    def go(self, speed: int | None):
        self.en(1 if speed else 0)
        self.motor.go(speed)
