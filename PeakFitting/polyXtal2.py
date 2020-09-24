import os
import math
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize, signal
from lmfit import models

df = pd.read_csv('xrdData/polyxtal.csv') #read the csv file
twoTheta = df["Angle"] #assigns angle column
intensity = df["Intensity"] #assigns intensity column 

#This function made by Chris Ostrouchov, https://chrisostrouchov.com/post/peak_fit_xrd_python/
def generateModel(spec):
    compositeModel = None
    params = None
    x = spec['x']
    y = spec['y']
    x_min = np.min(x)
    x_max = np.max(x)
    x_range = x_max - x_min
    y_max = np.max(y)
    
    for i, basis_func in enumerate(spec['model']): #builds the models around the scattered data
        prefix = f'm{i}_'
        model = getattr(models, basis_func['type'])(prefix = prefix)
        if basis_func['type'] in ['GaussianModel', 'Lorentzian Model', 'VoigtModel']:
            model.set_param_hint('sigma', min = 1e-6, max = x_range)
            model.set_param_hint('center', min = x_min, max = x_max)
            model.set_param_hint('height', min = 1e-6, max = 1.1*y_max)
            model.set_param_hint('amplitude', min = 1e-6)
            default_params = {prefix+'center':x_min + x_range*random.random(), prefix+'height': y_max*random.random(), prefix+'sigma': x_range*random.random()}
        else:
            raise NotImplemented(f'model {basis_func["type"]} not implemented yet')
        if 'help' in basis_func:
            for param, option in basis_func['help'].items():
                model.set_param_hint(param, **option)
        model_params = model.make_params(**default_params, **basis_func.get('params', {}))
        if params is None:
            params = model_params
        else:
            params.update(model_params)
        if compositeModel is None:
            compositeModel = model
        else:
            compositeModel = compositeModel + model
    return compositeModel, params


#Funtion by Chris Ostrouchov, https://chrisostrouchov.com/post/peak_fit_xrd_python/, guesses using find_peaks_cwt
def updateSpecFromPeaks(spec, model_indicies, peak_widths=(10, 25), **kwargs): #guesses where the peaks are 
    x = spec['x']
    y = spec['y']
    x_range = np.max(x) - np.min(x)
    peak_indicies = signal.find_peaks_cwt(y, peak_widths)
    np.random.shuffle(peak_indicies)
    for peak_indicie, model_indicie in zip(peak_indicies.tolist(), model_indicies):
        model = spec['model'][model_indicie]
        if model['type'] in ['GaussianModel', 'LorentzianModel', 'VoigtModel']:
            params = {
                'height': y[peak_indicie],
                'sigma': x_range / len(x) * np.min(peak_widths),
                'center': x[peak_indicie]
            }
            if 'params' in model:
                model.update(params)
            else:
                model['params'] = params
        else:
            raise NotImplemented(f'model {basis_func["type"]} not implemented yet')
    return peak_indicies

def peakFinder(spec, endLastPeak): #finds and counts peaks, WIP can find first peak
    y = spec['y']
    baseIntensity = 10*y.mean() #checks for a baseline
    dy = y.diff()
    for i in range(endLastPeak, len(y)): #finds where a peak starts
        if y[i] >= baseIntensity:
            peakStart = i
            break
        
    for j in range(peakStart, len(dy)): #finds max peaks
        if  dy[j] <= 0:
            if dy[j+1] <= 0 and dy[j+2] <= 0 and dy[j+3] <= 0:
                peakMax = j
                break
            else:
                pass

    for k in range(peakMax, len(y)): #finds the end of the peak
        if y[k] < baseIntensity:
            peakEnd = k
            break
    
    #print(peakStart, peakMax, peakEnd)
    return peakStart, peakMax, peakEnd
                
def multiPeakFinder(spec): #runs peak finder for all the peaks
    x = spec['x']
    xMin = int(x.min())
    xMax = int(x.max())
    position = xMin
    peakData = []
    for i in range(xMin, xMax):
        peak = peakFinder(spec, position)
        position = peak[2]
        peakData.append(peak)
        print(len(peakData))
    return peakData

 
    

spec = {'x':twoTheta, 'y':intensity, 'model':[
    {'type': 'GaussianModel'}, 
    {'type': 'GaussianModel'}, 
    {'type': 'GaussianModel'}, 
    {'type': 'GaussianModel'},
    {'type': 'GaussianModel'},
    {'type': 'GaussianModel'}
    ]}

foundPeaks = multiPeakFinder(spec)
print(len(foundPeaks))

peaks_found = updateSpecFromPeaks(spec, [0, 1, 2, 3, 4, 5], peak_widths=(250,300))
fig, ax = plt.subplots()
ax.scatter(spec['x'], spec['y'], s=4)
for i in peaks_found:
    ax.axvline(x=spec['x'][i], c='black', linestyle='dotted')
 
#ax.axvline(x=spec['x'][foundPeaks[1]], c='red', linestyle='dotted')

model, params = generateModel(spec)
output = model.fit(spec['y'], params, x=spec['x'])
fig, gridspec = output.plot(data_kws={'markersize':  1})

plt.show()