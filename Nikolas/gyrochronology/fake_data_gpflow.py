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

meanf = gpflow.mean_functions.Linear()

k = gpflow.kernels.Matern32() + gpflow.kernels.Linear()
def likel(y1, A):
    return -0.5 * (np.dot(y1.T, np.linalg.inv(A)).dot(y1) + np.log(np.linalg.det(A)) + 1*np.log(2 * np.pi))

le = int(X.shape[0])
theta = [1.0, 1.0]
y_1 = np.random.multivariate_normal(np.zeros(le), k(X, X))
ls = np.linspace(0.01,2,le)
sigmas = np.linspace(0.1,5.0,le)
L = np.zeros([le, le])
for i in range(0, le):
    for j in range(0, le):
        k = gpflow.kernels.Matern32(variance=sigmas[j], lengthscales=ls[i])
        A = k(X, X)
        L[i,j] = likel(Y, A)

indx = np.where(L == np.amax(L))
opt_ls = ls[indx[0]]
opt_s = sigmas[indx[1]]

k = gpflow.kernels.Matern32(variance=opt_ls, lengthscales=opt_s)
m = gpflow.models.GPR((X, Y), kernel=gpflow.kernels.Matern32(variance=2.5, lengthscales=8) + gpflow.kernels.Linear(), mean_function=meanf)

xx = np.linspace(np.min(X), np.max(X)+np.average(X)/2, 100).reshape(100,1)#[:,None]
tf.random.set_seed(1)
mean, var = m.predict_f(xx)#, full_cov=True)
plt.figure(figsize=(12, 6))
plt.plot(X, Y, 'kx', mew=2)
plt.plot(xx, mean, 'b', lw=2)
plt.fill_between(xx[:,0], mean[:,0] - 2*np.sqrt(var[:,0]), mean[:,0] + 2*np.sqrt(var[:,0]), color='blue', alpha=0.2)
plt.show()