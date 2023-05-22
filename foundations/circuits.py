'''
https://github.com/cpbunker/learn/qiskit

Adapted from "Building Blocks of Quantum Circuits — Qiskit Foundations Ep 4" video
'''

import visuals
import numpy as np

import qiskit
from qiskit import QuantumCircuit, QuantumRegister
import qiskit.quantum_info as qi

# simple demonstration of superposition with hadamard
if False:
    myqc = QuantumCircuit(1);
    myqc.h(0);
    visuals.circuit_counts(myqc);
    # this visualizer makes 1024 classical measurements
    # onto automatically added clbits

# rotation
if False:
    myqc = QuantumCircuit(1);
    theta = np.arccos(3/5)
    print(theta/np.pi)
    myqc.rx(theta, 0);
    visuals.circuit_counts(myqc);

# make the Bell \Phi^+ state
if True:

    makebell = QuantumCircuit(2);
    makebell.h(0);
    makebell.cx(0,1);

    initstate = qi.Statevector.from_int(0, 2**2);
    print(initstate.to_dict());
    finalstate = initstate.evolve(makebell);
    print(finalstate.to_dict());

