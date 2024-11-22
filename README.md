Please be aware that this is very much a work in progress and all functions are subject to change or drop.

# FrameBuffer.py
NeoPixel framebuffer for Circuitpython that's pretty damn quick

To keep the code fast this buffer uses GRB and GRBW format.

# Example code
## Simple example
Creat your framebuffer object, no need to include the neopixel.py helper library
```
import board
from FrameBuffer import FrameBuffer
PIXEL_GP = board.GP28
PIXEL_WIDTH = 32
PIXEL_HEIGHT = 8
fb = FrameBuffer(PIXEL_WIDTH, PIXEL_HEIGHT, PIXEL_GP, bpp=3, alternating=True)
```

Adjust a NeoPixel based on X,Y coords
```
fb.set(1,30, (192,10,255))  # Set the pixel at 1,30 to (192,10,255)
fb.clear(0,2)               # Resets a pixel to (0,0,0,0) or your defined "clear colour"
value = fb.get(19,4)        # Get the GRB value of 19,4 as a tuple
```

hline, vline, and rect functions
```
fb.hline(1,1,4, (0,0,255))              # Horizontal line at 1,1 that is 4 pixels long
fb.vline(5,5,10, (0,0,255))             # Vertical line at 5,5 that is 10 pixels long
fb.line(0,1,9,6, (255,0,0))             # Line from 0,1 to 9,6 (Bresenham's Algorithm)
fb.rect(5,4,4,4, (0,255,0), fill=True)  # Draw a rectangle at 5,4 that is 4x4 and has fill inabled
```

Working outside the buffer
```
fb[4] = (0,255,255)  # Set Neopixel at index 4 to 0,255,255
value = fb[9]        # Get the GRB value of Neopixel at index 9
del fb[15]           # Sets the Neopixel at index 15 to (0,0,0,0) or your defined "clear colour"
```

Other buffer methods
```
fb.fillbuffer((255,255,255))  # Fill the whole buffer with 255,255,255
fb.clearbuffer()              # Fill the whole buffer with 0,0,0 or your degined "clear colour"
fb.raw(bytearray(...))        # Replace buffer with a whole new byte array
bytes = fb.dump()             # Copy buffer to another bytearray or function
```

Experimental features and brightness controls
```
fb = FrameBuffer(PIXEL_WIDTH, PIXEL_HEIGHT, PIXEL_GP, bpp=3, alternating=True, brightness=0.1)                      # Sets global brightness to 10%
fb = FrameBuffer(PIXEL_WIDTH, PIXEL_HEIGHT, PIXEL_GP, bpp=3, alternating=True, advbrightness=True)                  # Turns on per-pixel brightness control via brightness table.
fb = FrameBuffer(PIXEL_WIDTH, PIXEL_HEIGHT, PIXEL_GP, bpp=3, alternating=True, brightness=0.5, advbrightness=True)  # Turns on per-pixel brightness and sets the default to 50%
fb.brightnesstable[11] = 0.25                                                                                       # Set Neopixel at index 11 to 25% brightness
```
