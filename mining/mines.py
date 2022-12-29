'''
https://github.com/cpbunker/learn_qiskit
'''

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


############################################################
#### mining types

class mine(object):
    '''
    A 3d collection of blocks
    Each block has a certain profit (self.w) equal to its value - its cost
    Each block is either mined or unmined
    '''

    def __init__(self, values, costs = None):
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
        self.mined = np.zeros_like(values,dtype = int);
        self.n_mined = sum(self.mined.flat);

    def __contains__(self,coord):
        z,y,x = tuple(coord);
        if(z >=0 and z < self.shape[0]):
            if(y >=0 and y < self.shape[1]):
                if(x >=0 and x < self.shape[2]):
                    return True;
        return False;

    def set_mined(self, mined):
        if(mined.dtype != int): raise TypeError;
        if(np.shape(mined) != self.shape): raise ValueError;
        self.mined = mined;
        self.n_mined = sum(self.mined.flat);

    def get_coords(self, mined = False):
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

    def get_parents(self, coord, mined = False):
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

    def smoothness(self):
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

    def show(self): 
        # plot labeled mine
        for y in range(self.shape[1]):
            sns.heatmap(self.mined[:,y,:], annot = self.w[:,y,:], cbar = False, cmap = matplotlib.colormaps["Reds"]);
            plt.show();

        
    


        
                
