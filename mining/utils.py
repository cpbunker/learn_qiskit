'''
https://github.com/cpbunker/learn_qiskit
'''

import numpy as np

import qiskit
from qiskit import QuantumCircuit
import qiskit.quantum_info as qinfo

############################################################
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

def BLO_to_ham(w: np.ndarray) -> qinfo.SparsePauliOp:
    '''
    Convert an unconstrained binary linear optimization problem (BLO),
    defined as find state x to minimize w \cdot x, where w is a vector
    of n weights and x is a vector of n qubits
    '''

    Istr = np.full((len(w),),"I");
    Istr = ''.join(Istr);
    Hop = [];

    for windex in range(len(w)):
        wi = w[windex];
        Zstr = np.full((len(w),),"I");
        Zstr[windex] = "Z";
        Zstr = ''.join(Zstr);
        hi = qi.SparsePauliOp.from_list([(Zstr,0.5*wi),(Istr,-0.5*wi)]);
        Hop.append(hi);

    return qinfo.SparsePauliOp.sum(Hop);

############################################################
#### mining

def get_parents(coords):
    '''
    returns a 1d array of the coords of the parents of the block coord
    '''
    if(coords.dtype != int): raise TypeError;
    if(np.shape(coords) != (3,)): raise ValueError;

    # parents are 3 x 3 block w/ z one higher
    parents = np.zeros((3,3,3));
    for deltax in [-1,0,1]:
        for deltay in [-1,0,1]:
            parents[deltax+1,deltay+1] += np.array([coords[0]+deltax,coords[1]+deltay,coords[2]+1]);

    return parents;
        
    

############################################################
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
        
                
