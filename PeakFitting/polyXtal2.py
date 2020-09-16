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


spec = {'x':twoTheta.index.values, 'y':intensity, 'model':[
    {'type': 'GaussianModel'}, 
    {'type': 'GaussianModel'}, 
    {'type': 'GaussianModel'}, 
    {'type': 'GaussianModel'},
    {'type': 'GaussianModel'},
    {'type': 'GaussianModel'}
    ]}


peaks_found = updateSpecFromPeaks(spec, [0, 1, 2, 3, 4, 5], peak_widths=(250,300))
fig, ax = plt.subplots()
ax.scatter(spec['x'], spec['y'], s=4)
for i in peaks_found:
    ax.axvline(x=spec['x'][i], c='black', linestyle='dotted')


model, params = generateModel(spec)
output = model.fit(spec['y'], params, x=spec['x'])
fig, gridspec = output.plot(data_kws={'markersize':  1})

plt.show()