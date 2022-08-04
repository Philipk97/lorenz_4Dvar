# lorenz_4Dvar

This repository contains files to launch a 4Dvar assimilation using a chaotic lorenz model.

## Lorenz model

The Lorenz model consists of the time evolution of 3 coordinates $x$, $y$, and $z$ using the following equations: 
$$\frac{\partial x}{\partial t} = \sigma(x-y)$$
$$\frac{\partial y}{\partial t} = x(\rho - z) - y$$
$$\frac{\partial z}{\partial t} = xy - \beta z$$
Where $\sigma$, $\rho$ and $\beta$ are three real numbers.

# Project forked from original by Renaud Matthias
The repository includes modules to calculate forward, tangent linear and adjoint trajectories. There are also further modules to minimise the cost function and to assimilate data. 

# Modifications by Philip Kennedy include:
Improvements test.py
Changes to lorenz.py test function
Fixes to run_windows.py and run_multiple_windows.py