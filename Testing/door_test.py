import serial
import time


ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)

# ser.setRTS(True)
print(ser.rts)
time.sleep(3)

ser.setRTS(False)

time.sleep(3)

ser.setRTS(True)
