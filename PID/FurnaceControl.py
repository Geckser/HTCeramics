# This is working code to set a target temperature on the PID when connected via USB. This program will then create a
# real time plot of Temp vs. Time with a line to mark the target temperature. Press RIGHT SHIFT to stop the code and
# i to change the target temp

# Throughout this code there is a command structure that looks like this: PID.write_register(4098, 999, 1). The first
# number indicates the command. It is a decimal number converted from hexidecimal. The hexidecimal code can be found in
# the manual for the PID controller. This code was written for the Omega CN7600, and shares instructions with CN7200,
# CN7500 and CN7800

import minimalmodbus
import time
import sys
import time
import matplotlib.pyplot as plt
import numpy as np
import keyboard
from matplotlib.offsetbox import AnchoredText
# Creates list to be edited later
tempList = []
timeList = []

temperatureSet = input("please enter a temperature setting: ")
startTime = time.time()
port = 'COM3' #Change this COM port
#Adds the chart
plt.figure()
plt.xlabel("Time")
plt.ylabel("Temperature")
plt.title("Temp vs. Time")

ac = fig.add_subplot() #adds top temperature box
ax = fig.add_subplot() #adds time box
aw = fig.add_subplot() #adds time box

print("DON'T FORGET TO SET YOUR COM PORT, if you need to set it, press c or edit the code")
print("Press i to change the target temperature and right shift in order to stop the code")


def plotData(temperatureSet):
    time.sleep(.25)
    while True:

        # This establishes connection with the PID. Sets max temp to 999 C. Sets min temp to 0 C. Turn on auto tune.
        try:
            PID = minimalmodbus.Instrument(port, 1, mode='rtu',
                                           close_port_after_each_call=True)  # CHANGE THIS COM PORT!!!!!!
            PID.write_register(4098, 999, 1) # Sets the maximum temperature (command,temp,number of decimals)
            PID.write_register(4099, 0, 1)# Sets the minimum temperature (command,temp,number of decimals)
            PID.write_bit(2067, 1, functioncode=5) # sets auto tune
            break

        # In cases where it does not fully establish communication with the PID these errors will be thrown and it will then proceed to try again.
        except IOError:
            print('Failed to initialize, trying again.')
        except ValueError:
            print('Failed to initialize, trying again.')

    while True:
        try:

            # Reestablish connection to PID
            PID = minimalmodbus.Instrument(port, 1, mode='rtu',
                                           close_port_after_each_call=True)  # CHANGE THIS COM PORT!!!!!!

            # This reads the temperature that the PID has measured.
            PIDTemperature = PID.read_register(4096, 1)

            # Plot the Temperature from the PID vs. Time using matplotlib.
            tempList.append(PIDTemperature) # updates the temperature
            runTime = time.time() - startTime
            timeList.append(runTime) #updates the time
            plt.plot(timeList, tempList, color='green')
            # Adds the temperature box
            at = AnchoredText(PIDTemperature, prop=dict(size=15), frameon=True, loc='upper left', )
            at.patch.set_boxstyle("round,pad=0.,rounding_size=.2")
            ac.add_artist(at)
            # Adds time box
            ar = AnchoredText(runTime, prop=dict(size=15), frameon=True, loc='upper right', )
            ar.patch.set_boxstyle("round,pad=0.,rounding_size=.2")
            ac.add_artist(ar)


            plt.pause(0.01)

        # Again, if these error are thrown due to poor communication between computer and PID we will continue to try again.
        except IOError:
            print("Failed to read, trying again")
        except ValueError:
            print("Failed to read, trying again")
        break

    # For cases where the user does not enter a temperature it will automatically be set to 15 C
    if temperatureSet == "none":
        temperatureSet = 15
        plt.axhline(y=temperatureSet)

    # This converts the new temperature reading to a float and creates a line on the plot to mark the desired temp
    else:
        temperatureSet = float(temperatureSet)
        plt.axhline(y=temperatureSet)
        #add target temperature box
        ak = AnchoredText(temperatureSet, prop=dict(size=15), frameon=True, loc='upper center', )
        ak.patch.set_boxstyle("round,pad=0.,rounding_size=.2")
        aw.add_artist(ak)

    try:

        # Reestablish connection to PID and set the target temp to "temperatureSet" as it was defined up above
        PID = minimalmodbus.Instrument(port, 1, mode='rtu',
                                       close_port_after_each_call=True)  # CHANGE THIS COM PORT!!!!!!
        PID.write_register(4097, temperatureSet, 1)

    except minimalmodbus.NoResponseError:
        plotData(temperatureSet)


while True:

    # Pressing RIGHT SHIFT will close down the program
    if keyboard.is_pressed("right shift"):
        PID = minimalmodbus.Instrument(port, 1, mode='rtu',
                                       close_port_after_each_call=True)  # CHANGE THIS COM PORT!!!!!!
        temperatureSet = 15
        PID.write_register(4097, temperatureSet, 1)
        print("Shutting down")
        exit()

    # Pressing i will allow you to change the target temp
    if keyboard.is_pressed("i"):
        temperatureSet = input("New temp setting: ")
        plotData(temperatureSet)
    if keyboard.is_pressed("c"):
        port = input("Enter your COM port in the format 'COM3', do not forget quotes. If you are using a Mac, first, why? Second enter in appropriate format. ")
        plotData(temperatureSet)
    else:
        plotData(temperatureSet)
