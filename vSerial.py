## File: vSerial.py
## Auth: Vescent Technologies, Inc.
## Date: 2024-06-05
## Version: 1.0
## 
## Desc: A library for quick development of excellently-implemented 
##       SLICE Serial Control scripts.
##
## ========================================================================== ##
##
## MIT License
##
## Copyright (c) 2024 Vescent Technologies, Inc.
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in all
## copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
## SOFTWARE.
## 
## ========================================================================== ##
## 

import signal
import serial
import time

termchars = '\r\n'
debug = False

class vCommHandler():
    def open(self, port):
        try:
            self.ser = serial.Serial(port, baudrate=115200, rtscts=True, dsrdtr=True, xonxoff=True, timeout=0.3, bytesize=8)
        except:
            print("Port %s Unavailable" % port)
            return False
        return True

    def close(self):
        try:
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.close()
        except:
            pass
        return

    def query(self, command):
        global debug
        if(debug):
            print("Sending: "+command)

        s = signal.signal(signal.SIGINT, signal.SIG_IGN)


        command = command + termchars
        self.ser.write(command.encode())

        sTime = time.time()
        while( self.ser.in_waiting == 0 ):
            if( (time.time() - sTime) > 5 ):
                self.close()
                print("No response, connection with device lost.")
                time.sleep(1)
                print("The program will now exit.")
                time.sleep(3)
                sys.exit(1)
        retStr = self.ser.readline().decode('ascii')

        signal.signal(signal.SIGINT, s)

        if(debug):
            print("Response: "+retStr)

        return retStr


    def send(self, command):
        command = command + termchars
        self.ser.write(command.encode())
        return

    def flush(self):
        self.ser.flushInput()
        self.ser.flushOutput()
        return

    def __del__(self):
        self.close()

