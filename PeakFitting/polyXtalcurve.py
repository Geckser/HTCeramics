import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from lmfit.models import GaussianModel
from lmfit.models import LorentzianModel
from lmfit.models import PseudoVoigtModel

df = pd.read_csv('singleXtalnum.csv') #read the csv file
twoTheta = df["Angle"] #assigns angle column
intensity = df["Intensity"] #assigns intensity column 

maxIntensity = intensity.max() #finds the value of the max intensity
peakLocation = twoTheta[intensity.idxmax()] #finds the 2-theta value of the maximum
derivativeIntensity = intensity.diff() #finds the rate of change of intensity, hopefully we can use this to find a good range for sigma

def curveFinder(): #funtion to narrow down the area of the peak
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
    return boundTwoTheta, boundIntensity

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
