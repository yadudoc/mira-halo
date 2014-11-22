#!/usr/bin/python
import mapping
import sys
import random

from mapping import DEBUG
from mapping import NetworkMapping
from mapping import BGQ_NET_DIM_IS_TORUS, BGQ_NET_DIM_SAME_NODE

def usage():
  print >> sys.stderr, "Usage: opt.py <nranks> <network dims> <logical dims>\n"
  print >> sys.stderr, "    nranks: total number of MPI ranks"
  print >> sys.stderr, "    logical dims: comma-separated list of logical dim sizes"
  print >> sys.stderr, "    network dims: comma-separated list of network dim sizes"
  sys.exit(1)

def main():
  if (len(sys.argv) != 4):
    usage()

  try:
    nranks = int(sys.argv[1])
  except ValueError, e:
    print >> sys.stderr, "Invalid nranks: %s" % sys.argv[1]
    usage()

  if DEBUG:
    print >> sys.stderr, "nranks: %d" % nranks

  try: 
    network_size, network_dims = mapping.dims_from_string(sys.argv[2])
  except ValueError, e:
    print >> sys.stderr, e.message
    usage()
  
  if DEBUG:
    print >> sys.stderr, "Network dims: %s size: %d" % (
            str(tuple(network_dims)), network_size)

  if network_size != nranks:
    print >> sys.stderr, ("Network size %d doesn't match nranks %d") % (network_size, nranks)
    sys.exit(1)

  try: 
    logical_size, logical_dims = mapping.dims_from_string(sys.argv[3])
  except ValueError, e:
    print >> sys.stderr, e.message
    usage()

  if DEBUG:
    print >> sys.stderr, "Logical dims: %s size: %d" % (
            str(tuple(logical_dims)), logical_size)

  if logical_size != nranks:
    print >> sys.stderr, "Logical size %d doesn't match nranks %d" % (
                          logical_size, nranks)
    sys.exit(1)

  logical = mapping.compute_logical_mapping(logical_dims, nranks)
  
  rank2net = random_rank2net(network_size, network_dims)
  
  network = NetworkMapping(network_dims, nranks, BGQ_NET_DIM_IS_TORUS, BGQ_NET_DIM_SAME_NODE, rank2net)


  anneal(logical, network, 100000)


def anneal(logical, network, niters):
  curr_dist = average_distance(logical, network)
  best_dist = curr_dist

  print "Initial average distance: %f" % (curr_dist)

  n = 1000
  for i in xrange(niters):
    temp = calc_temp(i, niters)
    if DEBUG:
      print >> sys.stderr, "Annealing iteration %i/%i T = %f" % (i, niters, temp)
    
    if i % 100 == 0:
      print >> sys.stderr, "Annealing iteration %i/%i dist = %f T = %f" % (
                            i, niters, curr_dist, temp)

    curr_rank2net = network.rank2coord
    
    nswaps = max(1, int(10 * temp))

    new_rank2net = network.rank2coord[:]

    permute(new_rank2net, nswaps)

    network.rank2coord = new_rank2net

    dist = average_distance(logical, network)

    # TODO: make direction of optimisation configurable
    accept = False

    if dist > curr_dist:
      accept = True
    else:
      p = random.random()
      
      # Number from 0.0 to 1.0 - higher is better
      relative = dist / curr_dist

      threshold = temp * (1.0 - (1.0 - relative) * 10)
      if DEBUG:
        print >> sys.stderr, "Relative: %f" % relative
        print >> sys.stderr, "Chance of acceptance: %f" % threshold
      accept = p < threshold
    
    if accept:
      curr_dist = dist
    else:
      # Restore copied mapping
      network.rank2coord = curr_rank2net
      
    if DEBUG:
      print >> sys.stderr, "Swapped %d, average distance = %f" % (nswaps, dist)

  print "Final distance: %f" % curr_dist


CYCLE_LENGTH = 25

def calc_temp(i, n):
  """
  Return number between 0 and 1.0
  """

  cycle = i / CYCLE_LENGTH
  total_cycles = (n - 1) / CYCLE_LENGTH + 1

  cycle_temp = 0.5 * float(total_cycles - cycle) / total_cycles
  
  return cycle_temp + cycle_temp * (CYCLE_LENGTH - (i % CYCLE_LENGTH)) / float(CYCLE_LENGTH)
 

def average_distance(logical, network):
  max_neighbour_dist, sum_neighbour_dist, total_neighbours = \
                            mapping.compute_distances(logical, network)

  return sum_neighbour_dist / float(total_neighbours)

def random_rank2net(network_size, network_dims):
  rank2net, _ = mapping.basic_mapping(network_dims, network_size)
  
  random.shuffle(rank2net)

  return rank2net

def permute(rank2net, nswaps):
  for i in xrange(nswaps):
    i1 = random.randint(0, len(rank2net) - 1)
    i2 = random.randint(0, len(rank2net) - 1)
    t = rank2net[i1]
    rank2net[i1] = rank2net[i2]
    rank2net[i2] = t

if __name__ == "__main__":
    main()
