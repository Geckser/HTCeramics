import minimalmodbus
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
count = 0
def readTemp():# this function reads the temperature
    while True:#this loop ensures the hardware is connected
        try:
            PID = minimalmodbus.Instrument('COM3',1,mode='rtu') #Set port and communication mode
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
print("The temperature is ",readTemp() )

def init():
    ax.set_ylim(10,50)
    ax.set_xlim(0,10000)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)
    return line,

fig, ax = plt.subplots()
line = ax.plot([],[],lw=2)
ax.grid()
xdata, ydata = [], []

def run(data):
    t,y =data
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()

    if t >= xmax:
        ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()
        line.set_data(xdata,ydata)
        return line,
ani =animation.FuncAnimation(fig,run,readTemp,blit=False,interval=10000,repeat=False,init_func=init)

plt.show()