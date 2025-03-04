#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 10:53:09 2021

@author: Matthias
"""

import numpy as np
from scipy.optimize import minimize
from scipy.linalg import inv
import matplotlib.pyplot as plt


class Variational :
    
    def __init__(self,Xb=None,B=None,R=None,M=None,Obs=None,i0=0) :
        self.Xb = Xb # background state
        self.B = B # background covariance error matrix
        self.Rinv = inv(R) # observation covariance error matrix
        self.M = M # Lorenz model
        self.Obs = Obs # observations (class observation)
        self.i0 = i0 # iteration corresponding to initial time of the current window
        
    
    def cost(self,X) :
        '''
        coast function to minimize
         INPUTS :
             - initial coordinates
         OUTPUTS :
             - Jout, value of the cost function, float
        '''
        # re initialize the model
        self.M.re_initiate()
        # background cost
        if self.B is not None :
            b_er = X-self.Xb # background error
            gb = np.dot(inv(self.B),b_er)
            Jb = 0.5*np.dot(b_er,gb)
        else :
            Jb = 0
        
        # observation cost
        Jo = 0.
        u = np.copy(X)
        
         # store trajectory
        u_trj = [u]
        
        for it in range(self.i0,self.M.n_iter+self.i0) :
            if self.Obs.isobserved(it) :
                miss = self.Obs.misfit(it,u) # H.x - y
                Jo = Jo + np.dot(miss,np.dot(self.Rinv,miss))
            u = self.M.step(u) # forward step
            u_trj.append(u)
        
        self.u_trj = u_trj # keep the trajectory for gradient computation
        
        J = 0.5*Jo + Jb # total cost
        return J
    
    def grad(self,X) :
        '''
        compute the gradient of the cost function at coordinates X using adjoint coding
        INPUTS :
         - X : size 3 array containing the coordinates (x,y,z) where the gradient has to be evaluated
        RETURN :
         - u_adj : the gradient of the cost function
        '''
        # re initialize the model
        self.M.re_initiate()
        # background cost
        if self.B is not None :
            b_er = X-self.Xb # background error
            grad_b = np.dot(inv(self.B),b_er) # gradient related to the background
        else :
            grad_b = 0
        i_last = self.i0 + self.M.n_iter # last iteration
        
        # adjoint coding
        u_adj = np.zeros(3)
        # backward in time
        for i in range(self.M.n_iter-1,-1,-1) :
            u_adj = self.M.step_adj(self.u_trj[i], u_adj) # adjoint step
            if self.Obs.isobserved(i+self.i0) :
                # observation term if it exist
                inov = self.Obs.misfit(self.i0+i,self.u_trj[i]) # compute inovation
                u_adj += self.Obs.H[i].T @ self.Rinv @ inov

        # add background component
        u_adj += grad_b
        # u_adj is the gradient of the cost function at X
        return u_adj
    
    def grad_test(self,deg=10,plot=False) :
        '''
        Computes the gradient test
        INPUTS :
        deg : precision of the test, 
        plot : if true, the result of the test is plotted
        '''
        X = 10*np.random.randn(3)
        dX = np.random.randn(3)
        J = self.cost(X)
        G = self.grad(X)
        L_plot = [] # list containing test values for plot option
        print("** GRADIENT TEST **\n")
        for i in range(deg) :
            test = 1 - (self.cost(X+10**-i*dX)-J)/np.dot(G,10**-i*dX)
            print(test)
            print(f'{10**-i:2E} : {test:2E}\n')
            L_plot.append(abs(test))
        if plot :
            fig, ax = plt.subplots()
            L_prec = [10**-i for i in range(deg)]
            ax.loglog()
            plt.gca().invert_xaxis()
            ax.plot(L_prec,L_plot)
            fig.show()
            plt.show()
        
        
        


