'''
https://github.com/cpbunker/learn_qiskit
'''

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

import qiskit
import qiskit.quantum_info as qinfo
from qiskit.circuit import QuantumCircuit, ParameterVector


############################################################
#### mining types

class mine(object):
    '''
    A 3d collection of blocks
    Each block has a certain profit (self.w) equal to its value - its cost
    Each block is either mined or unmined
    '''

    #### overloads

    def __init__(self, values: np.ndarray, costs = None) -> None:
        self.dim = 3;
        if(type(values) != np.ndarray): raise TypeError;
        if(len(np.shape(values)) != self.dim): raise ValueError;
        if(costs == None): costs = np.zeros_like(values);

        # basic attributes
        self.shape = np.shape(values);
        self.n_blocks = self.shape[0]*self.shape[1]*self.shape[2];
        self.z = 1; # num nearest neighbors along each direction

        # profits and whether mined
        self.w = values - costs; # weights
        self.mined = np.zeros_like(values,dtype = int); # init unmined
        self.n_mined = sum(self.mined.flat);

        # blocks as qubits
        self.qc = QuantumCircuit(self.n_blocks);
        self.sv = qinfo.Statevector.from_int(0,2**self.n_blocks);
        self.gd = None;
        self.ham = self.construct_ham(1.0);       
        
    def __contains__(self,coord) -> bool:
        z,y,x = tuple(coord);
        if(z >=0 and z < self.shape[0]):
            if(y >=0 and y < self.shape[1]):
                if(x >=0 and x < self.shape[2]):
                    return True;
        return False;

    #### basic methods

    def set_mined(self, mined: np.ndarray) -> None:
        if(mined.dtype != int): raise TypeError;
        if(np.shape(mined) != self.shape): raise ValueError;
        self.mined = mined;
        self.n_mined = sum(self.mined.flat);

    def unmine(self):
        self.mined = np.zeros_like(self.mined);
        self.n_mined = sum(self.mined.flat);

    def get_coords(self, mined = False) -> np.ndarray:
        # get z,y,x coords of all (mined) blocks
        coords = np.zeros((self.n_blocks,self.dim),dtype=int);
        mask = np.zeros((self.n_blocks,),dtype=int);

        # iter over coords
        for zi in range(self.shape[0]):
            for yi in range(self.shape[1]):
                for xi in range(self.shape[2]):
                    blocki = zi*self.shape[1]*self.shape[2] + yi*self.shape[2] + xi;
                    coords[blocki] = [zi,yi,xi];
                    mask[blocki] = self.mined[zi,yi,xi];
        if mined:
            return coords[mask == 1];
        else:
            return coords;

    def get_parents(self, coord: list, mined = False) -> np.ndarray:
        # get z,y,x coords of all parent blocks
        zc,yc,xc = tuple(coord);
        size = 2*self.z + 1;
        parents = [];
        mask = [];

        # iter over coords
        for zi in [zc-1]:
            for yi in [yc-1,yc,yc+1]:
                for xi in [xc-1,xc,xc+1]:
                    if [zi,yi,xi] in self:
                        parents.append([zi,yi,xi]);
                        mask.append(self.mined[zi,yi,xi]);

        # return
        parents, mask = np.array(parents), np.array(mask);
        if mined:
            return parents[mask == 1];
        else:
            return parents;

    def show(self) -> None: 
        # plot labeled mine
        for y in range(self.shape[1]):
            sns.heatmap(self.mined[:,y,:], annot = self.w[:,y,:], cbar = False, cmap = matplotlib.colormaps["Reds"]);
            plt.show();

    #### properties of the mine

    def smoothness(self) -> int:
        smooth_func = 0;
        # iter over coords
        for zi in range(self.shape[0]):
            for yi in range(self.shape[1]):
                for xi in range(self.shape[2]):
                    # mined status
                    imined = self.mined[zi,yi,xi];
                    # parent mined status
                    j_coords = self.get_parents([zi,yi,xi]);
                    j_coords_mined = self.get_parents([zi,yi,xi],mined=True);
                    jmined = np.zeros((len(j_coords),));
                    for jindex in range(len(j_coords)):
                        j = j_coords[jindex];
                        if j in j_coords_mined:
                            jmined[jindex] = 1;
                    # update smoothness function
                    for j in jmined:
                        smooth_func += imined*(1-j);
        return smooth_func;

    #### qiskit methods

    def print(self) -> None:
        print(self.qc.draw());

    def ansatz(self) -> None:
        '''
        Prepare the mined status of the blocks as a quantum circuit ansatz, with
        1 qubit per block, 0 = unmined and 1 = mined, according to Latone Eq 2
        '''

        # implement single y's
        thetas = ParameterVector('t',self.n_blocks);
        for qi in range(self.n_blocks):
            self.qc.ry(thetas[qi],qi);
        self.qc.barrier();

        # implement controlled y's
        # qi is control and each of its parents is target
        cthetas = []; # parameter vectors for all the controlled y's
        # iter over coords
        for zi in range(self.shape[0]):
            for yi in range(self.shape[1]):
                for xi in range(self.shape[2]):
                    # coord and parents
                    coord = [zi,yi,xi];
                    parents = self.get_parents(coord);

                    # as qubit
                    qi = zi*self.shape[1]*self.shape[2] + yi*self.shape[2] + xi;
                    thetai = ParameterVector('t'+str(qi),len(parents));

                    # iter over parent coords
                    for parentindex in range(len(parents)):
                        zp, yp, xp = tuple(parents[parentindex]);
                        qj = zp*self.shape[1]*self.shape[2] + yp*self.shape[2] + xp;
                        self.qc.cry(thetai[parentindex],qi,qj);
                    self.qc.barrier();

    def measure(self, cutoff = 1e-3) -> dict:
        '''
        Make a classical measurement of the qc evolution
        '''
        probs = self.gd.probabilities_dict();
        return {key : val for key,val in probs.items() if val > cutoff};

    def construct_ham(self, gamma: float) -> qinfo.SparsePauliOp:
        '''
        Construct smoothness-constrained  Hamiltonian according to Latone Eq 1
        '''
        Hp, Hs = [], [];
        Istr = ''.join(np.full((self.n_blocks,),"I")); # for chaining I's

        # construct Hp (maximum profit)
        # iter over coords
        for zi in range(self.shape[0]):
            for yi in range(self.shape[1]):
                for xi in range(self.shape[2]):
                    
                    # get qubit and weight
                    qi = zi*self.shape[1]*self.shape[2] + yi*self.shape[2] + xi;
                    wi = self.w[zi,yi,xi];

                    # I -> Z at qi
                    Zstr = np.full((self.n_blocks,),"I");
                    Zstr[qi] = "Z";
                    Zstr = ''.join(Zstr);
                    hi = qinfo.SparsePauliOp.from_list([(Istr,wi/2),(Zstr,-wi/2)]);
                    Hp.append(hi);

        # construct Hs (smoothness constraint)
        # iter over coords
        for zi in range(self.shape[0]):
            for yi in range(self.shape[1]):
                for xi in range(self.shape[2]):
                    
                    # get qubit and weight
                    qi = zi*self.shape[1]*self.shape[2] + yi*self.shape[2] + xi;
                    coord = [zi,yi,xi];

                    # I -> Z at qi
                    Zstr = np.full((self.n_blocks,),"I");
                    Zstr[qi] = "Z";
                    Zstr = ''.join(Zstr);
                    hi = qinfo.SparsePauliOp.from_list([(Istr,1/2),(Zstr,-1/2)]);
                    Hs.append(hi);
                    raise NotImplementedError;

        # combine into Hamiltonian
        Ham = Hp;
        return qinfo.SparsePauliOp.sum(Ham);

    def solve(self, method = 'ed') -> None:
        '''
        Find the gd state of self.ham and store in self.gd
        Methods:
        -ed, exact diagonalization, use np.linalg.eigh to diagonalize the matrix
        -vqe, variational quantum eigensolver
        '''
        
        if(method == 'ed'):
            ham_mat = self.ham.to_matrix();
            eiges, eigvs = np.linalg.eigh(ham_mat);
            gdstate = eigvs[:,0];
            gdint = np.argmax(gdstate);
            print(gdint)
            self.gd = qinfo.Statevector.from_int(gdint,2**self.n_blocks);
            
        elif(method == 'vqe'):
            from qiskit.algorithms.minimum_eigensolvers import VQE
            from qiskit.algorithms.optimizers import SLSQP
            myVQE = VQE(qiskit.primitives.Estimator(),self.qc,SLSQP());
            result = myVQE.compute_minimum_eigenvalue(self.ham);
            optimal_circuit = self.qc.bind_parameters(result.optimal_parameters);
            self.gd = self.sv.evolve(optimal_circuit)
        
        else:
            raise NotImplementedError;
        

        
    


        
                
