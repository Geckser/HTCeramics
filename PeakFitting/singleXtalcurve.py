import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from lmfit.models import GaussianModel
from lmfit.models import LorentzianModel
from lmfit.models import VoigtModel
#from scipy.optimize import leastsq

df = pd.read_csv('singleXtalnum.csv') #read the csv file
twoTheta = df["Angle"] #assigns angle column
intensity = df["Intensity"] #assigns intensity column 

maxIntensity = intensity.max() #finds the value of the max intensity
peakLocation = twoTheta[intensity.idxmax()] #finds the 2-theta value of the maximum
derivativeIntensity = intensity.diff() #finds the rate of change of intensity, hopefully we can use this to find a good range for sigma

for i in range(0, len(derivativeIntensity)): #finds where the spike begins
    if derivativeIntensity[i] >= 100: #this number might be specific to the curve, probably need a more universal way of finding it
        curveStart = i
        break


for j in range(intensity.idxmax()+1, len(derivativeIntensity)): #finds where the curve starts sloping up again. plus one is needed because .diff has one less index
    if derivativeIntensity[j] > 0:
        curveEnd = j
        break

peakArea = pd.DataFrame({'Angle': twoTheta[curveStart:curveEnd], 'Intensity': intensity[curveStart:curveEnd]}) #limits the area of the data around the curve for more consistent matching
peakArea = peakArea.reset_index() #resets index so the fitting works 
boundTwoTheta = peakArea["Angle"]
boundIntensity = peakArea["Intensity"]
#print(peakArea)



x = boundTwoTheta #for some reason the fit only works if the data is assigned like this
y = boundIntensity

mod = LorentzianModel() 

pars = mod.guess(y, x = x) #does the gaussian fit
out = mod.fit(y, pars, x = x)
print(out.fit_report(min_correl=0.25))
fittingParams = out.params
#print(fittingParams[sigma])


""" This is an attempt to get sigma from the fitting curve. WIP
print()
file = open('fittingParams.txt' , 'w')
file.write(str(out.params))
file.close()
"""

#plots everything
plt.plot(twoTheta, intensity, label = 'Single Crystal Si')
#plt.plot(twoTheta, G, label = 'Gaussian')
plt.plot(boundTwoTheta, out.best_fit, label = 'Fitted Curve')
#plt.plot(twoTheta, derivativeIntensity, label = 'Rate of Change')
plt.xlabel("Two Theta")
plt.ylabel("Intensity")
plt.legend()
plt.show()


""" lmfit does a better job at fitting, this is here for legacy sake
sigma = 0.0268 #probably better to pull sigma from the fit
#print(sigma)

FWHM = 2*sigma*np.sqrt(2*np.log(2)) #calcualtes the full width at half maximum using standard deviation
peak_move = twoTheta - peakLocation #shifts the peak to the maximum
G = maxIntensity*np.e**(-4*np.log(2)*((peak_move/FWHM)**2)) #calculates gaussian curve based on dataframe
"""

""" This is an attempt to get sigma from the fitting curve. WIP. Also here for legacy sake. 
print()
file = open('fittingParams.txt' , 'w')
file.write(str(out.params))
file.close()
"""