## File: EXAMPLE_QTC_temp_logger.py
## Date: 1/25/2023
## Updated: 6/5/2024
##
##
## In this example, temperature data is logged from a SLICE-QTC
## for 30 seconds, and then that data is plotted via Matplotlib.
##
## Requires Matplotlib and vSerial.
##

import serial
import time

from vSerial import vCommHandler

TST = 1.0 # Temperature Stability Threshold (mK)

_returnStr = ""

global qtc
qtc = vCommHandler()


comport = input("COM Port Number: ")
channel = int(input("QTC Channel: "))
if (channel < 1) or (channel > 4):
    print("Invalid channel, exiting.")
    sys.exit(1)

comport = "COM"+comport

qtc.open(comport)

setpt = qtc.query("tempset? {channel}")
temp_query = f"temp? {channel}"

t_start = time.time()

terrors = []
times = []

t_now = time.time()

while( t_now - t_start < 30): # Gather data for 30 seconds
    response = qtc.query(temp_query)
    terrors.append(float(response))
    times.append(t_now)
    t_now = time.time()
    print(response)

from datetime import datetime as dt

tstamp = dt.isoformat(dt.now())
fileName = "qtc_log_"+tstamp.split('.')[0].replace(':','-')+".txt"

for t in times:
    t = t - t_start

with open(fileName,'x') as oFile:
    for t in times:
        oFile.write(str(t))
        oFile.write(' ')
    oFile.write('\n')
    for t in terrors:
        oFile.write(str(t))
        oFile.write(' ')

import matplotlib.pyplot as plt

print("len: "+str(len(terrors)))

fig, ax = plt.subplots()

ax.plot(times, terrors)

plt.show()



