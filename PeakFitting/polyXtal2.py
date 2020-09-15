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

def generateModel(spec):
    compositeModel = None
    params = None
    x = spec['x']
    y = spec['y']
    x_min = np.min(x)
    x_max = np.max(x)
    x_range = x_max - x_min
    y_max = np.max(y)
    
    for i, basis_func in enumerate(spec['model']):
        prefix = f'm{i}_'
        model = getattr(models, basis_func['type'])(prefix = prefix)
        if basis_func['type'] in ['GaussianModel', 'Lorentzian Model', 'VoigtModel']:
            model.set_param_hint('sigma', min = 1e-6, max = x_range)
            model.set_param_hint('center', min = x_min, max = x_max)
            model.set_param_hint('height', min = 1e-6, max = 1.1*y_max)
            model.set_param_hint('amplitude', min = 1e-6)
            default_params = {prefix+'center':x_min + x_range*random.random(), prefix+'height': y_max*random.random(), prefix+'sigma': x_range*random.random()}
        else:
            raise NotImplemented(f'model {basis_func["type"]} not implemented')