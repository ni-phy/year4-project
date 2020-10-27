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

sparse = False
map = True


class Sqr_root(pm.gp.mean.Mean):
    '''Custom mean func of sqr root'''
    def __init__(self, coeffs=0, intercept=0):
        pm.gp.mean.Mean.__init__(self)
        self.b = intercept
        self.A = coeffs

    def __call__(self, X):
        return tt.squeeze(tt.dot(X**0.5, self.A) + self.b)

data = np.genfromtxt('gyro_fake_data_v0.csv', delimiter=',', skip_header=1)

X = data[:, 1].T
y = data[:, 2].T


with pm.Model() as model:
    

    l = pm.Normal('l', mu = 12, sigma=5)

    sigma = pm.HalfCauchy('sigma', beta=5)
    # range of values of sigma needs to cover all data. 15 - 30 days 
    # set as a guassian with a mean of 20 with a sd of 7.5


    mean = Sqr_root((y/X).mean()) # This is where I have the best success
    K = sigma**2 * pm.gp.cov.ExpQuad(1, l)

    if sparse:

      gp = pm.gp.MarginalSparse(cov_func=K, mean_func=mean, approx='FITC')
    
      Xu = pm.gp.util.kmeans_inducing_points(10, X.reshape(-1,1))

      obs = gp.marginal_likelihood("obs", X=X.reshape(-1,1), y=y, Xu=Xu, noise=sigma)

    else:
      gp = pm.gp.Marginal(cov_func=K, mean_func=mean)
      obs = gp.marginal_likelihood("obs", X=X.reshape(-1,1), y=y, noise=sigma)

    if map:
        trace = [pm.find_MAP()]
######################    
    

X_pred = np.linspace(0, 13.4, num=600)[:,None]

with model:
  f_pred = gp.conditional('f_pred', X_pred.reshape(-1,1), pred_noise=True) # predict function
  pred_samples = pm.sample_posterior_predictive(trace, vars=[f_pred], samples=3000) # predicts 1000 data points?
  
######################  

mu, var = gp.predict(X_pred, point=trace, diag=True, pred_noise=False)


# do this like 1000 timea?
sd = np.sqrt(var)



##### PLOT DATA #####    
fig = plt.figure(figsize=(12,8)); ax = fig.gca()
#from pymc3.gp.util import plot_gp_dist

#plot_gp_dist(ax, pred_samples["f_pred"], X_pred)

#plt.plot(X_pred, pred_samples["f_pred"][500, :].T, "co", ms=2, label="Predicted data")

plt.plot(X_pred, mu, label='mean function')
plt.fill_between(X_pred.flatten(), mu - sd, mu + sd, color="r", alpha=0.5, label='1 std')

plt.plot(X, y, 'ok', ms=3, alpha=0.5, label="Observed data")


#plt.axvspan(min(X), max(X), alpha=0.3, color='red', label='Data region')

plt.xlim(0,13.4)

# axis labels and title
plt.xlabel("age(Gyr)")
plt.ylabel("rotation(Days)")
plt.title("Posterior distribution over $f(x)$ at the observed values"); plt.legend()

plt.savefig('2dgp.png')
files.download("2dgp.png") 

######################  
