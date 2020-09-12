#Simple script for plotting XRD data for testing
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plotChooser():
    print("[1] Load new file\n[2] Load Default")
    choice = int(input("Input Choice: "))
    if choice == 1: #good for loading a file once
        dataFile = input('Enter name of file: ')
        dataFile = str(dataFile)
    elif choice == 2: #if a file needs to be loaded repeatedly, put it here
        dataFile = 'polyxtal.csv'
    else:
        print("Invalid Choice")
    return dataFile

csvFile = plotChooser()
filePath = "xrdData/" + csvFile
print(filePath)

df = pd.read_csv(filePath)
twoTheta = df["Angle"]
intensity = df["Intensity"]

plt.plot(twoTheta, intensity, label = 'Curve')
plt.xlabel("Two Theta")
plt.ylabel("Intensity")
plt.legend()
plt.show()
