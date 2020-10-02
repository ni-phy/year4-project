#Attempt2: Model the same data using sklearn
import numpy as np
import matplotlib.pyplot as plt
import sklearn as sk
from sklearn import gaussian_process as gp
from sklearn.gaussian_process.kernels import RBF

def sinusoid(x):
  return np.sin( np.pi * x)

def generate_1d_data(x, num_training_points, observation_noise_variance):

  observations_ = (sinusoid(x) +
                   np.random.normal(loc=0,
                                    scale=np.sqrt(observation_noise_variance),
                                    size=(num_training_points)))
  return observations_

# Generate training data with a known noise level (we'll later try to recover
# this value from the data).

num = 100
x = np.atleast_2d(np.linspace(0, 2, num=num)).T
observations_ = generate_1d_data(x, num, 0.1)
kernel = 2 * RBF(4.0)
gpf = gp.GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)

gpf.fit(x, observations_)
x_re = np.atleast_2d(np.linspace(2,4, num=num)).T
pred, std = gpf.predict(x_re, return_std=True)
#plt.figure()
x_plot = np.linspace(0, 4)
plt.plot(x_re, sinusoid(x_re), 'r:', label=r'$f(x) = x\,\sin(x)$')
plt.plot(x, observations_, 'r.', label='Observations')
plt.plot(x_re, pred, 'b-', label='Prediction')
plt.fill(np.concatenate([x_re, x_re[::-1]]),
         np.concatenate([pred - 1.9600 * std,
                        (pred + 1.9600 * std)[::-1]]),
         alpha=.5, fc='grey', ec='None', label='95% confidence interval')
plt.xlabel('$x$')
plt.ylabel('$f(x)$')
#plt.legend(loc='upper left')
plt.show()
#Std is too large