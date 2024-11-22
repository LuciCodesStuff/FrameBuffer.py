from neopixel_write import neopixel_write
import digitalio

def clamp(value, min, max):
    return max(min(value,max),min)

class FrameBuffer:
    def __init__(self, width, height, gp, brightness=1, bpp=3, alternating=True, clearcolour=(0,0,0,0), advbrightness=False):
        self.bpp = bpp
        self.clearcolour = tuple(clearcolour[i] for i in range(self.bpp))
        self.width = width
        self.height = height
        self.gp = digitalio.DigitalInOut(gp)
        self.gp.direction = digitalio.Direction.OUTPUT
        self.brightness = brightness
        self.alternating = alternating
        self.buffer = self._bufferCreate(self.clearcolour)
        self.advbrightness = advbrightness
        if self.advbrightness: self.brightnesstable = [self.brightness]*(self.width*self.height)
        self.show() # Clear!

    def raw(self, bytes):
        if self.alternating:
            for x in range(self.width):
                self.buffer[(x * self.height) * self.bpp:(x * self.height) * self.bpp + self.height ] = bytes[(x * self.height) * self.bpp:(x * self.height) * self.bpp + self.height]
        else:
            self.buffer = bytes[:]
    def dump(self):
        return self.buffer[:]

    def set(self, x, y, colour):
        #x,y = index # width, height
        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1:
            return
        if x % 2 == 0 or not self.alternating:
            byteindex = (x * self.height + y) * self.bpp
        else:
            byteindex = (x * self.height + (self.height - 1 - y)) * self.bpp
        for i in range(self.bpp):
            self.buffer[byteindex + i] = colour[i]
    def get(self, x, y):
        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1:
            return
        if x % 2 == 0 or not self.alternating:
            byteindex = (x * self.height + y) * self.bpp
        else:
            byteindex = (x * self.height + (self.height - 1 - y)) * self.bpp
        return tuple(self.buffer[byteindex + i] for i in range(self.bpp))
    def clear(self, x, y):
        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1:
            return
        if x % 2 == 0 or not self.alternating:
            byteindex = (x * self.height + y) * self.bpp
        else:
            byteindex = (x * self.height + (self.height - 1 - y)) * self.bpp
        for i in range(self.bpp):
            self.buffer[byteindex + i] = self.clearcolour[i]
    
    def hline(self, x, y, length, colour):
        if length < 0:
            for i in range(0, -length):
                self.set(x - i, y, colour)
        else:
            for i in range(length):
                self.set(x + i, y, colour)
    def vline(self, x, y, length, colour):
        if length < 0:
            for i in range(0, -length):
                self.set(x, y - i, colour)
        else:
            for i in range(length):
                self.set(x, y + i, colour)
    # Bresenham's Line Algorithm
    def line(self, x, y, x2, y2, colour):
        dx = abs(x2 - x)
        dy = abs(y2 - y)
        sx = 1 if x < x2 else -1
        sy = 1 if y < y2 else -1
        err = dx - dy

        while x != x2 or y != y2:
            self.set(x, y, colour)
            e2  = err * 2
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
    def rect(self, x, y, width, height, colour, fill=False):
        if fill:
            for i in range(width):
                for j in range(height):
                    self.set(x + i, y + j, colour)
        else:
            for i in range(width + 1):
                self.set(x + i, y, colour)
                self.set(x + i, y + height, colour)
            for i in range(height + 1):
                self.set(x, y + i, colour)
                self.set(x + width, y + i, colour)

    def fillbuffer(self, colour):
        self.buffer = self._bufferCreate(colour)
    def clearbuffer(self):
        self.buffer = self._bufferCreate(self.clearcolour)

    def adjust(self, x, y, factor):
        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1:
            return
        if x % 2 == 0 or not self.alternating:
            byteindex = (x * self.height + y) * self.bpp
        else:
            byteindex = (x * self.height + (self.height - 1 - y)) * self.bpp
        self.brightnesstable[byteindex] = factor

    def adjustall(self,factor):
        for i in range(self.width*self.height*self.bpp):
            self.buffer[i] = (min(max((int(self.buffer[i] * factor)),0), 255))

    def __getitem__(self, index):
        byteindex = index * self.bpp
        return tuple(self.buffer[byteindex + i] for i in range(self.bpp))
    def __setitem__(self, index, colour):
        byteindex = index * self.bpp
        for i in range(self.bpp):
            self.buffer[byteindex + i] = colour[i]
    def __delitem__(self, index):
        byteindex = index * self.bpp
        for i in range(self.bpp):
            self.buffer[byteindex + i] = self.clearcolour[i]

    def show(self):
        if self.advbrightness:
            neopixel_write(self.gp,self._adjustAdvBrightness(self.buffer))
        elif self.brightness < 1:
            neopixel_write(self.gp,self._adjustBrightness(self.buffer))
        else:
            neopixel_write(self.gp,self.buffer)

    def _bufferCreate(self, colour):
        buffer = bytearray()
        for i in range(self.width * self.height):
            for j in range(self.bpp):
                buffer.append(colour[j])
        return buffer
    
    def _adjustAdvBrightness(self, buffer):
        print(i for j in range(self.bpp) for i in range(self.width*self.height))
        return bytearray([int(buffer[i+j] * self.brightnesstable[i]) for j in range(self.bpp) for i in range(self.width*self.height)])

    def _adjustBrightness(self, buffer):
        return bytearray([int(pixel * self.brightness) for pixel in buffer])
