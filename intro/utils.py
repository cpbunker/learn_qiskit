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

def counts_to_subcounts(indices: list, counts: dict) -> dict:
    '''
    Given a dictionary containing eihter probabilites (eg from
    Statevector.probabilities_dict) or counts (eg from qiskit.execute.get_counts)
    spanning the whole qubit space, collapse to just certain qubits of interest.
    '''
    if( not isinstance(counts,dict)): raise TypeError;
    n_qubits = len(counts.copy().popitem()[0]);
    if( len(indices) > n_qubits): raise ValueError;
    if( len(indices) > 1): raise NotImplementedError;

    # iter over qubits of interest
    sub_counts = dict();
    for index in indices:
        revindex = n_qubits - 1 - index; # bc qiskit is little endian
        index_count_0 = 0;
        index_count_1 = 0;

        # iter over all counts
        for bitstring in counts.keys():
            if(bitstring[revindex] == '0'): 
                index_count_0 += counts[bitstring];
            else:
                index_count_1 += counts[bitstring];

        # store in subcounts
        sub_bitstring_0 = np.full((n_qubits,),'x');
        sub_bitstring_0[revindex] = '0';
        sub_bitstring_0 = ''.join(sub_bitstring_0);
        sub_counts[sub_bitstring_0] = index_count_0;
        sub_bitstring_1 = np.full((n_qubits,),'x');
        sub_bitstring_1[revindex] = '1';
        sub_bitstring_1 = ''.join(sub_bitstring_1);
        sub_counts[sub_bitstring_1] = index_count_1;

    if(sum(counts.values()) != sum(sub_counts.values())): raise Exception;
    return sub_counts;    

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
        
                
