import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#from scipy.optimize import leastsq

df = pd.read_csv('singleXtalnum.csv') #read the csv file
twoTheta = df["Angle"] #assigns angle column
intensity = df["Intensity"] #assigns intensity column 

maxIntensity = intensity.max() #finds the value of the max intensity
peakLocation = twoTheta[intensity.idxmax()] #finds the 2-theta value of the maximum

derivativeIntensity = intensity.diff() #finds the rate of change of intensity, hopefully we can use this to find a good range for sigma
print(derivativeIntensity[5851:5880]) #roughly where the peaks is

sigma = 0.01 #placeholder value, need to figure out how to find sigma over a smaller range

FWHM = 2*sigma*np.sqrt(2*np.log(2)) #calcualtes the full width at half maximum using standard deviation
peak_move = twoTheta - peakLocation #shifts the peak to the maximum
G = maxIntensity*np.e**(-4*np.log(2)*((peak_move/FWHM)**2)) #calculates gaussian curve based on dataframe

#plots everything
plt.plot(twoTheta, intensity, label = 'Single Crystal Si')
plt.plot(twoTheta, G, label = 'Gaussian')
plt.plot(twoTheta, derivativeIntensity, label = 'Rate of Change')
plt.xlabel("Two Theta")
plt.ylabel("Intensity")
plt.legend()
plt.show()


