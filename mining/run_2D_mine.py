'''
https://github.com/cpbunker/learn_qiskit

Frame the 2D open pit mining (OPM) problem as a binary linear
optimization (BLO) problem

Use variational quantum eigensolver (VQE) to solve the problem
'''

import mines

import numpy as np
import matplotlib.pyplot as plt

import qiskit
import qiskit.quantum_info as qinfo

#######################################################
#### define the OPM problem

# digging values -> mine object
values = np.array([[[-2,3,-1]], # indices are z,y,x
                   [[-9,5,-9]]],dtype=int);
values = np.ones_like(values);
shape = np.shape(values);
special = 5;
for zi in range(shape[0]):
    for yi in range(shape[1]):
        for xi in range(shape[2]):
            qi = zi*shape[1]*shape[2] + yi*shape[2] + xi;
            if qi == special: values[zi,yi,xi] = -1;
mine = mines.mine(values);

# dig some blocks
dig = np.zeros_like(values);
dig[0,0] = np.array([1,1,1]);
dig[1,0,1] = 1;
mine.set_mined(dig);

# visualize
mine.unmine();
mine.show();

# entangled ansatz
mine.ansatz();
#mine.print();

# solve
mine.solve(method='vqe');
print(mine.measure());



