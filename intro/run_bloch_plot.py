'''
https://github.com/cpbunker/learn/qiskit
'''

import qiskit
import qiskit.quantum_info as qinfo
from qiskit.circuit import QuantumCircuit, ParameterVector
from qiskit import visualization

import numpy as np
import matplotlib.pyplot as plt

# standardize plots
myfontsize = 14;
#plt.rcParams.update({"text.usetex": True,"font.family": "Times"})

# plot_bloch_vector
theta, phi = np.pi/4, 3*np.pi/4
fig = visualization.plot_bloch_vector([np.cos(phi)*np.sin(theta),np.sin(phi)*np.sin(theta),np.cos(theta)]);

ax = fig.add_axes((0.0,0.0,1.0,1.0));
label = '$|\chi \\rangle$'
ax.text(0.85,0.85,label,transform=ax.transAxes,fontsize=myfontsize,
        verticalalignment='top');
ax.axis('off');
plt.tight_layout();
plt.show();
#assert False

# visualize_transition
equatorial_rotation = QuantumCircuit(1);
#equatorial_rotation.initialize("1");
#equatorial_rotation.set_statevector(qinfo.Statevector([0,1,0]));
for _ in range(2):
    equatorial_rotation.y(0);
fig = visualization.visualize_transition(equatorial_rotation,trace=True,fpg=20,spg=1);
