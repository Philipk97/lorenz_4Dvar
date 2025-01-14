#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Matthias

run a lorenz model without data assimilation
"""

import sys
sys.path.append('../src/')

from lorenz import Model
import obs
import ana
from scipy.optimize import minimize
import matplotlib.pyplot as plt

import numpy as np

#########################
# parameter of simulation
#########################

dt = 0.01 # temporal discretisation
parameters = [10.,28.,8/3] # true parameters of the model
t_simu = 100 # number of iteration of the simulation


#########################
# assimilation parameter
#########################

# background state
Xb = np.array([0.93,0.,-13.60])
# background covariance error matrix
sigma_b = 1.
Pb = sigma_b*np.eye(3)
# observation covariance error matrix
sigma_y = 0.1
R = sigma_y*np.eye(3)


#########################
# TRUE MODEL
#########################
condi_ini = np.array([0.93,0.,-14.60]) # initial condition

# true model, reference
Lor_true = Model(dt,t_simu,parameters,condi_ini)
Lor_true.forward(9999)

#########################
# background model
#########################

Lor_back = Model(dt,t_simu,parameters,Xb)
Lor_back.forward(9999)

#########################
# observation parameter
#########################
n_sub = 1 # number of iteration between two observation

T_obs = [i*n_sub*dt for i in range(1,int(dt*t_simu))]

Obs = obs.Observation(int(dt*t_simu),n_sub)

Obs.gen_obs(Lor_true)

#########################
# Data Assimilation
#########################

# new initial condition
coef = 1.
delta_x = coef * np.random.random(3)
new_condi_ini = condi_ini + delta_x

# analysed model
Lor_ana = Model(dt,t_simu,parameters,new_condi_ini)

Var = ana.Variational(Xb, Pb, R, Lor_ana, Obs)


res = minimize(Var.cost,np.zeros(3),jac=Var.grad)

print('true state, x =',condi_ini,
      '\nresult of the analyse : x =',res.x)

print(f'cost of {res.x} :', Var.cost(res.x))



#########################
# Plot results
#########################

Lor_ana.x0 = res.x

Lor_ana.re_initiate()

Lor_ana.forward(int(t_simu*dt)) # store assimilation trajectory

t_obs = list(Obs.obs.keys())
t_obs.sort()
Xobs = np.array([Obs.obs[t] for t in t_obs])

plt.figure(figsize=(12,8))

plt.subplot(3,1,1) # plot X
plt.plot(Lor_true.time_series,Lor_true.xvar_series[:,0],label='true state')
plt.plot(Lor_true.time_series,Lor_ana.xvar_series[:,0],label='analysed')
plt.plot(Lor_true.time_series,Lor_back.xvar_series[:,0],label='background state')
plt.plot(t_obs,Xobs[:,0],'o')
plt.legend()

plt.subplot(3,1,2) # plot y
plt.plot(Lor_true.time_series,Lor_true.xvar_series[:,1],label='true state')
plt.plot(Lor_true.time_series,Lor_ana.xvar_series[:,1],label='analysed')
plt.plot(Lor_true.time_series,Lor_back.xvar_series[:,1],label='background state')
plt.plot(t_obs,Xobs[:,1],'o')
plt.legend()

plt.subplot(3,1,3) # plot z
plt.plot(Lor_true.time_series,Lor_true.xvar_series[:,2],label='true state')
plt.plot(Lor_true.time_series,Lor_ana.xvar_series[:,2],label='analysed')
plt.plot(Lor_true.time_series,Lor_back.xvar_series[:,2],label='background state')
plt.plot(t_obs,Xobs[:,2],'o')
plt.legend()



plt.show()

