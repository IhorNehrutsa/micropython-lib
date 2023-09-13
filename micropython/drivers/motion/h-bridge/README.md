## Full H-Bridge integrated circuit drivers

This directory contains software drivers for managing hardware H-bridge drivers.

 ![image](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/H_bridge.svg/310px-H_bridge.svg.png)

 [Schematic of an H-bridge (highlighted in red) from Wikipedia.](https://en.wikipedia.org/wiki/H-bridge)

All HBridgeXXX classes have an init constructor, repr, deinit, go and stop functions.

```
U16 = 2**16


class HBridgeXXX:

    def __init__(self, ... *, reverse=False, freq=5_000 ) -> None:
        ...
        # reverse - reverse motor direction
        # freq - default PWM frequency

    def __repr__(self) -> str:
        ...

    def deinit(self) -> None:
        ...

    def go(self, speed: int | None) -> None:
        ...
        # speed in range from -U16 to +U16

    def stop(self) -> None:
        ...
```

Any HBridgeXXX class can be called in the HBridgeEn class(from HBridge_commom.py),
which adds the Enable/_Enable functionality(with high or low active level):

```
class HBridgeEn:

    def __init__(self, motor: HBridgeXXX, en : Signal | Pin | pin_number):
        ...
```


* ### 1) PWM/Dir H-Bridge driver

Equivalent circuit is:

![image](https://github.com/IhorNehrutsa/micropython-lib/assets/70886343/5738d4cb-a12f-429e-995d-d503724a9849)

| Dir | PWM | Function       |
|:---:|:---:|----------------|
|  1  | PWM | Motor forward  |
|  0  | PWM | Motor backward |
|  X  |  0  | Park brake     |

Examples:
```
motor = HBridgeDirPwm(23, 26)
    # inside dir and pwm are initialized as:
    # self.dir = Pin(23, mode=Pin.OUT, value=0)   # dir is low level at the start
    # self.pwm = PWM(26, freq=5_000, duty_u16=0)  # pwm is low level at the start
motor.go(2**16//2)  # 50% of speed
```
or add the Enable functionality
```
motor = HBridgeEn(HBridgeDirPwm(23, 26), 25)  # en is high level at the start
print(motor)
```
or change all default levels, direction and freq
```
dir = Pin(23, mode=Pin.OUT, value=1)                         # dir is high level at the start
pwm = PWM(26, freq=5_000, duty_u16=2**16)                    # pwm is high level at the start
motor = HBridgeDirPwm(dir, pwm, reverse=True, freq = 1_000)  # change of forward/backward and user defined PWM freq
motor.stop()
```

**An example of the Noname module: L6384(High-voltage half bridge driver) + IRF3205(HEXFET Power MOSFET)**

Rated voltage: 3-36 V

Rated current: 10 A

Peak current: 30 A

![image](https://github.com/IhorNehrutsa/micropython-lib/assets/70886343/eff2c908-921c-463d-ae92-af45e31d21cb)



* ### 2) 4PWM/4IN H-Bridge driver

Equivalent circuit is:

![image](https://github.com/IhorNehrutsa/micropython-lib/assets/70886343/3ad73687-16d0-44f5-9991-e068b461bbae)


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

where:

PWM1 - High side left aka S1

PWM2 - Lower left aka S2

PWM3 - High side right aka S3

PWM4 - Lower right aka S4

For example:
```
motor = HBridge4Pwm(22, 4, 23, 2)
motor.go(2**16//4)  # 25% of speed
```

**An example of the Noname module: RF5305 + T60N03G (Power MOSFET)**

Rated voltage: 5-27 V

Rated current: 5 A

Support PWM signal frequency within 20KHz.

**`Attention: Connect PWM1 to the IN1, PWM2 to the IN3, PWM3 to the IN2, PWM4 to the IN4!`**

![image](https://github.com/IhorNehrutsa/micropython-lib/assets/70886343/277a5ec9-4266-4c6d-8855-8174c7261a22)

* ### 3) 2MCPWM/4IN H-Bridge driver

Equivalent circuit is:

![image](https://github.com/IhorNehrutsa/micropython-lib/assets/70886343/1bc78b01-6c67-4a6b-ab3e-01095e6bf25f)


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

where:

MCPWM1 - High side left aka S1, Lower left aka S2

MCPWM2 - High side right aka S3, Lower right aka S4

For example:
```
motor = HBridge2McPwm(22, 4, 23, 2)
motor.go(2**16//4)  # 25% of speed
```

* ### 4) IN1/IN2/PWM H-Bridge driver

TB6612 based modules

For example:
```
IN1 = 22
IN2 = 4
PWM_PIN = 23
STBY= 2  # Enable is high level
motor = HBridgeEn(HBridgeInInPwm(IN1, IN2, PWM_PIN), STBY)  # start in Standby mode
```

* ### 5) PWM1/PWM2 H-Bridge driver
DRV8871, DRV8837, DRV8838 based modules


* ### 6) L298, L293 and L9110 based modules

