# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15k2UbUuqHzCvB0AqHPVjOoW6-a8Q4mge
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_probability as tfp
import gpflow
from gpflow.utilities import print_summary, set_trainable, to_default_float
from mpl_toolkits.mplot3d import Axes3D
from gpflow.ci_utils import ci_niter

data = np.array(pd.read_csv('gyro_fake_data_v1.csv'))

Y = Y_plot = data[::10,1].reshape(-1,1)
X1 = X1_plot = data[::10,3] #rotation
X2 = X2_plot = data[::10,2] #B_V

#np.random.seed(1991)
k = gpflow.kernels.Matern12(variance=10, lengthscales=[15, 1])
#meanf = [gpflow.mean_functions.Linear(), gpflow.mean_functions.Linear()]
X = np.dstack([X1, X2]).reshape(-1, 2)
model = gpflow.models.GPR(data=(X, Y), kernel=k, mean_function=gpflow.mean_functions.Zero())#gpflow.mean_functions.Product(meanf[0], meanf[1]))
opt = gpflow.optimizers.Scipy()
opt_logs = opt.minimize(model.training_loss, model.trainable_variables, options=dict(maxiter=100))

x1_mesh, x2_mesh = np.meshgrid(X1, X2)

resolution = len(Y)
X1_test = np.linspace( np.min(X1), np.max(X1), num=resolution )
X2_test = np.linspace( np.min(X2), np.max(X2), num=resolution )
X1_test, X2_test = np.meshgrid( X1_test, X2_test )
X_test = np.dstack([X1_test, X2_test]).reshape(resolution, resolution, 2)

print(X1_test.shape)

# predict training set
mean, var = model.predict_y( X_test )
mean1 = np.array(mean)
mean1 = np.squeeze(mean1)
mean = tf.squeeze(mean)

f64 = gpflow.utilities.to_default_float

for p in model.trainable_parameters:
  p.prior = tfp.distributions.Gamma(
      gpflow.utilities.to_default_float(1.0), gpflow.utilities.to_default_float(1.0)
  )

hmc_helper = gpflow.optimizers.SamplingHelper(
    model.log_posterior_density, model.trainable_parameters
)

hmc = tfp.mcmc.HamiltonianMonteCarlo(
    target_log_prob_fn=hmc_helper.target_log_prob_fn, num_leapfrog_steps=10, step_size=0.01
)
adaptive_hmc = tfp.mcmc.SimpleStepSizeAdaptation(
    hmc, num_adaptation_steps=10, target_accept_prob=f64(0.75), adaptation_rate=0.1
)

num_burnin_steps = ci_niter(300)
num_samples = ci_niter(500)

# Note that here we need model.trainable_parameters, not trainable_variables - only parameters can have priors!

hmc_helper = gpflow.optimizers.SamplingHelper(
     model.log_posterior_density, model.trainable_parameters)

hmc = tfp.mcmc.HamiltonianMonteCarlo(
    target_log_prob_fn=hmc_helper, num_leapfrog_steps=10, step_size=0.01
)
adaptive_hmc = tfp.mcmc.SimpleStepSizeAdaptation(
    hmc, num_adaptation_steps=10, target_accept_prob=0.75, adaptation_rate=0.1
)

num_results = int(10e3)
num_burnin_steps = int(1e3)

def run_chain_fn():
    return tfp.mcmc.sample_chain(
        num_results=num_samples,
        num_burnin_steps=num_burnin_steps,
        current_state=hmc_helper.current_state,
        kernel=adaptive_hmc,
        trace_fn=lambda _, pkr: pkr.inner_results.is_accepted,
    )


samples, traces = run_chain_fn()
parameter_samples = hmc_helper.convert_to_constrained_values(samples)

param_to_name = {param: name for name, param in gpflow.utilities.parameter_dict(model).items()}
sample_mean = []
sample_stddev = []
is_accepted = []

print(np.mean(np.array(samples[0][:]), axis=0))
i = 0
# for p in model.trainable_parameters:
#   p.assign(np.mean(np.array(samples[i][100:])))
#   i = i+1
model.kernel.lengthscales.assign(np.mean(np.array(samples[1][:]), axis=0))
model.kernel.variance.assign(np.mean(np.array(samples[1][:])))
model.likelihood.variance.assign(np.mean(np.array(samples[2][:])))
#assigning lengthscales doesn't seem to work
print(model.trainable_parameters)

#Testing quality of results

numElems = len(Y)
idx = np.round(np.linspace(0, len(mean1.reshape(numElems**2)) - 1, numElems)).astype(int)
# Picks equal spaced elements from (longer) prediction array so that its shape of data

mu_test = (mean1.reshape(numElems**2)[idx])
sd_test = (np.array(var).reshape(numElems**2)[idx]) 

vals = np.sort([mu_test, sd_test], axis=1)

plt.figure(figsize=(18,9))
plt.errorbar(Y, vals[0,:], yerr=vals[1,:]**2, fmt='bo')
plt.plot(np.linspace( np.min(Y), np.max(Y), num=resolution ), np.linspace( np.min(Y), np.max(Y), num=resolution ), 'r')
plt.show()

Z = (np.sort(data[::2,1])-vals[0,:])/vals[1,:]
print(Y.shape)
import seaborn as sns
plt.hist(Z, density=True, bins=8)
sns.distplot(np.random.normal(size=1000), hist=False)
plt.show()