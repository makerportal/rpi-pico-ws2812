###############################################################
# WS2812 RGB LED Ring Light Multi-Example
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
brightness = 0.1 # 0.1 = darker, 1.0 = brightest

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
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))

# Activate the state machine
sm.active(1)

# Range of LEDs stored in an array
ar = array.array("I", [0 for _ in range(led_count)])
#
############################################
# Functions for RGB Coloring
############################################
#
def pixels_show(brightness_input=brightness):
    dimmer_ar = array.array("I", [0 for _ in range(led_count)])
    for ii,cc in enumerate(ar):
        r = int(((cc >> 8) & 0xFF) * brightness_input) # 8-bit red dimmed to brightness
        g = int(((cc >> 16) & 0xFF) * brightness_input) # 8-bit green dimmed to brightness
        b = int((cc & 0xFF) * brightness_input) # 8-bit blue dimmed to brightness
        dimmer_ar[ii] = (g<<16) + (r<<8) + b # 24-bit color dimmed to brightness
    sm.put(dimmer_ar, 8) # update the state machine with new colors
    time.sleep_ms(10)

def pixels_set(i, color):
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2] # set 24-bit color

def pixels_fill(color):
    for ii in range(len(ar)):
        pixels_set(ii, color) # show all colors
        
def breathing_led(color):
    step = 5
    breath_amps = [ii for ii in range(0,255,step)]
    breath_amps.extend([ii for ii in range(255,-1,-step)])
    for ii in breath_amps:
        for jj in range(len(ar)):
            pixels_set(jj, color) # show all colors
        pixels_show(ii/255)
        time.sleep(0.01)

def color_chase(color, wait):
    for ii in range(led_count): # turn on each color 
        pixels_set(ii, color)
        time.sleep(wait) # wait between each turn on
        pixels_show()
    time.sleep(0.2)
 
def wheel(pos): # gives the illusion of a traveling color wheel
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)
 
 
def rainbow_cycle(wait):
    for jj in range(255):
        for ii in range(led_count):
            rc_index = (ii * 256 // led_count) + jj
            pixels_set(ii, wheel(rc_index & 255))
        pixels_show()
        time.sleep(wait)
#
############################################
# Main Calls and Loops
############################################
#
# color specifications
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
cyan = (0,255,255)
white = (255,255,255)
colors = (blue, yellow, green, cyan, red, white)

# loop calls to rgb led change functions 
for color in colors: # all LEDs iterate through each color 
    pixels_fill(color)
    pixels_show()
    time.sleep(0.5)
    
for color in colors: # emulate breathing LED (similar to Amazon's Alexa)
    breathing_led(color) 
    
for color in colors: # Turn on one color for each LED individually
    color_chase(color, 0.02)
     
rainbow_cycle(0) # cycling rainbow wheel

pixels_fill((255,255,255)) # end with bright white light
pixels_show()

