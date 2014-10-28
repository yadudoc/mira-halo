#!/usr/bin/env python

import numpy as np
import math
data = np.loadtxt(open("regular_map.txt","r"),delimiter=" ", dtype=int)

ldata = list(data)

corners = []

for index,row in enumerate(ldata):
    #print row[0], row[1], row[2], row[3], row[4], row[5]
    flag = True
    #print row
    for col in row:
        if col == 1 or col == 2:
            flag = False
            
    if flag == True:
        print "Corner vertex found   : ",  row,  index
        corners.append(index)
        
foo=zip(corners, corners[::-1])

for x in range(0, len(foo)/2):
    ind1=foo[x][0] + 1
    ind2=foo[x][1]
    print ldata[ind1], ldata[ind2]
    (ldata[ind1], ldata[ind2]) = (ldata[ind2], ldata[ind1])
    print ldata[ind1], ldata[ind2]

for row in ldata:
    print row[0], row[1], row[2], row[3], row[4], row[5]
    
    
    
