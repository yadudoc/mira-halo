#!/usr/bin/env python
import itertools
import pprint
import numpy as np

pp = pprint.PrettyPrinter(indent=4,depth=6)

A_dim, B_dim, C_dim, D_dim, E_dim, T_dim = [4,4,4,4,2,16]


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

def boxing_mapping(ofile):
    fd = open(ofile, 'w');
    x = np.array(xrange(0, 8192)) # 4x4x4x4                                                                                                                                                   
    print x.shape
    #origin = np.reshape(x, (4,4,4,4,2,16), order='C' )
    origin = np.reshape(x, (32, 32, 8), order='C')

    '''
    App dimensions are 32x32x8
    Phy dimensions are 4x4x4x4x2x16
    '''
    for A in range(0, 32, 4):            # INCR 4
        for B in range(0, 2):        # INCR 2
            for C in range(0, 2):     # INCR 2
                #print origin[A,B,C],  " :  ", A, B, C
                a = A%16 # E = A/16 
                print a/4, (B/2)%4, int(C/2), int(B/8), int(A/16), ( (a%4 * 4) + ( B%2 * 2) + (C%2) )
    #pp.pprint(y)
    #pp.pprint(origin[0,0:4,0:4,0:4,0:2,0:8])
    
    '''
    for index in range(0,8192):
        location = np.where(origin==index)
        fd.write('{0} {1} {2} {3} {4} {5}\n'.format(location[0][0], location[1][0], location[2][0], location[3][0], location[4][0], location[5][0]))
        print location[0][0], location[1][0], location[2][0], location[3][0], location[4][0], location[5][0]
    fd.close
    '''

boxing_mapping("foo");

#regular_mapping("regular_mapping.txt");
#line_mapping("linear_mapping.txt");
#skewed1_mapping("skewed1_mapping.txt");
#skewed2_mapping("skewed2_mapping.txt");
