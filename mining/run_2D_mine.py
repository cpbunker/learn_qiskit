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
import qiskit.quantum_info as qi

#######################################################
#### define the OPM problem

# digging values -> mine object
values = np.array([[[-2,3,-1]], # indices are z,y,x
                   [[-9,5,-9]],
                   [[-9,-9,-9]]]);
mine = mines.mine(values);

# dig some blocks
dig = np.zeros_like(values);
dig[1,0] = np.array([1,1,1]);
dig[1,0,1] = 1;
mine.set_mined(dig);

# visualize
mine.show();

# parents
print("->",mine.smoothness());

