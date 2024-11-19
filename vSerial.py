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

import subprocess
from subprocess import DEVNULL
import os
import signal
import serial
import time
import sys

termchars = '\r\n'
debug = False

class vCommHandler():
    def open(self, port):
        try:
            self.ser = serial.Serial(port, baudrate=115200, rtscts=True, dsrdtr=True, xonxoff=True, timeout=0.3, bytesize=8)
            self.port = port
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

    def reopen(self):
        success = False
        tries = 0
        while not success:
            tries = tries + 1
            if tries >= 25:
                return
            try:
                self.ser.close()
            except:
                pass
            try:
                time.sleep(1.5)
                subprocess.run("echo '2-1' | sudo tee /sys/bus/usb/drivers/usb/unbind",stdout=DEVNULL, stderr=DEVNULL, shell=True)
                subprocess.run("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind",stdout=DEVNULL, stderr=DEVNULL, shell=True)
                time.sleep(0.5)
                subprocess.run("echo '2-1' | sudo tee /sys/bus/usb/drivers/usb/bind",stdout=DEVNULL, stderr=DEVNULL, shell=True)
                subprocess.run("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/bind",stdout=DEVNULL, stderr=DEVNULL, shell=True)
                time.sleep(2.5)
                self.ser = serial.Serial(self.port, baudrate=115200, rtscts=True, dsrdtr=True, xonxoff=True, timeout=0.005, bytesize=8)
                success = True
            except Exception as e:
                print(e)
                print("trying again...")
                success = False


    def query(self, command):
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        global debug
        if(debug):
            print("Sending: "+command)
        command = command + termchars
        try:
            self.ser.write(command.encode())
        except:
            self.close()
            success = False
            loops = 0
            while not success:
                loops = loops + 1
                try:
                    self.ser.close()
                    self.ser = serial.Serial(self.port, baudrate=115200, rtscts=True, dsrdtr=True, xonxoff=True, timeout=0.005, bytesize=8)
                    success = True
                except Exception as e:
                    if(debug):
                        print(e)
                        print('write command')
                    success = False
                    time.sleep(0.1)
                    if loops >= 10:
                        if(debug):
                            print("\n============")
                            print("TRYING IT!!!")
                            print("============\n")
                        #input("press enter when ready.")
                        subprocess.run("echo '2-1' | sudo tee /sys/bus/usb/drivers/usb/unbind",stdout=DEVNULL, stderr=DEVNULL, shell=True)
                        subprocess.run("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind",stdout=DEVNULL, stderr=DEVNULL, shell=True)
                        time.sleep(0.5)
                        subprocess.run("echo '2-1' | sudo tee /sys/bus/usb/drivers/usb/bind",stdout=DEVNULL, stderr=DEVNULL, shell=True)
                        subprocess.run("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/bind",stdout=DEVNULL, stderr=DEVNULL, shell=True)
                        time.sleep(1)
                    if loops >= 30:
                        sys.exit(1)

            signal.signal(signal.SIGINT, s)
            return None

        sTime = time.time()
        in_waiting = 0
        while( in_waiting == 0 ):
            try:
                in_waiting = self.ser.in_waiting
            except:
                in_waiting = 0

            if( (time.time() - sTime) > 2 ):
                self.close()
                success = False
                loops = 0
                while not success:
                    loops = loops + 1
                    try:
                        try:
                            self.ser.close()
                        except:
                            pass
                        self.ser = serial.Serial(self.port, baudrate=115200, rtscts=True, dsrdtr=True, xonxoff=True, timeout=0.005, bytesize=8)
                        success = True
                    except Exception as e:
                        if debug:
                            print('waiting '+str(loops)+'...')
                            print(e)
                        success = False
                        time.sleep(0.1)
                        if loops >= 10:
                            if debug:
                                print("\n============")
                                print("TRYING IT!!!")
                                print("============\n")
                                #input("press enter when ready.")
                            subprocess.run("echo '2-1' | sudo tee /sys/bus/usb/drivers/usb/unbind",stdout=DEVNULL, stderr=DEVNULL, shell=True)
                            subprocess.run("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind",stdout=DEVNULL, stderr=DEVNULL, shell=True)
                            time.sleep(0.5)
                            subprocess.run("echo '2-1' | sudo tee /sys/bus/usb/drivers/usb/bind",stdout=DEVNULL, stderr=DEVNULL, shell=True)
                            subprocess.run("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/bind",stdout=DEVNULL, stderr=DEVNULL, shell=True)
                            time.sleep(3)
                        if loops >= 31:
                            sys.exit(1)
                signal.signal(signal.SIGINT, s)
                return None

        try:
            retStr = self.ser.readline().decode('ascii')
        except:
            self.ser.close()
            success = False
            loops = 0
            while not success:
                loops = loops + 1
                try:
                    self.ser = serial.Serial(self.port, baudrate=115200, rtscts=True, dsrdtr=True, xonxoff=True, timeout=0.005, bytesize=8)
                    success = True
                except Exception as e:
                    if debug:
                        print('readline')
                        print(e)
                    success = False
                    time.sleep(0.1)
                    if loops >= 10:
                        if debug:
                            print("\n============")
                            print("TRYING IT!!!")
                            print("============\n")
                            #input("press enter when ready.")
                        subprocess.run("echo '2-1' | sudo tee /sys/bus/usb/drivers/usb/unbind",stdout=DEVNULL, stderr=DEVNULL, shell=True)
                        subprocess.run("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind",stdout=DEVNULL, stderr=DEVNULL, shell=True)
                        time.sleep(0.5)
                        subprocess.run("echo '2-1' | sudo tee /sys/bus/usb/drivers/usb/bind",stdout=DEVNULL, stderr=DEVNULL, shell=True)
                        subprocess.run("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/bind",stdout=DEVNULL, stderr=DEVNULL, shell=True)
                        time.sleep(3)

            retStr = None

        signal.signal(signal.SIGINT, s)

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

