'''
https://github.com/cpbunker/learn/qiskit
'''

import qiskit
from qiskit.visualization import plot_bloch_vector

import matplotlib.pyplot as plt
plt.rcParams.update({"text.usetex": True,"font.family": "Times"})

fig = plot_bloch_vector([0,1,0]);
plt.show();
