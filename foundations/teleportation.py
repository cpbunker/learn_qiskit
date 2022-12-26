'''
https://github.com/cpbunker/learn/qiskit

Adapted from "Quantum Teleportation Algorithm — Qiskit Foundations Ep 5" video
'''

import utils
import visuals

import qiskit
from qiskit import QuantumCircuit, QuantumRegister
import qiskit.quantum_info as qi

def qc_teleport() -> QuantumCircuit:
    '''
    copying of quantum bits is not allowed
    we want to transfer ('teleport') quantum state from q0 to q2
    an ancillary qubit q1 is required as well
    '''
    
    # build q0, q1, q2 as circuit
    qc = QuantumCircuit(3, 3);

    # teleportation protocol

    # entangle q1 and q2
    qc.h(1);
    qc.cx(1,2);

    # entangle q0 and q1 in reverse order
    qc.cx(0,1);
    qc.h(0);

    # measure 0 and 1
    qc.barrier()
    qc.measure([0,1],[0,1]);

    # entangle 1, 2; 0,2
    qc.barrier()
    qc.cx(1,2);
    qc.cz(0,2);
    
    return qc;

# prep state 001
state0_str = '001';
myqc = utils.str_to_qc(state0_str, clbits = True);
print(myqc.draw());

# teleport q0 -> q2, st 001 -> 100
myqc.compose(qc_teleport(), qubits = [0,1,2], clbits = [0,1,2], inplace = True);
print(myqc.draw());

# verify
myqc.measure([2],[2]);
visuals.circuit_counts(myqc); # we can see that q2 is always in state 1
