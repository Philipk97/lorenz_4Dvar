#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 15:54:38 2021

@author: renamatt
"""
import sys
sys.path.append('../src')

import lorenz as lor
import obs
import windows as wdw
sys.path.append('../')
import diagnostic as diag
import matplotlib.pyplot as plt
import numpy as np

# CONFIGURATION
###############################################################################

#########################
# parameter of simulation
#########################


dt = 0.01 # temporal discretisation
t_simu = 1.0
parameters = [10.,28.,8/3] # true parameters of the model
X0 = np.array([0.93,0.00,-14.60])

# numerical scheme : euler,
# sch = 'euler'
scheme = 'RK4'

# assimilation windows parameters
n_window = 20 # number of iteration contained in an assimilation window (need to be even)
n_step = n_window//2 # number of iteration between two assimilation, the window cross each other
n_assimil = 9 # number of assimilation windows
n_simul = (1+n_assimil)*n_step # number of iteration of the simulation


#########################
# observation parameter
#########################

# one observation every n_sub iteration
n_sub = 1 # number of iteration between two observations


#########################
# assimilation parameter
#########################

# new parametrs for assimilation
# delta for each parameters
d_param = [0., -0.05, 0.] # d sigma, d rho, d beta
par_assimil = []
for i in range(3) :
    new_param = parameters[i] + d_param[i]
    par_assimil.append(new_param)

# initial background state
Xb = np.array([0.93,0.00,-14.60])


###############################################################################

# RUN

#########################
# run assimilation
#########################

M_true,M_ana, Obs = wdw.assimil(n_window,n_step,n_assimil,n_simul,dt,t_simu,parameters,\
                            par_assimil,n_sub,X0,Xb,scheme=scheme)

#########################
# plot results
#########################

var_to_plot = 'x' # x,y or z

dict_coord = {'x':0,'y':1,'z':2}
coord = dict_coord[var_to_plot]

time = [i*dt for i in range(n_simul)]
time_obs = [i*dt for i in Obs.iter_obs]
time_window = np.array([i*dt for i in range(0,n_simul-n_step,n_step)])

name_coord = {0 : 'x',1 : 'y',2 : 'z'}

observations = np.array(list(Obs.obs.values()))

coord = 2

fig, ax = plt.subplots(figsize=(10,5))

ax.plot(time,M_true.xvar_series[:,coord],label='true')
ax.plot(time,M_ana.xvar_series[:,coord],label='ana')
ax.plot(time_obs,observations[:,coord],'o')
ax.vlines(time_window,ax.get_ylim()[0],ax.get_ylim()[1], linestyles='dashed')
ax.set_ylabel(name_coord[coord])
ax.set_xlabel('time, s')
ax.legend()


X_ref = np.copy(M_true.xvar_series)
X = np.copy(M_ana.xvar_series)

score = diag.SCORE(X_ref,X)
score_wdw = np.array([score[i] for i in range(0,n_simul-n_step,n_step)])

fig, ax = plt.subplots(figsize=(10,4))
ax.plot(time,score)
ax.plot(time_window,score_wdw,'o',color='red')
ax.set_ylim(bottom=0.8)
ax.set_ylabel("score")
ax.set_xlabel("time, s")
fig.show()
plt.show()



