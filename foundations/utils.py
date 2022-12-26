'''
https://github.com/cpbunker/learn/qiskit
'''

import numpy as np

import qiskit
from qiskit import QuantumCircuit
import qiskit.quantum_info as qi

#### type conversions

def int_to_str(n: int) -> str:
    '''
    convert a decimal integer to a bitstring
    '''
    assert(isinstance(n, int));

    return bin(n)[2:];

def str_to_qc(s: str, clbits = False) -> QuantumCircuit:
    '''
    Given a bit string s, creates a circuit which prepares that state

    clbits: whether to include a clbit for each qubit or not
    '''
    for c in s: assert(c in ['0','1']);

    # quantum circuit
    if(clbits):
        qc = QuantumCircuit(len(s), len(s));
    else:
        qc = QuantumCircuit(len(s));

    # flip 1s
    s = s[::-1]; # reverse bc of qiskit convention
    for ci in range(len(s)):
        if(s[ci] == '1'):
            qc.x(ci);

    qc.barrier();
    return qc;           
        

#### misc

def basis_strings(n: int) -> list:
    '''
    given a system of n qubits, output list of all the bit strings forming the
    computational basis

    e.g. n=2 returns ['00','01','10',11']
    '''
    assert(isinstance(n, int));

    # logical basis in decimal
    b_ints = np.array(range(2**n)); 

    # convert to bit strings
    b_strings = np.full(np.shape(b_ints), '0'*n);
    for i in range(len(b_strings)):
        bit = bin(b_ints[i])[2:];
        bit = '0'*(n-len(bit)) + bit; # standardize length
        b_strings[i] = bit;

    return list(b_strings);   


def basis_op(qc: QuantumCircuit) -> None:
    '''
    Given a quantum circuit acting on n qubits, operates on the 2**n basis states
    More general version of qiskit.quantum_info.Operator(QuantumCircuit)
    '''
    assert(isinstance(qc, QuantumCircuit));
    print(qc.name+" operation:");

    # iter thru basis in decimal
    for i in range(2**len(qc.qubits)):

        state = qi.Statevector.from_int(i, 2**len(qc.qubits));
        print("\n - ",state,"\n    ->",state.evolve(qc));
        
                
