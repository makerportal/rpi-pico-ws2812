# Raspberry Pi Pico WS2812B Ring Light Control
Raspberry Pi Pico RGB LED (WS2812) Ring Light Control with MicroPython 

### JUMP TO:
<a href="#start">- Wiring Diagram</a><br>
<a href="#state">- MicroPython State Machine</a><br>
<a href="#google">- Google Home LED Emulator </a><br>

The RPi Pico WS2812 library can be downloaded using git:

    git clone https://github.com/makerportal/rpi-pico-ws2812

<a id="start"></a>
# - Wiring Diagram -
The wiring diagram between the Raspberry Pi Pico and a 16-pixel RGB LED ring light is shown below:

![Wiring Diagram](./images/rpi_pico_w_power_supply_WS2812_ring_white.jpg)

The pin wiring is also given in the table below:

| Power Supply | Pico | Ring Light |
| --- | --- | --- |
| 5V | N/A | 5V |
| N/A | GPIO13 | DI | 
| GND | GND | GND |

<a id="state"></a>
# - MicroPython State Machine -

<a id="google"></a>
# - Google Home LED Emulator -
