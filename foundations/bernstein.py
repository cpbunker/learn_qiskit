'''
https://github.com/cpbunker/learn/qiskit

Adapted from "Bernstein-Vazirani Algorithm — Qiskit Foundations Ep 6" video
'''

import utils
import visuals

import qiskit
from qiskit import QuantumCircuit, QuantumRegister
import qiskit.quantum_info as qi

def qc_encode(s: str) -> QuantumCircuit:
    '''
    quantum circuit that encodes an unknown bit string
    '''
    assert(isinstance(s, str));
    for c in s: assert c in ['0','1'];
    n_bits = len(s);

    # quantum circuit with one ancilalry qubit
    qc = QuantumCircuit(n_bits + 1, n_bits);

    # iter over qubits
    # recall left -> right in bitstring is highest -> lowest in qubiti
    for biti in range(n_bits):
        if( s[biti] == '1'): # put an cx gate onto ancillary bit
            qubiti = n_bits - 1 - biti;
            qc.cx(qubiti, n_bits);

    return qc;


def qc_bernstein(n_bits: int) -> QuantumCircuit:
    '''
    Contructs a circuit which performs the Bernstein-Vazirani Algorithm to
    find the secret binary number of length n_bits in one shot
    '''
    assert(isinstance(n_bits, int));

    # init qc with all bits except ancillary superposed
    qc = QuantumCircuit(n_bits + 1, n_bits);
    qc.h(qc.qubits[:-1]);
    qc.barrier();

    # prep the ancillary bit
    qc.x(n_bits);
    qc.h(n_bits);
    qc.barrier();

    # encode the secret number into the circuit
    qc_number = qc_encode(GlobalSecretNumber);
    qc.compose(qc_number, qubits = qc.qubits, clbits = qc.clbits, inplace = True);
    qc.barrier();

    # undo superposition
    qc.h(qc.qubits[:-1]);

    # measure the secret number
    qc.measure(qc.qubits[:-1], qc.clbits);

    return qc;



GlobalSecretNumber = '1100'
myqc = qc_bernstein(len(GlobalSecretNumber));
print(myqc.draw());
visuals.circuit_counts(myqc, shots = 1); # should measure secret number 100% of the time

