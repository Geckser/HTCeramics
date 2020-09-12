#Simple script for plotting XRD data for testing
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('xrdData/915aluminumNum.csv')
twoTheta = df["Angle"]
intensity = df["Intensity"]

plt.plot(twoTheta, intensity, label = 'Curve')
plt.xlabel("Two Theta")
plt.ylabel("Intensity")
plt.legend()
plt.show()
