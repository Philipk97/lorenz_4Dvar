#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 14:46:57 2021

@author: Matthias
"""
import sys
sys.path.append('../src/')

from lorenz import Model
import ana
import windows as wdw
import numpy as np


#########################
# parameter of simulation
#########################

dt = 0.01 # temporal discretisation
t_sim = 1000
param = [10.,28.,8/3] # true parameters of the model
n_simul = 30 # number of iteration of the simulation
scheme = 'RK4'
X0 = np.array([0.93,0.00,-14.60]) # initial condition

### ADJOINT & TANGENT TEST ###
Lor = Model(dt,t_sim,param,scheme=scheme,test=True,X0=X0)


### GRADIENT TEST ###

n_sub = 5 # time step between two observations

Obs = wdw.create_Obs(Lor,n_simul,n_sub)

Xb = np.array([0.5,0.00,-12.])
R = Obs.std*np.eye(3) # observation error covariance matrix
B = np.eye(3) # background error covariance matrix

Var = ana.Variational(Xb=Xb,B=B,R=R,M=Lor,Obs=Obs)

Var.grad_test(plot=True)
