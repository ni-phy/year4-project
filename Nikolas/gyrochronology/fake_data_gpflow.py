import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gpflow
import tensorflow_probability as tfp
from gpflow.utilities import print_summary, set_trainable, to_default_float

data = np.array(pd.read_csv('/home/nikolas/Documents/Project/gyro_fake_data_v0.csv'))
Y = data[:,1] #=age(GYr)
X = data[:,2] #=rotation period (days)

k = gpflow.kernels.Matern52(1, lengthscales=0.3) + gpflow.kernels.Linear()
#m = gpflow.models.gpr.GPR(X, Y, kernel=k)
meanf = gpflow.mean_functions.Linear()
m = gpflow.models.GPR((X, Y), kernel=gpflow.kernels.Matern32() + gpflow.kernels.Linear(), mean_function=meanf)
m.likelihood.variance = 0.1

xx = np.linspace(np.max(X), np.max(X)+np.average(X)/2)#[:,None]
mean, var = m.predict_f(xx, full_cov=True)
plt.figure(figsize=(12, 6))
plt.plot(X, Y, 'kx', mew=2)
plt.plot(xx, mean, 'b', lw=2)
plt.fill_between(xx[:,0], mean[:,0] - 2*np.sqrt(var[:,0]), mean[:,0] + 2*np.sqrt(var[:,0]), color='blue', alpha=0.2)
plt.show()