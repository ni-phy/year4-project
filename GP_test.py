import numpy as np
import matplotlib.pyplot as plt
import sklearn as sk
from sklearn import gaussian_process as gp
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

#Attemt to model noisy sinusoidal wave with GP
#Attempt1: using only Numpy
def exponential_cov(x, y, params):
  return params[0] * np.exp( -10 * params[1] * np.subtract.outer(x, y)**2)

def conditional(x_new, x, y, params):
 
  B = exponential_cov(x_new, x, params)
  C = exponential_cov(x, x, params)
  A = exponential_cov(x_new, x_new, params)
 
  mu = np.linalg.inv(C).dot(B.T).T.dot(y)
  sigma = A - B.dot(np.linalg.inv(C).dot(B.T))
 
  return (mu.squeeze(), sigma.squeeze())
def sinusoid(x):
  return np.sin( np.pi * x)

def generate_1d_data(num_training_points, observation_noise_variance):
  """Generate noisy sinusoidal observations at a random set of points.

  Returns:
     observation_index_points, observations
  """
  index_points_=np.linspace(0,2, num=num_training_points)
  #index_points_ = np.random.uniform(-1., 1., (num_training_points, 1))
  index_points_ = index_points_.astype(np.float64)
  # y = f(x) + noise
  observations_ = (sinusoid(index_points_) +
                   np.random.normal(loc=0,
                                    scale=np.sqrt(observation_noise_variance),
                                    size=(num_training_points)))
  return observations_

# Generate training data with a known noise level (we'll later try to recover
# this value from the data).
NUM_TRAINING_POINTS = 100
observations_ = generate_1d_data(
    num_training_points=NUM_TRAINING_POINTS, observation_noise_variance=.01)


theta = [1, 100]
σ_0 = exponential_cov(0, 0, theta)
xpts = np.arange(0, 2, step=0.01)

def predict(x, data, kernel, params, sigma, t):
  k = [kernel(x, y, params) for y in data]
  Sinv = np.linalg.inv(sigma)
  y_pred = np.dot(k, Sinv).dot(t)
  sigma_new = kernel(x, x, params) - np.dot(k, Sinv).dot(k)
  return y_pred, sigma_new
 
x_pred = np.linspace(2, 4, 100)

x = np.linspace(0, 2, num=NUM_TRAINING_POINTS)
#observations_ = sinusoid(x)
#mu, s = conditional(x_more, x, y, theta)
y = observations_#np.random.multivariate_normal(mu, s)#np.array(observations_)#np.exp(np.linspace(0, 1, num=5))#np.random.multivariate_normal(mu, s)

σ_new = exponential_cov(x, x, theta)
predictions = [predict(i, x_pred, exponential_cov, theta, σ_new, y) for i in x_pred]


y_pred, sigmas = np.transpose(predictions)
print(sigmas)
plt.plot(np.linspace(0,4), sinusoid(np.linspace(0,4)))
plt.plot(x_pred, y_pred, 'bo')
plt.plot(x, y, "ro")
plt.show()
