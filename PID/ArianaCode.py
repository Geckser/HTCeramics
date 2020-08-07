import matplotlib.pyplot as plt
import serial
import time
#'/dev/tty.usbserial-COMP4'
#AB0JU8VHA\0000
#baudrate='115200',bytesize=8
#115200
#PID_6001
#USB\VID_0403&amp;PID_6001&amp;REV_0600
#PID = minimalmodbus.Instrument('COM3',  1, mode='rtu',  close_port_after_each_call=True)
#relay = serial.Serial (COM=4,baudrate='115200',bytesize=8)
#how long it's off
relay = serial.Serial ('COM4', baudrate='115200',bytesize=8)
relay.write(serial.to_bytes([170, 3, 254, 108, 1, 24]))  # Close relay 1
time.sleep(5)
relay.write(serial.to_bytes([170, 3, 254, 109, 1, 25]))  # Close relay 2
time.sleep(5)
#how long it's on
relay.write(serial.to_bytes([170, 3, 254, 100, 1, 16]))  # Open relay 1
time.sleep(2)
relay.write(serial.to_bytes([170, 3, 254, 101, 1, 17]))  # Open relay 2
time.sleep(2)

voltageList = []
countList = []
count = 0
plt.figure()
while True:
    relay.write(serial.to_bytes([170, 2, 254, 150, 64]))  #
    time.sleep(5)
    count += 1
    for i in range(0, 4):
        value = relay.read(1)
        #print(value)
        if i == 2:
            read = ord(value)
            print('read: ', read)
            voltage = (int(read) / 255) * 5
            voltageList.append(voltage)
            countList.append(count)
            print(voltage)
    plt.plot(countList, voltageList)
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.pause(0.01)







