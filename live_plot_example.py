import matplotlib.pyplot as plt
import numpy as np
import time

countList = [] # generate an empty list
dataList = [] # generate an empty list

plt.figure() # initialize a figure from matplotlib
plt.xlabel('Counts')
plt.ylabel('sin(counts / 5)')
plt.title('Cool title')

for i in range(0, 120, 1):
    countList.append(int(i)) # append the iterator i to countList
    dataList.append(np.sin(int(i) / 5)) # Make some data by appending the sine of the iterator to the dataList
    time.sleep(0.25) # wait for 0.25 second
    plt.plot(countList, dataList, color='green') # plot the data, make it green colored.
    plt.pause(0.01) # Pause the plot for 0.01 seconds
