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

"""
#This function made by Chris Ostrouchov, https://chrisostrouchov.com/post/peak_fit_xrd_python/
def generateModel(spec):
    composite_model = None
    params = None
    x = spec['x']
    y = spec['y']
    x_min = np.min(x)
    x_max = np.max(x)
    x_range = x_max - x_min
    y_max = np.max(y)
    for i, basis_func in enumerate(spec['model']):
        prefix = f'm{i}_'
        model = getattr(models, basis_func['type'])(prefix=prefix)
        if basis_func['type'] in ['GaussianModel', 'LorentzianModel', 'VoigtModel', 'PseudoVoigtModel']: # for now VoigtModel has gamma constrained to sigma
            model.set_param_hint('sigma', min=1e-6, max=x_range)
            model.set_param_hint('center', min=x_min, max=x_max)
            model.set_param_hint('height', min=1e-6, max=1.1*y_max)
            model.set_param_hint('amplitude', min=1e-6)
            # default guess is horrible!! do not use guess()
            default_params = {
                prefix+'center': x_min + x_range * random.random(),
                prefix+'height': y_max * random.random(),
                prefix+'sigma': x_range * random.random()
            }
        else:
            raise NotImplemented(f'model {basis_func["type"]} not implemented yet')
        if 'help' in basis_func:  # allow override of settings in parameter
            for param, options in basis_func['help'].items():
                model.set_param_hint(param, **options)
        model_params = model.make_params(**default_params, **basis_func.get('params', {}))
        if params is None:
            params = model_params
        else:
            params.update(model_params)
        if composite_model is None:
            composite_model = model
        else:
            composite_model = composite_model + model
    return composite_model, params
"""

def createModel(spec, params):
    x = spec['x']
    y = spec['y']
    params = params
    print(params) 
    center = params['center']
    height = params['height']
    sigma = params['sigma']

    gauss1 = models.GaussianModel(prefix='g1_')
    pars = gauss1.make_params()
    pars.update(gauss1.make_params())
    pars['g1_center'].set(value = center[0])
    pars['g1_sigma'].set(value = sigma[0])
    pars['g1_amplitude'].set(value = height[0])

    gauss2 = models.GaussianModel(prefix='g2_')
    pars.update(gauss2.make_params())
    pars['g2_center'].set(value = center[1])
    pars['g2_sigma'].set(value = sigma[1])
    pars['g2_amplitude'].set(value = height[1])

    gauss3 = models.GaussianModel(prefix='g3_')
    pars.update(gauss3.make_params())
    pars['g3_center'].set(value = center[2])
    pars['g3_sigma'].set(value = sigma[2])
    pars['g3_amplitude'].set(value = height[2])

    gauss4 = models.GaussianModel(prefix='g4_')
    pars.update(gauss4.make_params())
    pars['g4_center'].set(value = center[3])
    pars['g4_sigma'].set(value = sigma[3])
    pars['g4_amplitude'].set(value = height[3])

    gauss5 = models.GaussianModel(prefix='g5_')
    pars.update(gauss5.make_params())
    pars['g5_center'].set(value = center[4])
    pars['g5_sigma'].set(value = sigma[4])
    pars['g5_amplitude'].set(value = height[4])

    gauss6 = models.GaussianModel(prefix='g6_')
    pars.update(gauss6.make_params())
    pars['g6_center'].set(value = center[5])
    pars['g6_sigma'].set(value = sigma[5])
    pars['g6_amplitude'].set(value = height[5])

    mod = gauss1 + gauss2 + gauss3 + gauss4 + gauss5 + gauss6
    return mod, pars

def peakFinder(spec, endLastPeak): #finds and counts peaks
    y = spec['y']
    baseIntensity = 2*y.mean() #checks for a baseline, probabily have to set manually for each dataset since it is so dependent on the data set
    dy = y.diff()
    #print(len(y)-endLastPeak)
    peakStart = -1
    for i in range(endLastPeak, len(y)): #finds where a peak starts
        if y[i] >= baseIntensity and y[i+1] >= baseIntensity and y[i+2] >= baseIntensity:
            peakStart = i
            break

    if peakStart == -1:
        return     
    
    for j in range(peakStart, len(dy)): #finds max peaks
        if  dy[j] <= 0:
            if dy[j+1] <= 0 and dy[j+2] <= 0 and dy[j+3] <= 0:
                peakMax = j
                break
            else:
                pass

    for k in range(peakMax, len(y)): #finds the end of the peak
        if y[k] < baseIntensity and y[k+1] < baseIntensity and y[k+2] < baseIntensity:
            peakEnd = k
            break
    
    #print(peakStart, peakMax, peakEnd)
    return peakStart, peakMax, peakEnd
                
def multiPeakFinder(spec): #runs peak finder for all the peaks
    x = spec['x']
    y = spec['y']
    xMin = int(x.min())
    xMax = int(x.max())
    position = xMin
    peakData = []
    for h in range(xMin, xMax):
        peak = peakFinder(spec, position)
        if not peak:
            break
        position = peak[2]
        peakData.append(peak)
        #print(len(peakData), peakData)
    
    peakDataDF = pd.DataFrame(peakData, columns = ['Start', 'Max', 'End'])
    return peakDataDF

def updateParams(spec): #updates limit from data found in multiPeakFinder
    x = spec['x']
    y = spec['y']
    x_range = np.max(x) - np.min(x)
    peakData = multiPeakFinder(spec)
    peak_indicies = peakData['Max']
    peak_widths = peakData['End'] - peakData['Start']
    model_indicies = range(0, len(peak_indicies))
    totalParams = []
    for peak_indicie, model_indicie in zip(peak_indicies.tolist(), model_indicies): #This block is by by Chris Ostrouchov, https://chrisostrouchov.com/post/peak_fit_xrd_python/
        model = spec['model'][model_indicie]
        if model['type'] in ['GaussianModel', 'LorentzianModel', 'VoigtModel', 'PseudoVoigtModel']:
            params = {
                'height': y[peak_indicie],
                'sigma': x_range / len(x) * np.min(peak_widths),
                'center': x[peak_indicie]
            }
            totalParams.append(params)
        else:
            raise NotImplemented(f'model {basis_func["type"]} not implemented yet')
    totalParams = pd.DataFrame(totalParams)
    return peak_indicies, totalParams
    
    
defaultspec = {'x':twoTheta, 'y':intensity, 'model':[
    {'type': 'GaussianModel'}, 
    {'type': 'GaussianModel'},
    {'type': 'GaussianModel'},
    {'type': 'GaussianModel'},
    {'type': 'GaussianModel'},
    {'type': 'GaussianModel'},
    ]}

spec = defaultspec

foundPeaks, params = updateParams(spec)
mod, pars = createModel(spec, params)

x = twoTheta
y = intensity
out = mod.fit(y, pars, x= x)
out.plot(data_kws={'markersize':  1})
#model, params = generateModel(spec)

#output = model.fit(spec['y'], params, x=spec['x'])
#print_best_values(spec, output)

#plotting stuff below here
"""
fig, ax = plt.subplots()
ax.scatter(spec['x'], spec['y'], s=4)
for i in foundPeaks:
    ax.axvline(x=spec['x'][i], c='black', linestyle='dotted')
"""
#output.plot(data_kws={'markersize':  1})

#ax.axhline(y = intensity.mean(), c='red', linestyle = 'dotted')
#ax.axhline(y = 5*intensity.mean(), c='red', linestyle = 'dotted')

#fig, gridspec = output.plot(data_kws={'markersize':  1})

plt.show()

"""
Legacy Code: 

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
"""
