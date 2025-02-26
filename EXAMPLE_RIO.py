# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 11:49:12 2025

@author: fcomb


•	“TEMPSET? 0” to query the RIO temperature set point.
•	“TEMPSET 0 XX.XXXX” to change the temperature set point to XX.XXXX in deg C.





"""

from vSerial import vCommHandler
import sys


#======START OF USER CODE=======#
if __name__ == "__main__":
    port = 'COM10'
    dev = vCommHandler()
    dev.open(port)
    print(float(dev.query('TEMPSET? 0')))
