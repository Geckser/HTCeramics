import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from lmfit.models import GaussianModel
from lmfit.models import LorentzianModel
from lmfit.models import PseudoVoigtModel

df = pd.read_csv('xrdData/polyxtal.csv') #read the csv file
twoTheta = df["Angle"] #assigns angle column
intensity = df["Intensity"] #assigns intensity column 

derivativeIntensity = intensity.diff() #finds the rate of change of intensity, hopefully we can use this to find a good range for sigma
print(intensity.mean())

def curveFinder(intensity): #funtion to narrow down the area of the peak
    for i in range(0, len(intensity)): #finds where the spike begins
        if intensity[i] >= 10*intensity.mean(): #this number might be specific to the curve, needs to be higher than the noise, using 10x the average for now
            curveStart = i
            break

    for j in range(curveStart + 1, len(derivativeIntensity)):
        if derivativeIntensity < 0:
            peakMax = j
            break

    for k in range(intensity.idxmax()+1, len(derivativeIntensity)): #finds where the curve starts sloping up again. plus one is needed because .diff has one less index
        if derivativeIntensity[k] > 0:
            curveEnd = k
            break
    
    peakArea = pd.DataFrame({'Angle': twoTheta[curveStart:curveEnd], 'Intensity': intensity[curveStart:curveEnd]}) #limits the area of the data around the curve for more consistent matching
    peakArea = peakArea.reset_index() #resets index so the fitting works 
    boundTwoTheta = peakArea["Angle"]
    boundIntensity = peakArea["Intensity"]
    #print(peakArea)
    return boundTwoTheta, boundIntensity, peakMax

def fittingGaussian(x, y): #fits a gaussian curve
    mod = GaussianModel() 
    pars = mod.guess(y, x = x) #does the gaussian fit
    out = mod.fit(y, pars, x = x)
    print(out.fit_report(min_correl=0.25))
    return out.best_fit

def fittingLoretzian(x, y): #fits a loretzian curve
    mod = LorentzianModel() 
    pars = mod.guess(y, x = x) 
    out = mod.fit(y, pars, x = x)
    print(out.fit_report(min_correl=0.25))
    return out.best_fit

def fittingPseudoVoigt(x, y): #fits a pseudovoigt curve
    mod = PseudoVoigtModel() 
    pars = mod.guess(y, x = x) 
    out = mod.fit(y, pars, x = x)
    print(out.fit_report(min_correl=0.25))
    return out.best_fit

boundedData = curveFinder(intensity)

x = boundedData[0] #for some reason the fit only works if the data is assigned like this
y = boundedData[1]

gaussianFit = fittingGaussian(x, y)
lorentzianFit = fittingLoretzian(x, y)
pseudoVoigtFit = fittingPseudoVoigt(x, y)

#plots everything
plt.plot(twoTheta, intensity, label = 'Single Crystal Si')
plt.plot(boundedData[0], gaussianFit, label = 'Gaussian Fitted Curve')
plt.plot(boundedData[0], lorentzianFit, label = 'Lorentzian Fitted Curve')
plt.plot(boundedData[0], pseudoVoigtFit, label = 'Pseudo-Voigt Fitted Curve')
plt.xlabel("Two Theta")
plt.ylabel("Intensity")
plt.legend()
plt.show()
