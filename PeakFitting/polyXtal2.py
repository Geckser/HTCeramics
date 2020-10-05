import os
import math
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lmfit import models
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

df = pd.read_csv('xrdData/915aluminumNum.csv') #read the csv file
twoTheta = df["Angle"] #assigns angle column
intensity = df["Intensity"] #assigns intensity column 

def createModel(spec, params):
    params = params
    modelType = pd.DataFrame(spec['model'])
    basis_func = modelType['type']
    peaks = params.index.values
    center = params['center']
    height = params['height']
    sigma = params['sigma']
    
    gaussi = models.GaussianModel(prefix = 'gi_') #uses an empty gaussian function to initialaize the paramaters
    pars = gaussi.make_params() #creates params dataset
    
    for i in peaks:
        if basis_func[i] == 'GaussianModel': #checks if the peak is gaussian
            prefix = 'g'+str(i)+'_'
            gauss = models.GaussianModel(prefix = prefix)
            pars.update(gauss.make_params())

            pars[prefix + 'center'].set(center[i])
            pars[prefix + 'sigma'].set(sigma[i])
            pars[prefix + 'amplitude'].set(height[i])
            if i == 0: #initiallizes the mod variable if it's the first model in the composite function
                mod = gauss
            else:
                mod = mod + gauss
                
        elif basis_func[i] == 'LorentzianModel':
            prefix = 'l'+str(i)+'_'
            lorentz = models.LorentzianModel(prefix = prefix)
            pars.update(lorentz.make_params())

            pars[prefix + 'center'].set(center[i])
            pars[prefix + 'sigma'].set(sigma[i])
            pars[prefix + 'amplitude'].set(height[i])
            if i == 0: #initiallizes the mod variable if it's the first model in the composite function
                mod = lorentz
            else:
                mod = mod + lorentz  

        elif basis_func[i] == 'PseudoVoigtModel':
            prefix = 'p'+str(i)+'_'
            pseudoV = models.PseudoVoigtModel(prefix = prefix)
            pars.update(pseudoV.make_params())

            pars[prefix + 'center'].set(center[i])
            pars[prefix + 'sigma'].set(sigma[i])
            pars[prefix + 'amplitude'].set(height[i])
            if i == 0: #initiallizes the mod variable if it's the first model in the composite function
                mod = pseudoV
            else:
                mod = mod + pseudoV
        
        else:
            print("Function not implemented")

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
        
    peakCount = len(peakData)
    peakDataDF = pd.DataFrame(peakData, columns = ['Start', 'Max', 'End'])
    return peakDataDF, peakCount

def updateParams(spec): #updates limit from data found in multiPeakFinder
    x = spec['x']
    y = spec['y']
    x_range = np.max(x) - np.min(x)
    peakData, peakCount = multiPeakFinder(spec)
    peak_indicies = peakData['Max']
    peak_widths = peakData['End'] - peakData['Start']
    model_indicies = range(0, peakCount)
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
            print("Function not implemeted")
    totalParams = pd.DataFrame(totalParams)
    return peak_indicies, totalParams

def specWriter():
    spec = {'x':twoTheta, 'y':intensity, 'model':[]}
    peakCount = multiPeakFinder(spec)
    modelList = spec['model']
    for peaks in range(0, peakCount[1]):
        modelList.append({'type':'GaussianModel'})

    return spec

def specWriter2(): #for UI
    spec = {'x':twoTheta, 'y':intensity, 'model':[]}
    peakCount = multiPeakFinder(spec)
    modelList = spec['model']
    for peaks in range(0, peakCount[1]):
        modelList.append({'type':'GaussianModel'})
        """ Finds each individual peak, broken
        print("Choose Model type for peak" + str(peaks) +"\n 1 Gaussian, 2 for Lorentzian, 3 for PseudoVoigt: ")
        modelType = input()
        if modelType == 1:
            modelList.append({'type':'GaussianModel'})
        elif modelType == 2:
            modelList.append({'type':'LorenztianModel'})
        elif modelType == 3:
            modelList.append({'type':'PseudoVoigtModel'})
        else:
            print('Invalid Choice')
        """   
    return spec

def dataPlotter(spec): #plots the data without a curve, used in UI
    fig = Figure(figsize = (5,5), dpi = 100)

    x = spec['x']
    y = spec['y']

    plot = fig.add_subplot(111)

    plot.scatter(x,y, s = 4)

    canvas = FigureCanvasTkAgg(fig, master = mainframe)
    canvas.draw()

    canvas.get_tk_widget().grid(column = 0, row = 0, stick = (N, W))

def fitCurve(spec, params): #fits the curve, BROKEN
    intensity = spec['y']
    twoTheta = spec['x']
    fig = Figure(figsize = (5,5), dpi = 100)
    mod, pars = createModel(spec, params)
    out = mod.fit(intensity, pars, x = twoTheta)
    out.plot(data_kws={'markersize':  1})

    canvas = FigureCanvasTkAgg(fig, master = mainframe)
    canvas.draw()

    canvas.get_tk_widget().grid(column = 0, row = 0, stick = (N, W))

def _quit(): #allows process to actually stop
    root.quit()
    root.destroy()

spec = specWriter()

foundPeaks, params = updateParams(spec)
#mod, pars = createModel(spec, params)

#out = mod.fit(intensity, pars, x= twoTheta)



#plotting stuff below here
#out.plot(data_kws={'markersize':  1})


#This plots where the peaks are. Useful for testing
"""
fig, ax = plt.subplots()
ax.scatter(spec['x'], spec['y'], s=4)
for i in foundPeaks:
    ax.axvline(x=spec['x'][i], c='black', linestyle='dotted')

ax.axhline(y = intensity.mean(), c='red', linestyle = 'dotted')
ax.axhline(y = 5*intensity.mean(), c='red', linestyle = 'dotted')
"""

#plt.show()


#UI stuff here

root = Tk()
root.title("Peak Data")
mainframe = ttk.Frame(root, padding = "3 3 12 12")
mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
ttk.Label(mainframe, text = params).grid(column = 0, row = 2, stick = (W,E))
ttk.Button(master = mainframe, command = dataPlotter(spec), text = 'Plot').grid(column = 1, row = 2, stick = (N))
#ttk.Button(master = mainframe, command = fitCurve(spec, params), text = 'Fit').grid(column =1, row =2, stick = (W))
ttk.Button(master = mainframe, command =_quit, text = 'Quit').grid(column = 1, row = 2, stick = (S))


root.mainloop()