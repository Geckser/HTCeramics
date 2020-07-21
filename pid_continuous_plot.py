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
            PID = minimalmodbus.Instrument('COM3',  1, mode='rtu') # CHANGE THIS COM PORT!!!!!!
            break
        except IOError:
            print('Failed to initialize, trying again.')
        except ValueError:
            print('Failed to initialize, trying again.')

    while True:
        try:
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
        temperatureSet = int(temperatureSet)
        plt.axhline(y = temperatureSet)

    PID.write_register(4097, temperatureSet, 1)

while True:
    if keyboard.is_pressed("right shift"):
        print("Shutting down")
        exit()
    else:
        plotData(temperatureSet)
