import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gpflow
import tensorflow_probability as tfp
import tensorflow as tf
from gpflow.utilities import print_summary, set_trainable, to_default_float

data = np.array(pd.read_csv('/home/nikolas/Documents/Project/gyro_fake_data_v0.csv'))
Y = data[:,1].reshape(-1,1) #=age(GYr)
X = data[:,2].reshape(-1,1) #=rotation period (days)

k = gpflow.kernels.Matern52(1, lengthscales=0.3) + gpflow.kernels.Linear()
#m = gpflow.models.gpr.GPR(X, Y, kernel=k)
meanf = gpflow.mean_functions.Linear()
m = gpflow.models.GPR((X, Y), kernel=gpflow.kernels.Matern32(variance=2.5, lengthscales=8) + gpflow.kernels.Linear(), mean_function=meanf)

xx = np.linspace(np.min(X), np.max(X)+np.average(X)/2, 100).reshape(100,1)#[:,None]
tf.random.set_seed(1)
mean, var = m.predict_f(xx)
mean, var = m.predict_f(xx)
plt.figure(figsize=(12, 6))
plt.plot(X, Y, 'kx', mew=2)
plt.plot(xx, mean, 'b', lw=2)
plt.fill_between(xx[:,0], mean[:,0] - 2*np.sqrt(var[:,0]), mean[:,0] + 2*np.sqrt(var[:,0]), color='blue', alpha=0.2)
plt.show()