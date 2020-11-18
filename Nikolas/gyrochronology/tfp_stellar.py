# -*- coding: utf-8 -*-
"""tfp_stellar.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12pa5iGDPJicJiHpZYLn6jw8FKRycumcu
"""

pip install pyAstronomy

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow.compat.v2 as tf
import tensorflow_probability as tfp
from mpl_toolkits.mplot3d import Axes3D
from google.colab import files
import io

uploaded = files.upload()

data0 = data = np.array(pd.read_csv(io.BytesIO(uploaded['Data1.csv'])))

def mean_fn(x, y, a, b, c, d):
  return ((x*1000)**a * b*(y - c)**d)
#fn from Barnes 2007

from PyAstronomy import pyasl
r = pyasl.BallesterosBV_T()
b = pyasl.Ramirez2005()
bv = []
d0 = []
d1 = []
d2 = []

for i in range(len(data[:,3])):
  if data[i, 3]<1.1 and data[i, 3]>1:
    d0.append(data[i, 0])
    d1.append(data[i, 1])
    d2.append(data[i, 2])

data1= np.array([d0, d1, d2]).T
print(data1)
for i in data1[:,0]:
  bv.append(r.t2bv(i))
a = 0.5189
b=0.75
c=0.4
d=0.601
x = mean_fn(data1[:,2], np.array(bv), a, b, c ,d)
plt.scatter(data1[:,2], x, c=bv, cmap='hsv')
plt.show()
plt.scatter(data1[:,2], data1[:,1]-x, c=bv, cmap='hsv')
plt.show()

from mpl_toolkits.axes_grid1 import make_axes_locatable

fig, ax = plt.subplots()
divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='5%', pad=0.05)
# plt.xlabel('Rotation(Days)')
# plt.ylabel('Age (Gyr)')

im = ax.scatter(data1[:,2], data1[:,1], c=bv, cmap='hsv')
fig.colorbar(im, cax=cax, orientation='vertical', label='B-V')

data = data1
tf.enable_v2_behavior()

tfb = tfp.bijectors
tfd = tfp.distributions
psd_kernels = tfp.math.psd_kernels

# observations from a known function at some random points.
al = 10
X1 = data[::al,2] #age
X2 = r.t2bv(data[::al,0])#data[::al,2] #B_V
X = np.dstack([X1, X2]).reshape(-1, 2)

x1_mesh, x2_mesh = np.meshgrid(X1, X2)

resolution = len(X1)
X1_test = X1_plot = np.linspace( np.min(X1), np.max(X1), num=resolution )
X2_test = X2_plot = np.linspace( np.min(X2), np.max(X2), num=resolution )
X1_test, X2_test = np.meshgrid( X1_test, X2_test )
X_test = np.dstack([X1_test, X2_test]).reshape(resolution, resolution, 2)
a = 0.5189
b=0.75
c=0.4
d=0.601

amplitude = tfp.util.TransformedVariable(
  1., tfb.Exp(), dtype=tf.float64, name='amplitude')
length_scale = tfp.util.TransformedVariable(
  20., tfb.Exp(), dtype=tf.float64, name='length_scale')
length_scale1 = tfp.util.TransformedVariable(
  20., tfb.Exp(), dtype=tf.float64, name='length_scale')
# a =  tfp.util.TransformedVariable(
#   0.5189, tfb.Exp(), dtype=tf.float64, name='a')
# b = tfp.util.TransformedVariable(
#   0.75, tfb.Exp(), dtype=tf.float64, name='b')
# c = tfp.util.TransformedVariable(
#   0.4, tfb.Exp(), dtype=tf.float64, name='c')
# d = tfp.util.TransformedVariable(
#   0.601, tfb.Exp(), dtype=tf.float64, name='d')
Y = (data[::al, 1] - mean_fn(X1, X2, a, b, c, d))#.reshape(-1,1)


observation_index_points = X 
observations = Y#.T
kernel = psd_kernels.ExponentiatedQuadratic(amplitude, length_scale=10)* psd_kernels.ExponentiatedQuadratic(amplitude, length_scale=1)

observation_noise_variance = tfp.util.TransformedVariable(
   np.exp(0), tfb.Exp(), name='observation_noise_variance')

optimizer = tf.optimizers.Adam(learning_rate=.05, beta_1=.5, beta_2=.99)

# trainable_variables = [v.trainable_variables[0] for v in 
#                        [amplitude_var,
#                        length_scale_var,
#                        observation_noise_variance_var]]
@tf.function
def optimize():
  with tf.GradientTape() as tape:
    loss = -gp.log_prob(observations)
  grads = tape.gradient(loss, gp.trainable_variables)
  optimizer.apply_gradients(zip(grads, gp.trainable_variables))
  return loss

gp = tfd.GaussianProcessRegressionModel(
    kernel=kernel,
    index_points=X_test,
    observation_index_points=observation_index_points,
    observations=observations, observation_noise_variance=observation_noise_variance)

#First train the model, then draw and plot posterior samples.
for i in range(1000):
  neg_log_likelihood_ = optimize()
  if i % 100 == 0:
    print('.')

print("Final NLL = {}".format(neg_log_likelihood_))

samples = gp.sample(10).numpy()
var = gp.variance()
# ==> 10 independently drawn, joint samples at `index_points`.
# ==> 10 independently drawn, noisy joint samples at `index_points`

fig, ax = plt.subplots()
divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='5%', pad=0.05)
# plt.xlabel('Rotation(Days)')
# plt.ylabel('Age (Gyr)')

im = ax.scatter(X1_test, samples[0]+mean_fn(X1_test, X2_test, a, b, c ,d), cmap='hsv', c=X2_test)
fig.colorbar(im, cax=cax, orientation='vertical', label='B-V')
plt.show()

fig = plt.figure(figsize=(18, 10))
ax = plt.axes(projection='3d')
ax.view_init(20, 60)
ax.plot_surface(X1_test, X2_test, samples[0]+mean_fn(X1_test, X2_test, a, b, c, d), antialiased=True, alpha=0.7, linewidth=0.5, cmap='winter')
ax.scatter3D(X1, X2, (data[::al,1]).reshape(-1,1), 
             marker='o',edgecolors='k', color='r', s=150)
#ax.set_zlim(0, 50)
ax.set_xlabel('B-V Index')
ax.set_ylabel('Rotation Period (Days)')
ax.set_zlabel('Age (Gyr)')

plt.show()

numElems = len(Y)
sample = samples[0]+mean_fn(X1, X2, a ,b ,c ,d)
idx = np.round(np.linspace(0, len(np.array(sample).reshape(numElems**2)) - 1, numElems)).astype(int)
# Picks equal spaced elements from (longer) prediction array so that its shape of data

mu_test = (np.array(sample).reshape(numElems**2)[idx])
sd_test = (np.array(var).reshape(numElems**2)[idx]) 

vals = np.sort([mu_test, sd_test], axis=1)

print(vals.shape)

plt.figure(figsize=(18,9))
print(Y.shape, X1.shape)
plt.errorbar(np.sort(data[::al,1]), vals[0,:], yerr=vals[1,:], fmt='bo')
plt.scatter(np.sort(data[::al,1]), vals[0,:])
plt.plot(np.linspace( np.min(vals[0,:]), np.max(vals[0,:]), num=resolution ), 
         np.linspace( np.min(vals[0,:]), np.max(vals[0,:]), num=resolution ), 'r')

plt.xlabel('Data')
plt.ylabel('Prediction')

Z = (np.sort(data[::al,0])-vals[0,:])/vals[1,:]
print(Y.shape)
plt.figure(figsize=(9,8))
plt.hist(Z, density=True, bins=20)
mu, sigma = 0, 1 # mean and standard deviation
s = np.random.normal(mu, sigma, 1000)
# count, bins, ignored = plt.hist(s, 30, density=True)
# plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
#                np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
#          linewidth=2, color='r', alpha=0.9)
plt.xlabel('(Data - Prediction)/$\sigma$')
plt.ylabel('Frequency')

