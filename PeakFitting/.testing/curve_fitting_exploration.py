import pandas as pd
import numpy as np
from lmfit.models import GaussianModel
import matplotlib.pyplot as plt
from sklearn.kernel_ridge import KernelRidge
from sklearn.decomposition import KernelPCA


data = pd.read_csv('../xrdData/915glassNum.csv')
angle = np.array(data['Angle'])
intensity = np.array(data['Intensity'])
angle = np.reshape(angle, (-1, 1))
intensity = np.reshape(intensity, (-1, 1))


transformer = KernelPCA(kernel='rbf')
angle, intensity = transformer.fit_transform(angle, intensity)

plt.scatter(angle, intensity)
plt.title("pca")
plt.show()
# print(np.argmax(intensity))
# print(intensity[1006])
# print(angle[1006])
#
# model = KernelRidge(kernel='rbf')
# model.fit(angle, intensity)
#
# predict = model.predict(angle)
# plt.plot(angle, predict)
# plt.show()
