#!/usr/bin/env python
import itertools
import pprint
import numpy as np

pp = pprint.PrettyPrinter(indent=4,depth=6)

A_dim, B_dim, C_dim, D_dim, E_dim, T_dim = [4,4,4,4,2,16]

def boxing_mapping(ofile):
    fd = open(ofile, 'w');
    x = np.array(xrange(0, 8192)) # 4x4x4x4
    #print x.shape
    #origin = np.reshape(x, (4,4,4,4,2,16), order='C' )
    origin = np.reshape(x, (8,8,8,8,2), order='C')

    '''
    App dimensions are 8x8x8x8x2
    Phy dimensions are 4x4x4x4x2x16
    '''
    target = {}
    for E in range(0,2):
        for A in range(0, 8, 2):            # INCR 4
            for B in range(0, 8, 2):         # INCR 2
                for C in range(0, 8, 2):        # INCR 2
                    for D in range(0, 8, 2):

                        a = A/2
                        b = B/2
                        c = C/2
                        d = D/2
                        e = E
                        #print a, b, c, d, E
                        slice = origin[A:A+2, B:B+2, C:C+2, D:D+2, E]
                        #print "Slice for {0} {1} {2} {3} {4}:  {5}".format(A,B,C,D,E,slice)
                        items = np.reshape(slice, (16), order='C')
                        for core,item in enumerate(items):
                            target[item] = "{0} {1} {2} {3} {4} {5}".format(a,b,c,d,e,core)
                            #print "target[{0}] = {1}".format(item, target[item])

    for index in range(0,8192):
        fd.write('{0}\n'.format(target[index]))
        #fd.write('{0} {1} {2} {3} {4} {5}\n'.format(location[0][0], location[1][0], location[2][0], location[3][0], location[4][0], location[5][0]))
        #print location[0][0], location[1][0], location[2][0], location[3][0], location[4][0], location[5][0]
    fd.close

    return


boxing_mapping("box.txt");

#regular_mapping("regular_mapping.txt");
#line_mapping("linear_mapping.txt");
#skewed1_mapping("skewed1_mapping.txt");
#skewed2_mapping("skewed2_mapping.txt");
