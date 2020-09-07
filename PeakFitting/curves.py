import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-5,5,100) #sets an array from -5 to 5 with steps of 1/100
L = 1/(1+x**2) #Lorentzian plot standardized to a max value of 1
G = np.e**(-1*(np.log(2)*x**2)) #Gaussian curve standardized the same way as the Lorentzian
V = L + G

fig, ax = plt.subplots() #creates a figure with 2 axis
ax.plot(x, L, label = 'Lorentzian' ) #plots Lorentzian curve
ax.plot(x, G, label = 'Gaussian') #plots Gaussian
#ax.plot(x, V, label = 'Pseudo-Voigt')
ax.set_title('Curve Types') #title
ax.legend() #adds a legend
plt.show() #shows plot