'''
https://github.com/cpbunker/learn/qiskit
'''

import utils

import qiskit
from qiskit import QuantumCircuit
from qiskit import quantum_info as qi
from qiskit import Aer
from qiskit.providers.aer import AerSimulator

from qiskit.visualization import plot_bloch_vector, plot_bloch_multivector, plot_histogram
import matplotlib.pyplot as plt
#try:  plt.rcParams.update({"text.usetex": True,"font.family": "Times"})

#### bloch sphere visualization

def bloch_qubits(state: qi.Statevector, my_title = '') -> None:
    '''
    Take a quantum_info.Statevector object and plot the state of the qubitith
    qubit on the bloch sphere
    '''
    assert(isinstance(state, qi.Statevector));

    state.draw(output = 'bloch', title = my_title, reverse_bits = True);
    plt.show();

    return None;


def bloch_state(state: qi.Statevector, vec0: str, vec1: str) -> None:
    '''
    Draw a (single or multiqubit) state on the bloch sphere with poles vec0, vec1
    '''
    assert(isinstance(state, qi.Statevector));
    statedict = state.to_dict();
    assert(vec0 in statedict and vec1 in statedict ); # allowed poles

    # get coefs
    coef0, coef1 = statedict[vec0], statedict[vec1];

    # convert to bloch sphere coordinates (see
    # https://en.wikipedia.org/wiki/Bloch_sphere#Plotting_pure_two-spinor_states_through_stereographic_projection)
    u = coef1/coef0; # complex number
    ux, uy = u.real, u.imag; # break into ux + i uy form
    px = 2*ux/(1 + ux*ux + uy*uy); # p is the bloch sphere point
    py = 2*uy/(1 + ux*ux + uy*uy);
    pz = (1 - ux*ux - uy*uy)/(1 + ux*ux + uy*uy);

    # plot using qiskit
    plot_bloch_vector([px, py, pz], title = '|0> = '+vec0+', |1> = '+vec1);
    plt.show();


#### circuit visualization

def circuit_counts(qc: QuantumCircuit, which = None, shots = 1024) -> None:
    '''
    Do a quantum simulation of myqc and plot histogram of the results

    measurement:
    - plotting results: sum over qubits not specified in 'which'
    - m gates:
        if qc has clbits, assume there are m gates manually set up.
        check that these correspond to the clbits in which.
        if not we will just measure all the qubits to new clbits
    '''
    assert(isinstance(qc, QuantumCircuit));

    # which qubits to count
    if which == None:
        which = list(range(qc.num_qubits));

    # whether measurement is needed
    if(len(qc.clbits)):
        # make sure qubits we want to count have clbits
        clbit_indices = [xbit.index for xbit in qc.clbits];
        for w in which:
            if w not in clbit_indices: raise ValueError;

    else: # measure onto new clbits measure_all
        qc.measure_all(add_bits = True);
        
    # run the job
    if True:
        mybackend = Aer.get_backend('qasm_simulator');
        result = qiskit.execute(qc, backend = mybackend, shots = shots).result();
        counts = result.get_counts();

    else:
        job = AerSimulator().run(qc); # physically runs the qc
        counts = job.result().get_counts();

    # show
    if(len(which) != qc.num_qubits):
        counts = utils.counts_to_subcounts(which, counts);
    plot_histogram(counts);
    plt.show();
    return None;


#### test code
    
if(__name__ == "__main__"):

    # null state
    null = qi.Statevector.from_label('00');

    # phi + bell state
    bell_qc = QuantumCircuit(2);
    bell_qc.h(1);
    bell_qc.cnot(0,1);
    print(bell_qc.draw());
    phi_plus = null.evolve(bell_qc);
    print(phi_plus.to_dict())

    # draw qubits
    bloch_qubits(phi_plus);

    # draw state
    bloch_state(phi_plus, '00', '10');
