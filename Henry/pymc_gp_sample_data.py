# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 17:32:14 2020

@author: henry
"""


import matplotlib.pyplot as plt

import numpy as np
import scipy as sp

import pymc3 as pm
import theano.tensor as tt



class Sqr_root(pm.gp.mean.Mean):
    '''
    Custom mean square root class
    '''
    def __init__(self, c=0):
        self.c = c

    def __call__(self, X):
        return tt.alloc(1.0, X.shape[0]) * tt.sqrt(self.c)  

data = np.genfromtxt('gyro_fake_data_v0.csv', delimiter=',', skip_header=1)

X = data[:, 1] # age(Gyr)
y = data[:, 2] # rotation(Days)

X_pred = np.linspace(min(X)-0.5, max(X)+0.5, num=200)

#### CREATE MODEL ####
with pm.Model() as model:
    
    l = pm.Uniform('l', 0, 10) # chosing lengths and sigma over a uniform range
    sigma = pm.Uniform('sigma', 0, 10)
    
    mean = Sqr_root((y/X).mean())
    K = sigma**2 * pm.gp.cov.ExpQuad(1, l) # Exp squared covariance function (the 1 means 1 input dim)

   # gp = pm.gp.MarginalSparse(cov_func=K, mean_func=mean, approx='FITC')
    gp = pm.gp.Marginal(cov_func=K, mean_func=mean)
    
  #  Xu = pm.gp.util.kmeans_inducing_points(10, X.reshape(-1,1))

    sigma_2 = pm.HalfCauchy("sigma_2", beta=5)
    obs = gp.marginal_likelihood("obs", X=X.reshape(-1,1), y=y, noise=sigma_2)

    mp = pm.find_MAP()
######################    
    

#### TRAIN MODEL ####
with model:
  f_pred = gp.conditional('f_pred', X_pred.reshape(-1,1), pred_noise=False) # predict function
  pred_samples = pm.sample_posterior_predictive([mp], vars=[f_pred], samples=1000) # predicts samples data points?
  
######################  




##### PLOT DATA #####    
fig = plt.figure(figsize=(12,8)); ax = fig.gca()
from pymc3.gp.util import plot_gp_dist

#mu, var = gp.predict(X_pred, point=mp, diag=True)
#sd = np.sqrt(var)


plot_gp_dist(ax, pred_samples["f_pred"], X_pred)

plt.plot(X_pred, pred_samples["f_pred"][800, :].T, "co", ms=2, label="Predicted data");
#plt.fill_between(X_pred.flatten(), mu - 2*sd, mu + 2*sd, color="r", alpha=0.5)

plt.plot(X, y, 'ok', ms=3, alpha=0.5, label="Observed data")


plt.axvspan(min(X), max(X), alpha=0.3, color='red', label='Data')
plt.axvspan(0, min(X), alpha=0.1, color='blue', linestyle='--')
plt.axvspan(max(X), 7, alpha = 0.1, color='blue', label='No Data', linestyle='--')

plt.xlim(0,7)

# axis labels and title
plt.xlabel("age(Gyr)")
plt.ylabel("rotation(Days)")
plt.title("Posterior distribution over $f(x)$ at the observed values"); plt.legend()
######################  