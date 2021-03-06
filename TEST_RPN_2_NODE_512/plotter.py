#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import math
import sys
data = np.loadtxt(open("512N_RPN2_vardata_3mappings.csv","r"),delimiter=", ", dtype=str)

#print sys.argv[1]
#print data

#nodes  =  [ math.log(int(row[0]),2) for row in data if row[2] ==  "Sendrecv no delay"]
#rtime  =  [ float(row[2]) for row in data if row[2] ==  "Sendrecv no delay"]

SearchString="Isend-Irecv wt delay"
#if len(sys.argv) > 0:
#    SearchString=str(sys.argv[1])

maxdist_data  =  [ math.log(int(row[0])*8,2) for row in data if row[2] ==  SearchString and row[1] == "MAXDIST"]

maxdist_time  =  [ math.log(float(row[3]),2) for row in data if row[2] ==  SearchString and row[1] == "MAXDIST"]
regular_time  =  [ math.log(float(row[3]),2) for row in data if row[2] ==  SearchString and row[1] == "REGULAR"]
skewed_time   =  [ math.log(float(row[3]),2) for row in data if row[2] ==  SearchString and row[1] == "SKEWED"]

percent_reg_max  = [ 100*((y-x)/x) for (x,y) in zip(regular_time, maxdist_time) ]
percent_reg_skew = [ 100*((y-x)/x) for (x,y) in zip(regular_time, skewed_time) ]

'''
line_reg = plt.plot(maxdist_data, percent_reg_max,  'b*', label="Regular vs MaxDist % difference")
line_reg = plt.plot(maxdist_data, percent_reg_max,  'b', label="Regular vs MaxDist % difference")
line_reg = plt.plot(maxdist_data, percent_reg_skew, 'g*', label="Regular vs Skewed % difference")
line_reg = plt.plot(maxdist_data, percent_reg_skew, 'g', label="Regular vs Skewed % difference")
line_reg = plt.plot(maxdist_data, [ 0 for i in percent_reg_skew], 'r', label="Regular vs Skewed % difference")
'''

line_regular = plt.plot(maxdist_data, regular_time, '--g^', label="Regular mapping")
#line_regular = plt.plot(maxdist_data, regular_time, 'g', label="Regular mapping")
line_skewed  = plt.plot(maxdist_data, skewed_time,  '--b*', label="Skewed mapping")
#line_skewed  = plt.plot(maxdist_data, skewed_time,  'b', label="Skewed mapping")
line_maxdist = plt.plot(maxdist_data, maxdist_time, '--ro', label="Maxdist mapping")
#line_maxdist = plt.plot(maxdist_data, maxdist_time, 'r', label="Maxdist mapping")


plt.title('Time to complete halo exchange with 3 different mappings (' + SearchString + ')')
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.5)
plt.xlabel('Data in bytes (log2 scale)')
plt.ylabel('time to completion in us')
#plt.ylabel('% difference between mappings')
plt.show()

print maxdist_data
print rtime
exit()
print nodes
print rtime
plt.plot(nodes, rtime, 'rs', nodes, rtime, 'r')
plt.xlabel('nodes(log2)')
plt.ylabel('time in us')
plt.show()
