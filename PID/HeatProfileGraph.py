import minimalmodbus
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

countList = []
dataList = []
hottest = 0
coldest = 1000
def readTemp():  # this function reads the temperature
    while True:  #this loop ensures the hardware is connected
        try:
            PID = minimalmodbus.Instrument('COM3', 1, mode='rtu') #Set port and communication mode
            break
        except IOError:
            print('Failed to initialize, try again')
        except ValueError:
            print("Failed to initialize")
        time.sleep(.25)
    while True:
        try:
            PIDTemperature = PID.read_register(4096,1) #The 4096 is the decimal command of the hexidecimal command in the manual, the 1 is the number of decimals

            break
        except IOError or ValueError:
            print("Failed to read, trying again")

    return PIDTemperature




def writeTemp(goal):  # this function reads the temperature
    while True:  #this loop ensures the hardware is connected
        try:
            PID = minimalmodbus.Instrument('COM3', 1, mode='rtu') #Set port and communication mode
            break
        except IOError:
            print('Failed to initialize, try again')
        except ValueError:
            print("Failed to initialize")
        time.sleep(.25)
    while True:
        try:
            TargetTemp = PID.write_register(4097,goal,1) #The 4097 is the decimal command of the hexidecimal command in the manual, the 1 is the number of decimals

            break
        except IOError or ValueError:
            print("Failed to read, trying again")

    return TargetTemp



countList = [] # generate an empty list
dataList = [] # generate an empty list

plt.figure() # initialize a figure from matplotlib
plt.xlabel('Counts')
plt.ylabel('Temperature')
plt.title('Temperature plot')

while True:
    target = 40.2
    writeTemp(target)
    CurrentTemp = readTemp()
    countList.append(time.time()) # append the iterator i to countList
    dataList.append(CurrentTemp) # Make some data by appending the sine of the iterator to the dataList
    time.sleep(0.25) # wait for 0.25 second
    plt.plot(countList, dataList, color='green') # plot the data, make it green colored.
    plt.pause(0.01) # Pause the plot for 0.01 seconds


    if CurrentTemp >= target:
        print("Benchmark 1 reached")
        break

    else:
         True

while True:
    target = 30
    writeTemp(target)
    CurrentTemp = readTemp()
    countList.append(time.time())  # append the iterator i to countList
    dataList.append(CurrentTemp)  # Make some data by appending the sine of the iterator to the dataList
    time.sleep(0.25)  # wait for 0.25 second
    plt.plot(countList, dataList, color='green')  # plot the data, make it green colored.
    plt.pause(0.01)  # Pause the plot for 0.01 seconds

    if CurrentTemp <= target:
        print("Benchmark 2 reached")
        break

    else:
        True

while True:
    target = 55.6
    writeTemp(target)
    CurrentTemp = readTemp()
    countList.append(time.time())  # append the iterator i to countList
    dataList.append(CurrentTemp)  # Make some data by appending the sine of the iterator to the dataList
    time.sleep(0.25)  # wait for 0.25 second
    plt.plot(countList, dataList, color='green')  # plot the data, make it green colored.
    plt.pause(0.01)  # Pause the plot for 0.01 seconds

    if CurrentTemp >= target:
        print("Benchmark 3 reached")
        break

    else:
        True