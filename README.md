# Raspberry Pi Pico WS2812B Ring Light Control
Raspberry Pi Pico RGB LED (WS2812) Ring Light Control with MicroPython 

### JUMP TO:
<a href="#start">- Wiring Diagram</a><br>
<a href="#state">- MicroPython State Machine</a><br>
<a href="#simple">- Simple LED Array Loop </a><br>

The RPi Pico WS2812 library can be downloaded using git:

    git clone https://github.com/makerportal/rpi-pico-ws2812

<a id="start"></a>
# - Wiring Diagram -
The wiring diagram between the Raspberry Pi Pico and a 16-pixel RGB LED ring light is shown below:

![Wiring Diagram](./images/rpi_pico_w_power_supply_WS2812_ring_white.jpg)

The pinout wiring is also given in the table below:

| Power Supply | Pico | Ring Light |
| --- | --- | --- |
| + | N/A | 5V |
| N/A | GPIO13 | DI | 
| - | GND | GND |

Most of the GPIO pins can be used to control the WS2812 LED array, thus, the specification of GPIO13 for controlling the light is arbitrary. Be sure to change the pin in the codes as well, if using another pin for wiring.

<a id="state"></a>
# - MicroPython State Machine -
The 16-Pixel RGB LED ring light array will be controlled using the scheme outlined in the [Raspberry Pi Pico MicroPython getting started document](https://datasheets.raspberrypi.org/pico/raspberry-pi-pico-python-sdk.pdf), where we can get started with the tutorial entitled “Using PIO to drive a set of NeoPixel Ring (WS2812 LEDs).” The tutorial contains a script that will be used to create a state machine on the RPi Pico. The state machine will be used to control the LEDs on the ring light using a single pin on the Pico (GPIO13 in the wiring above). The full MicroPython example script can also be found at the Raspberry Pi Pico’s [NeoPixel Ring repository](https://github.com/raspberrypi/pico-micropython-examples/blob/master/pio/neopixel_ring/neopixel_ring.py).

The code to start the state machine on the Pico's GPIO pin #13 is given below:

```python
import array, time
from machine import Pin
import rp2
#
############################################
# RP2040 PIO and Pin Configurations
############################################
#
# WS2812 LED Ring Configuration
led_count = 16 # number of LEDs in ring light
PIN_NUM = 13 # pin connected to ring light
brightness = 0.5 # 0.1 = darker, 1.0 = brightest

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT,
             autopull=True, pull_thresh=24) # PIO configuration

# define WS2812 parameters
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()


# Create the StateMachine with the ws2812 program, outputting on pre-defined pin
# at the 8MHz frequency
state_mach = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))

# Activate the state machine
state_mach.active(1)
```
The snippet of code given above will be used for each algorithm used to test the 16-pixel WS2812 LED ring light.

<a id="simple"></a>
# - Simple LED Array Loop -
The following corresponds to the script entitled:

