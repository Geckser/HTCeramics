import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#from scipy.optimize import leastsq

df = pd.read_csv('singleXtalnum.csv') #read the csv file
twoTheta = df["Angle"] #assigns angle column
intensity = df["Intensity"] #assigns intensity column 
maxIntensity = intensity.max() #finds the value of the max intensity
sigma = intensity.std() #find the standard deviation
#print(intensity[maxIntensity])




#def gaussian(sigma, peak, ):

plt.plot(twoTheta, intensity, label = 'Single Crystal Si')
plt.xlabel("Two Theta")
plt.ylabel("Intensity")
plt.legend()
plt.show()


