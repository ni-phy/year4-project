import numpy as np
import matplotlib.pyplot as plt
import sklearn as sk
from sklearn import gaussian_process as gp
from sklearn.gaussian_process.kernels import RBF, WhiteKernel
import pandas as pd

# Generate training data with a known noise level (we'll later try to recover
# this value from the data).

data = np.array(pd.read_csv("gyro_fake_data.csv"))
age = data[:,1]
rotatoin_unc = data[:,3]
observations_ =data[:,2]

x = np.atleast_2d(observations_[:70]).T

kernel = 2*RBF(length_scale=10.0) +WhiteKernel(noise_level=1.0)
gpf = gp.GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=20, normalize_y= True)

#First Prediction for existing range
gpf.fit(x, age[:70])
x_re = np.atleast_2d(observations_[70:]).T
pred, std = gpf.predict(x_re, return_std=True)

#Plot
plt.scatter(observations_, age, c='r', label='Observations')
plt.errorbar(x_re, pred, yerr=std*1.9600, fmt='bo', label='Prediction with 95% confidence interval')
plt.legend(loc='upper left')
plt.show()

#Second Prediction for non-existing range
x_re2 = np.linspace(np.max(observations_), np.max(observations_)+np.average(observations_))
x_re2 = np.atleast_2d([x_re2]).T
pred2, std2 = gpf.predict(x_re2, return_std=True)

#Plot
plt.scatter(observations_, age, c='r', label='Observations')
plt.errorbar(x_re2, pred2, yerr=std2*1.9600, fmt='bo', label='Prediction with 95% confidence interval')
plt.legend(loc='upper left')
plt.show()

#This does not work, sklearn does not let us define a mean function

'''
#plt.errorbar(data[:,2], data[:,1], xerr = rotatoin_unc, fmt='r.', label='Observations')
plt.plot(x_re, pred, 'bo', label='Prediction')
plt.scatter(x_re, pred - std * 1.9600)
plt.scatter(x_re, pred + std * 1.9600)
plt.fill_between(observations_[70:], pred - std*1.9600, pred + std*1.9600, alpha=0.8)#, c='lightgray')
#plt.fill(x_re[3], pred[3], alpha=1, fc='lightgray', label='95% confidence interval') #this fixes labelling issues with plt.fill

plt.ylabel('Age (Gyr)')
plt.xlabel('Rotation (Days)')
plt.legend(loc='upper left')
plt.show()'''