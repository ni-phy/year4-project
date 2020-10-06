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
                   np.random.normal(loc=x,
                                    scale=np.sqrt(observation_noise_variance)))#, size=(num_training_points)))
  return observations_

# Generate training data with a known noise level (we'll later try to recover
# this value from the data).

num = 100
x = np.atleast_2d(np.linspace(0, 1.5, num=num)).T
x_more = np.atleast_2d(np.linspace(2.2, 3, num=num)).T
x = np.concatenate((x, x_more))
observations_ = generate_1d_data(x, num, 0.1)
kernel = 2*RBF(1.0)
gpf = gp.GaussianProcessRegressor(kernel=None, n_restarts_optimizer=30)

gpf.fit(x, observations_)
x_re = np.atleast_2d(np.linspace(1,2.5, num=num)).T
pred, std = gpf.predict(x_re, return_std=True)
print(x.shape, observations_.shape)
y = generate_1d_data(x_re, num, 0.1)
plt.scatter(x_re, y, c='grey', label=r'$f(x) = x\,\sin(x)$ + Noise')
plt.scatter(x, observations_, c='r', label='Observations')
plt.plot(x_re, pred, 'b-', label='Prediction')
plt.fill(np.concatenate([x_re, x_re[::-1]]),
         np.concatenate([pred - 1.9600 * std,
                        (pred + 1.9600 * std)[::-1]]),
         alpha=.5, fc='grey', ec='None')#, label='95% confidence interval')
plt.xlabel('$x$')
plt.ylabel('$f(x)$')
plt.legend(loc='upper left')
plt.show()
