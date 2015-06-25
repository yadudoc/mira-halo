#!/usr/bin/env python
import itertools
import pprint
import numpy as np

pp = pprint.PrettyPrinter(indent=4,depth=6)

A_dim, B_dim, C_dim, D_dim, E_dim, T_dim = [4,4,4,4,2,16]


def regular_mapping(ofile):
    fd = open(ofile, 'w')
    for A in range(0, A_dim):
        for B in range(0, B_dim):
            for C in range(0, C_dim):
                for D in range(0, D_dim):
                    for E in range(0, E_dim):
                        for T in range(0, T_dim):
                            #print A, B, C, D, E, T
                            #print '{0} {1} {2} {3} {4} {5}'.format(A,B,C,D,E,T)
                            fd.write('{0} {1} {2} {3} {4} {5}\n'.format(A,B,C,D,E,T))
    fd.close()


def line_mapping(ofile):
    fd = open(ofile, 'w');
    for T in range(0, T_dim):
        for E in range(0, E_dim):
            for D in range(0, D_dim):
                for C in range(0, C_dim):
                    for B in range(0, B_dim):
                        for A in range(0, A_dim):
                            print A, B, C, D, E, T
                            fd.write('{0} {1} {2} {3} {4} {5}\n'.format(A,B,C,D,E,T))
    fd.close()  



def skewed1_mapping(ofile):
    fd = open(ofile, 'w')
    for A in [0, 2, 1, 3]:
        for B in [0, 2, 1, 3]:
            for C in [0, 2, 1, 3]:
                for D in [0, 2, 1, 3]:
                    for E in [0, 1]:
                        for T in range(0, T_dim):
                            print A, B, C, D, E, T
                            #print '{0} {1} {2} {3} {4} {5}'.format(A,B,C,D,E,T)
                            fd.write('{0} {1} {2} {3} {4} {5}\n'.format(A,B,C,D,E,T))
    fd.close()

def skewed2_mapping(ofile):
    fd = open(ofile, 'w');
    for T in range(0, T_dim):
        for E in [0, 1]:
            for D in [0, 2, 1, 3]:
                for C in [0, 2, 1, 3]:
                    for B in [0, 2, 1, 3]:
                        for A in [0, 2, 1, 3]:
                            print A, B, C, D, E, T
                            fd.write('{0} {1} {2} {3} {4} {5}\n'.format(A,B,C,D,E,T))
    fd.close()  



def box_mapping():    
    APP_DIMS  =(4,4,4,4,4)
    PHYS_DIMS =(4,4,4,4,2,16)
    APP_SLOTS = reduce( lambda x,y : x*y, APP_DIMS)
    PHYS_SLOTS= reduce( lambda x,y : x*y, PHYS_DIMS)

    if APP_SLOTS != PHYS_SLOTS :
        print "ERROR! Total app slots do not match physical slots"
        exit(1)
        
    print "Application dimensions : ", APP_DIMS
    print "Physical dimensions    : ", PHYS_DIMS
        
    OUTER_DIM = []
    for dim in PHYS_DIMS:
        INNER_DIM = [ [x] for x in range(0,dim) ]
        if not OUTER_DIM :
            OUTER_DIM = INNER_DIM
        else:
            T = [ a+b for a in OUTER_DIM for b in INNER_DIM ]
            OUTER_DIM = T

def slice1_mappings(ofile):
    fd = open(ofile, 'w');
    x = np.array(xrange(0, 8192)) # 4x4x4x4                                                                                                                                                   
    print x.shape
    origin = np.reshape(x, (4,4,4,4,2,16), order='C' )
    #pp.pprint(y)
    #pp.pprint(origin[0,0:4,0:4,0:4,0:2,0:8])
    
    # SWAP ALONG A_DIM
    SOURCE=np.ndarray.copy(origin[0, 0:4, 0:4, 0:4, 0:2, 8:16])
    origin[0, 0:4, 0:4, 0:4, 0:2, 8:16] = origin[2, 0:4, 0:4, 0:4, 0:2, 0:8] 
    origin[2, 0:4, 0:4, 0:4, 0:2, 0:8]  = SOURCE
    SOURCE=np.ndarray.copy(origin[1, 0:4, 0:4, 0:4, 0:4, 8:16])
    origin[1, 0:4, 0:4, 0:4, 0:2, 8:16] = origin[3, 0:4, 0:4, 0:4, 0:2, 0:8]  
    origin[3, 0:4, 0:4, 0:4, 0:2, 0:8]  = SOURCE

    # SWAP ALONG B_DIM
    SOURCE=np.ndarray.copy(origin[0:4, 0, 0:4, 0:4, 0:2, 8:16])
    origin[0:4, 0, 0:4, 0:4, 0:2, 8:16] = origin[0:4, 2, 0:4, 0:4, 0:2, 0:8]
    origin[0:4, 2, 0:4, 0:4, 0:2, 0:8]  = SOURCE
    SOURCE=np.ndarray.copy(origin[0:4, 1, 0:4, 0:4, 0:4, 8:16])
    origin[0:4, 1, 0:4, 0:4, 0:2, 8:16] = origin[0:4, 3, 0:4, 0:4, 0:2, 0:8]
    origin[0:4, 3, 0:4, 0:4, 0:2, 0:8]  = SOURCE

    # SWAP ALONG C_DIM
    SOURCE=np.ndarray.copy(origin[0:4, 0:4, 0, 0:4, 0:2, 8:16])
    origin[0:4, 0:4, 0, 0:4, 0:2, 8:16] = origin[0:4, 0:4, 2, 0:4, 0:2, 0:8]
    origin[0:4, 0:4, 2, 0:4, 0:2, 0:8]  = SOURCE
    SOURCE=np.ndarray.copy(origin[0:4, 0:4, 1, 0:4, 0:2, 8:16])
    origin[0:4, 0:4, 1, 0:4, 0:2, 8:16] = origin[0:4, 0:4, 3, 0:4, 0:2, 0:8]  
    origin[0:4, 0:4, 3, 0:4, 0:2, 0:8]  = SOURCE

    # SWAP ALONG D_DIM
    SOURCE=np.ndarray.copy(origin[0:4, 0:4, 0:4, 0, 0:4, 8:16])
    origin[0:4, 0:4, 0:4, 0, 0:2, 8:16] = origin[0:4, 0:4, 0:4, 2, 0:2, 0:8]
    origin[0:4, 0:4, 0:4, 2, 0:2, 0:8]  = SOURCE
    SOURCE=np.ndarray.copy(origin[0:4, 0:4, 0:4, 1, 0:4, 8:16])
    origin[0:4, 0:4, 0:4, 1, 0:2, 8:16] = origin[0:4, 0:4, 0:4, 3, 0:2, 0:8]
    origin[0:4, 0:4, 0:4, 3, 0:2, 0:8]  = SOURCE

    for index in range(0,8192):
        location = np.where(origin==index)
        fd.write('{0} {1} {2} {3} {4} {5}\n'.format(location[0][0], location[1][0], location[2][0], location[3][0], location[4][0], location[5][0]))
        print location[0][0], location[1][0], location[2][0], location[3][0], location[4][0], location[5][0]
    fd.close

def slice2_mappings():
    x = np.array(xrange(0, 64)) # 4x4x4
    print x.shape
    y = np.reshape(x, (4,4,4), order='C' )
    #pp.pprint(y)

    # SWAP SLICES 
    SOURCE=np.ndarray.copy(y[0,0:4,0:2])
    y[0,0:4,0:2] = y[2,0:4,2:4]
    y[2,0:4,2:4] = SOURCE
    location = np.where(y==0)
    print location[0][0], location[1][0], location[2][0]
    pp.pprint(y)

slice1_mappings("sliced_mappings.txt")

#regular_mapping("regular_mapping.txt");
#line_mapping("linear_mapping.txt");
#skewed1_mapping("skewed1_mapping.txt");
#skewed2_mapping("skewed2_mapping.txt");
