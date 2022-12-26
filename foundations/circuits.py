'''
https://github.com/cpbunker/learn/qiskit

Adapted from "Building Blocks of Quantum Circuits — Qiskit Foundations Ep 4" video
'''

import visuals

import qiskit
from qiskit import QuantumCircuit, QuantumRegister
import qiskit.quantum_info as qi

# simple demonstration of superposition with hadamard
myqc = QuantumCircuit(1);
myqc.h(0);
visuals.circuit_counts(myqc); # this visualizer makes 1024 classical measurements
                                # onto automatically added clbits

