'''
https://github.com/cpbunker/learn/qiskit

Adapted from "Quantum Teleportation Algorithm — Qiskit Foundations Ep 5" video
'''

import utils
import visuals

import qiskit
from qiskit import QuantumCircuit, QuantumRegister
import qiskit.quantum_info as qinfo

def qc_teleport() -> QuantumCircuit:
    '''
    copying of quantum bits is not allowed
    we want to transfer ('teleport') quantum state from q0 to q2
    an ancillary qubit q1 is required as well
    '''
    
    # build q0, q1, q2 as circuit
    n_qubits = 3
    qc = QuantumCircuit(n_qubits, n_qubits);

    # teleportation protocol

    # entangle q1 and q2
    #qc.x(2)
    qc.h(1);
    qc.cx(1,2);

    if True:
        print(qc.draw())
        sv = qinfo.Statevector.from_int(0,2**n_qubits);
        sv = sv.evolve(qc);
        print(sv.to_dict());
        assert False;

    # entangle q0 and q1 in reverse order
    qc.cx(0,1);
    qc.h(0);

    # measure 0 and 1
    qc.barrier();
    qc.measure([0,1],[0,1]);

    # entangle 1, 2; 0,2
    qc.barrier();
    qc.cx(1,2);
    qc.cz(0,2);
    
    return qc;

# prep state 001
state0_str = '000';
n_qubits = len(state0_str);
myqc = utils.str_to_qc(state0_str, clbits = True);
myqc.h(2); myqc.barrier();
print(myqc.draw());

# teleport q0 -> q2, st 001 -> 100
myqc.compose(qc_teleport(), qubits = [0,1,2], clbits = [0,1,2], inplace = True);
print(myqc.draw());

# verify
myqc.measure([2],[2]);
print(myqc.draw());
visuals.circuit_counts(myqc, which = [2]); # we can see that q2 is always in state 1
