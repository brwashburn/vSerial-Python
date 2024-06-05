

#======INCLUDES=======#
from vSerial import vCommHandler
import sys


#======FUNCTION DEFINITIONS=======#





#======CONNECTION=======#

port = input("SLICE COM Port: ")
port = "COM"+str(port)

dev = vCommHandler()
dev.open(port)


#======USAGE EXAMPLE=======#
print("\nConnected.  Querying...")

reply = dev.query("*IDN?")

print("Response: " + reply)
#print(reply)



#======START OF USER CODE=======#
