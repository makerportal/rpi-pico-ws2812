###############################################################
# WS2812 RGB LED Ring Light Single-Pixel Loop
# with the Raspberry Pi Pico Microcontroller
#
# by Joshua Hrisko, Maker Portal LLC (c) 2021
#
# Based on the Example neopixel_ring at:
# https://github.com/raspberrypi/pico-micropython-examples
###############################################################
#
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

# Range of LEDs stored in an array
pixel_array = array.array("I", [0 for _ in range(led_count)])
#
############################################
# Functions for RGB Coloring
############################################
#
def update_pix(brightness_input=brightness): # dimming colors and updating state machine (state_mach)
    dimmer_array = array.array("I", [0 for _ in range(led_count)])
    for ii,cc in enumerate(pixel_array):
        r = int(((cc >> 8) & 0xFF) * brightness_input) # 8-bit red dimmed to brightness
        g = int(((cc >> 16) & 0xFF) * brightness_input) # 8-bit green dimmed to brightness
        b = int((cc & 0xFF) * brightness_input) # 8-bit blue dimmed to brightness
        dimmer_array[ii] = (g<<16) + (r<<8) + b # 24-bit color dimmed to brightness
    state_mach.put(dimmer_array, 8) # update the state machine with new colors
    time.sleep_ms(10)

def set_24bit(ii, color): # set colors to 24-bit format inside pixel_array
    pixel_array[ii] = (color[1]<<16) + (color[0]<<8) + color[2] # set 24-bit color

#
############################################
# Main Loops and Calls
############################################
#
color = (255,0,0) # looping color
blank = (255,255,255) # color for other pixels
cycles = 5 # number of times to cycle 360-degrees
for ii in range(int(cycles*len(pixel_array))+1):
    for jj in range(len(pixel_array)):
        if jj==int(ii%led_count): # in case we go over number of pixels in array
            set_24bit(jj,color) # color and loop a single pixel
        else:
            set_24bit(jj,blank) # turn others off
    update_pix() # update pixel colors
    time.sleep(0.05) # wait 50ms
