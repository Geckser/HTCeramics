import minimalmodbus
import time
import sys
import time
import matplotlib.pyplot as plt
import numpy as np
import keyboard

tempList = []
timeList = []
temperatureSet = input("please enter a temperature setting: ")
startTime = time.time()
plt.figure()
plt.xlabel("Time")
plt.ylabel("Temperature")
plt.title("Temp vs. Time")

def plotData(temperatureSet):

    time.sleep(.25)
    while True:
        try:
            PID = minimalmodbus.Instrument('COM3',  1, mode='rtu',  close_port_after_each_call=True) # CHANGE THIS COM PORT!!!!!!
            PID.write_register(4098, 999, 1)
            PID.write_register(4099, 0, 1)
            break
        except IOError:
            print('Failed to initialize, trying again.')
        except ValueError:
            print('Failed to initialize, trying again.')

    while True:
        try:
            PID = minimalmodbus.Instrument('COM3',  1, mode='rtu',  close_port_after_each_call=True) # CHANGE THIS COM PORT!!!!!!

            PIDTemperature = PID.read_register(4096, 1)

            tempList.append(PIDTemperature)
            runTime = time.time() - startTime
            timeList.append(runTime)
            plt.plot (timeList, tempList, color = 'green')
            plt.pause(0.01)

        except IOError:
            print("Failed to read, trying again")
        except ValueError:
            print("Failed to read, trying again")
        break

    if temperatureSet == "none":
        temperatureSet = 30
        plt.axhline(y = temperatureSet)

    else:
        temperatureSet = float(temperatureSet)
        plt.axhline(y = temperatureSet)

    try:
        PID = minimalmodbus.Instrument('COM3',  1, mode='rtu',  close_port_after_each_call=True) # CHANGE THIS COM PORT!!!!!!

        PID.write_register(4097, temperatureSet, 1)
        PID.write_bit(2067, 1, functioncode = 5)

    except minimalmodbus.NoResponseError:
        plotData(temperatureSet)
    #PID.write_register(4101, 3)

while True:
    if keyboard.is_pressed("right shift"):
        PID = minimalmodbus.Instrument('COM3',  1, mode='rtu',  close_port_after_each_call=True) # CHANGE THIS COM PORT!!!!!!
        temperatureSet = 15
        PID.write_register(4097, temperatureSet, 1)
        print("Shutting down")
        exit()

    if keyboard.is_pressed("i"):
        temperatureSet = input("New temp setting: ")
        plotData(temperatureSet)

    else:
        plotData(temperatureSet)
