#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import math
import sys
#data = np.loadtxt(open("512N_RPN2_vardata_3mappings.csv","r"),delimiter=", ", dtype=str)

data = np.loadtxt(open("results.csv","r"),delimiter=", ", dtype=str)

SearchString="12 at a time no delay"
#SearchString="12 at a time no delay"
#linear_mapping   =  [ int(row[0])*8 for row in data if row[1] ==  SearchString and row[0] == "linear_mapping"]

def mod_list(array):
    ret_list = []
    for i in xrange(23):
        total = 0
        for item in array[i*50:(i+1)*50]:
            total += float(item[2])

        avg = total/50
        #print "average: {0} = {1}".format(i, avg)
        ret_list.insert(i,array[i*50])
        ret_list[i][2] = avg
        np.append(ret_list[i], i*3)

    return ret_list

def mod_none(array):
    return array

linear_data   =  [ row for row in data if row[1] ==  SearchString and row[0] == "linear_mapping"]
random1_data  =  [ row for row in data if row[1] ==  SearchString and row[0] == "random1_mapping"]
random2_data  =  [ row for row in data if row[1] ==  SearchString and row[0] == "random2_mapping"]
random3_data  =  [ row for row in data if row[1] ==  SearchString and row[0] == "random3_mapping"]
random4_data  =  [ row for row in data if row[1] ==  SearchString and row[0] == "random4_mapping"]
regular_data  =  [ row for row in data if row[1] ==  SearchString and row[0] == "regular_mapping"]
reversed_data =  [ row for row in data if row[1] ==  SearchString and row[0] == "reversed_mapping"]
skewed1_data  =  [ row for row in data if row[1] ==  SearchString and row[0] == "skewed1_mapping"]
skewed2_data  =  [ row for row in data if row[1] ==  SearchString and row[0] == "skewed2_mapping"]
sliced_data   =  [ row for row in data if row[1] ==  SearchString and row[0] == "sliced_mappings"]
optimal_data  =  [ row for row in data if row[1] ==  SearchString and row[0] == "optimal_mapping"]
pessimal_data  =  [ row for row in data if row[1] ==  SearchString and row[0] == "worst_mapping"]
print "optimal : ", len(optimal_data)
# Use map instead ?
LOG=True
if LOG :
    linear_mapping =  [ math.log(float(row[2]),2) for row in mod_list(linear_data) ]
    random1_mapping = [ math.log(float(row[2]),2) for row in mod_list(random1_data) ]
    random2_mapping = [ math.log(float(row[2]),2) for row in mod_list(random2_data) ]
    random3_mapping = [ math.log(float(row[2]),2) for row in mod_list(random3_data) ]
    random4_mapping = [ math.log(float(row[2]),2) for row in mod_list(random4_data) ]
    regular_mapping = [ math.log(float(row[2]),2) for row in mod_list(regular_data) ]
    reversed_mapping = [ math.log(float(row[2]),2) for row in mod_list(reversed_data) ]
    skewed1_mapping =[ math.log(float(row[2]),2) for row in mod_list(skewed1_data) ]
    skewed2_mapping =[ math.log(float(row[2]),2) for row in mod_list(skewed2_data) ]
    sliced_mapping =[ math.log(float(row[2]),2) for row in mod_list(sliced_data) ]
    optimal_mapping =[ math.log(float(row[2]),2) for row in mod_list(optimal_data) ]
    pessimal_mapping =[ math.log(float(row[2]),2) for row in mod_list(pessimal_data) ]
else:
    linear_mapping =  [ float(row[2]) for row in mod_list(linear_data) ]
    random1_mapping = [ float(row[2]) for row in mod_list(random1_data) ]
    random2_mapping = [ float(row[2]) for row in mod_list(random2_data) ]
    random3_mapping = [ float(row[2]) for row in mod_list(random3_data) ]
    random4_mapping = [ float(row[2]) for row in mod_list(random4_data) ]
    regular_mapping = [ float(row[2]) for row in mod_list(regular_data) ]
    reversed_mapping = [ float(row[2]) for row in mod_list(reversed_data) ]
    skewed1_mapping =[ float(row[2]) for row in mod_list(skewed1_data) ]
    skewed2_mapping =[ float(row[2]) for row in mod_list(skewed2_data) ]
    sliced_mapping =[ float(row[2]) for row in mod_list(sliced_data) ]
    optimal_mapping =[ float(row[2]) for row in mod_list(optimal_data) ]
    pessimal_mapping =[ float(row[2]) for row in mod_list(pessimal_data) ]

#Log 2 scale
maxdist_data = [ item+3 for item in range(0,23) ]

# Takes data as log2 input
def model_f(logdata):
    data = math.pow(2,logdata)
    if data < 112 :
        return linear_mapping[0]
    elif data < 496:
        return linear_mapping[5]
    else:
        return logdata

# Measured from data
# We use the default/regular mapping sampes as baseline
baseline_data = [ float(row[2]) for row in mod_list(regular_data) ]

Ts_Immed = baseline_data[0]
Ts_Short = baseline_data[4]
Ts_Eager = baseline_data[9]
Ts_Rendz = baseline_data[9]

def no_congestion_model(logdata, Nsteps ):
    Tb = math.pow(10,6) / ( 1.8 * math.pow(2,30) )
    N  = math.pow(2, logdata)
    if N < 112 :
        Ts = Ts_Immed
    elif N < 496 :
        Ts = Ts_Short
    else:
        Ts = Ts_Rendz

    # TODO: FIX below
    return  Ts_Immed + Nsteps * N*16*Tb
    #return Nsteps * (Ts + N*16*Tb)

def node_model(logdata, Nsteps ):
    # Multiplying by 10 for all links available does not make sense here because there are 10 messages sent
    # one along every link.
    Tb = math.pow(10,6) / ( 1.8 * math.pow(2,30) )
    N  = math.pow(2, logdata)

    Const = 1
    if N < 112 :
        Ts = Ts_Immed
    elif N < 497 :
        Ts = Ts_Short
    elif N <= 4096 :
        Ts = Ts_Short # Eager
    elif N > 4096 :
        Ts = Ts_Rendz
        Const = 6.06230054379
        #Const = 7.57874801074

    return  Ts + Nsteps * N*16*Tb * Const
    #return Nsteps * (Ts + N*16*Tb)

def model_node(Nsteps):
    return [ math.log(node_model(d, Nsteps ), 2) for d in maxdist_data ]


Ndims = 5

def model_no_congestion(Nsteps):
    return [ math.log(no_congestion_model(d, Nsteps ), 2) for d in maxdist_data ]

def model_with_congestion(Nsteps):
    return [ math.log(congestion_model(d, Nsteps ), 2) for d in maxdist_data ]

def err_percent(actual,predicted):
    #return (abs(actual-predicted)/actual)*100
    return ((actual-predicted)/actual)*100

def err(experimental, model):
    #data = mod_list(experimental)
    data = [ math.pow(2,d) for d in experimental ]
    ret_list = []
    for i in range(len(data)):
        print float(data[i]), model[i], err_percent(float(data[i]), model[i])
        ret_list.append(err_percent(float(data[i]), model[i]))
    return ret_list


def plotter (kind, experimental, steps):

    #print "maxdist_data :", len(maxdist_data)
    #print "experimental :", len(experimental)

    data_axes = ['8B','16B','32B','64B','128B','256B', '512B', '1KB', '2KB', '4KB', '8KB', '16KB','32KB','64KB','128KB','256KB', '512KB', '1MB',
                 '2MB', '4MB', '8MB', '16MB','32MB']

    model         = plt.plot(maxdist_data, model_node(steps) ,  '-cd',  label="Analytical model")
    plt.setp(model, alpha=0.8, antialiased=True, linewidth=2.0)

    line           = plt.plot(maxdist_data, experimental      ,  '-ro', label=kind)
    plt.setp(line, alpha=1.0, antialiased=True,  linewidth=2.0)


    plt.xticks(maxdist_data, data_axes, rotation=45)
    plt.legend(loc=2, ncol=1, borderaxespad=2)
    #duplicate_err = plt.plot(maxdist_data, err(experimental, [no_congestion_model(d, steps) for d in maxdist_data]) , '-bs', label="Error %")
    plt.ylabel("Time to completion in us (log2 scale)")
    plt.xlabel("Data per Halo exchange in Bytes(log2 scale)")

    err_plot       = plt.twinx()

    rects1 = plt.bar(maxdist_data,
                     err(experimental, [node_model(d, steps) for d in maxdist_data]),
                     0.35,
                     alpha=0.2,
                     color='r',
                     label='Error %')

    plt.ylim(-50,50)
    errors =  err(experimental, [node_model(d, steps) for d in maxdist_data])
    avg_error = sum( [abs(i) for i in errors ] ) / len(errors)
    print "ERRORS {0} {1} {2} {3}".format(kind, min(errors), max(errors), avg_error)
    plt.title('Time to complete halo exchange - 512 Nodes, RPN 16, 3D application matrix')

    err_plot.set_ylabel('Error %')
    plt.show()


def mappings_plotter ():
    #line           = plt.plot(maxdist_data, experimental , '--r*', label=kind)
    plt.ylabel("Time to completion in us (log2 scale)")
    plt.xlabel("Data per Halo exchange in Bytes(log2 scale)")

    data_axes = ['8B','16B','32B','64B','128B','256B', '512B', '1KB', '2KB', '4KB', '8KB', '16KB','32KB','64KB','128KB','256KB', '512KB', '1MB',
                 '2MB', '4MB', '8MB', '16MB','32MB']

    line_optimal   = plt.plot(maxdist_data, optimal_mapping , '-gd', label="Optimal mapping")
    plt.setp(line_optimal, alpha=0.8, antialiased=True, linewidth=2.0)
    line_regular   = plt.plot(maxdist_data, regular_mapping , '-bd', label="Regular mapping")
    plt.setp(line_regular, alpha=0.8, antialiased=True, linewidth=2.0)
    line_skewed1   = plt.plot(maxdist_data, skewed1_mapping , '--c*', label="Skewed mapping1")
    plt.setp(line_skewed1, alpha=0.8, antialiased=True,  linewidth=2.0)
    #line_skewed2   = plt.plot(maxdist_data, skewed2_mapping , '--gv', label="Skewed mapping2")
    line_linear    = plt.plot(maxdist_data, linear_mapping ,  '--y*', label="Linear mapping")
    #line_reversed  = plt.plot(maxdist_data, reversed_mapping , '--m^', label="Reversed mapping")
    #line_rand4     = plt.plot(maxdist_data, random2_mapping , '-bp', label="Random mapping4")
    #plt.setp(line_rand4, alpha=1.0, antialiased=True,  linewidth=2.0)
    #line_rand3     = plt.plot(maxdist_data, random2_mapping , '-cd', label="Random mapping3")
    #plt.setp(line_rand3, alpha=1.0, antialiased=True,  linewidth=2.0, marker='+')
    line_rand2     = plt.plot(maxdist_data, random2_mapping , '-.rs', label="Random mapping2")
    plt.setp(line_rand2, alpha=1.0, antialiased=True,  linewidth=2.0)
    line_rand1     = plt.plot(maxdist_data, random1_mapping , '--ko', label="Random mapping1")
    plt.setp(line_rand1, alpha=1.0, antialiased=True,  linewidth=2.0)
    #line_worst     = plt.plot(maxdist_data, worst_mapping , '-rd', label="Pessimal mapping")
    #plt.setp(line_worst, alpha=1.0, antialiased=True,  linewidth=2.0)
    #err_plot.set_xlabel('time (s)')
    # Make the y-axis label and tick labels match the line color.
    plt.xticks(maxdist_data, data_axes, rotation=45)
    plt.title('Time to complete halo exchange - 512 Nodes, RPN 16, 3D application matrix')
    #plt.legend(bbox_to_anchor=(0., 1.02, 1., .202), loc=3, ncol=2, mode="expand", borderaxespad=0.5)
    plt.legend(loc=2, ncol=1, borderaxespad=2)
    plt.show()

#print  [ float(row[2]) for row in mod_list(optimal_data) ]
#print  [ float(row[2]) for row in mod_list(random1_data) ]

def calculate_alpha():
    regular = [ float(row[2]) for row in mod_list(regular_data) ]
    model_res = model_node(float(regular_data[0][3]))
    print model_res
    print regular

    print "{0: <16} {1: <16} {2: <16}".format("model", "data", "dev")
    for i in range(10,23):
        print "{0: <16} {1: <16} {2: <16}".format( math.pow(2,model_res[i]), regular[i],
                                                   regular[i] / math.pow(2,model_res[i]) )

    devs=[ d/math.pow(2,m) for (m,d) in zip(model_res[9:], regular[9:]) ]
    average = sum(devs)/len(devs)
    print "devs    : ", devs
    print "average : ", average

calculate_alpha()

#mappings_plotter()
plotter("Optimal mapping", optimal_mapping, float(optimal_data[0][3]))
plotter("Regular mapping", regular_mapping, float(regular_data[0][3]))
plotter("Linear mapping", linear_mapping, float(linear_data[0][3]))
plotter("Reversed mapping", reversed_mapping, float(reversed_data[0][3]))

plotter("Skewed regular", skewed1_mapping, float(skewed1_data[0][3]))
plotter("Skewed reversed", skewed2_mapping, float(skewed2_data[0][3]))
plotter("Random mapping", random1_mapping, float(random1_data[0][3]))
plotter("Pessimal mapping", pessimal_mapping, float(pessimal_data[0][3]))


#plotter("Random mapping 2", random2_mapping, float(random2_data[0][3]))
#plotter("Random mapping 3", random3_mapping, float(random3_data[0][3]))
#plotter("Random mapping 4", random4_mapping, float(random4_data[0][3]))
#plotter("Reversed mapping", reversed_mapping, float(reversed_data[0][3]))



#line_linear    = plt.plot(maxdist_data, linear_mapping ,  '--m*',   label="Linear mapping")
#line_reversed  = plt.plot(maxdist_data, reversed_mapping, '--b*', label="Reversed mapping")
#line_rand1     = plt.plot(maxdist_data, random1_mapping , '--ro', label="Random mapping1")
#line_rand2     = plt.plot(maxdist_data, random1_mapping , '--bo', label="Random mapping2")
#line_rand3     = plt.plot(maxdist_data, random1_mapping , '--yo', label="Random mapping3")

#plt.title('Time to complete halo exchange Analytical model with no-congestion (' + SearchString + ')')
#plt.title('Time to complete halo exchange - 512 Nodes, RPN 16, 5D application matrix(' + SearchString + ')')
exit()
