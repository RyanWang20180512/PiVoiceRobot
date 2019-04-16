import re
import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

class Matrix_Led:
    '''
    Use matrix led to a little interaction
    '''
    def __init__(self,cascaded,block_orientation,rotate):
        # create matrix device
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, cascaded=cascaded or 1, block_orientation=block_orientation, rotate=rotate or 0)
        
    def setBrightChar(self,char):
        with canvas(self.device) as draw:
            text(draw,(0,0),chr(char),fill='white')
            text(draw,(8,0),chr(char),fill='white')
        self.brightContrast=0
        self.brightPlus=True
        self.device.contrast(self.brightContrast)
        
    def brightChar(self):
        if self.brightPlus is True:
            self.brightContrast+=1
            self.device.contrast(self.brightContrast)
            if self.brightContrast==255:
                self.brightPlus=False
        else:
            self.brightContrast-=1
            self.device.contrast(self.brightContrast)
            if self.brightContrast==0:
                self.brightPlus=True

    def setScrollChar(self,char):
        self.scrollPos=16
        self.scrollChar=char
        with canvas(self.device) as draw:
            text(draw,(self.scrollPos,0),chr(char),fill='white')

    def scrollingChar(self):
        self.scrollPos-=1
        with canvas(self.device) as draw:
            text(draw,(self.scrollPos,0),chr(self.scrollChar),fill='white')
        if self.scrollPos==-8:
            self.scrollPos=16
