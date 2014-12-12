#!/usr/bin/python
import mapping
import sys
import random

from mapping import DEBUG
from mapping import NetworkMapping
from mapping import BGQ_NET_DIM_IS_TORUS, BGQ_NET_DIM_SAME_NODE

def usage():
  print >> sys.stderr, "Usage: opt.py <nranks> <network dims> <logical dims> <maximise distances> <nsteps> <logical mapping output> <network mapping output>\n"
  print >> sys.stderr, "    nranks: total number of MPI ranks"
  print >> sys.stderr, "    network dims: comma-separated list of network dim sizes"
  print >> sys.stderr, "    logical dims: comma-separated list of logical dim sizes"
  print >> sys.stderr, "    maximise distance: Y/N - try to maximise distance" 
  print >> sys.stderr, "    nsteps: number of annealing steps"
  print >> sys.stderr, "    logical mapping output: output file with logical coordinates of ranks"
  print >> sys.stderr, "    network mapping output: output file with network coordinates of ranks"
  sys.exit(1)

def main():
  if (len(sys.argv) != 8):
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
 
  maximise = sys.argv[4].lower()
  if maximise != 'y' and maximise != 'n':
    print >> sys.stderr, "Maximise must be y/n"
    sys.exit(1)
  maximise = maximise == 'y'

  try:
    nsteps = int(sys.argv[5])
  except ValueError, e:
    print >> sys.stderr, "Invalid nsteps: %s" % sys.argv[4]
    usage()

  logical_out = open(sys.argv[6], 'w')
  network_out = open(sys.argv[7], 'w')

  logical = mapping.compute_logical_mapping(logical_dims, nranks)

  mapping.write_mapping(logical_out, logical.rank2coord)
  logical_out.close()
  
  rank2net, _ = mapping.basic_mapping(network_dims, network_size)
  if maximise or True:
    # Start off with a bad (randomised) mapping
    random.shuffle(rank2net)
  
  network = NetworkMapping(network_dims, nranks, BGQ_NET_DIM_IS_TORUS, BGQ_NET_DIM_SAME_NODE, rank2net)

  neighbour_lists = mapping.compute_neighbour_lists(logical, False)

  anneal(logical, network, neighbour_lists, nsteps, maximise)
  
  mapping.write_mapping(network_out, network.rank2coord)
  network_out.close()

def anneal(logical, network, neighbour_lists, niters, maximise):
  curr_dist = average_distance(logical, network, neighbour_lists)
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

    nswaps = max(1, int(0.02 * temp * network.nranks))

    swaps = select_permutation(network.nranks, nswaps)

    permute(network.rank2coord, swaps)

    dist = average_distance(logical, network, neighbour_lists)

    # TODO: make direction of optimisation configurable
    accept = False



    if maximise and dist > curr_dist:
      accept = True
    elif not maximise and dist < curr_dist:
      accept = True
    else:
      p = random.random()
      
      # Number from 0.0 to 1.0 - higher is better
      if maximise:
        relative = dist / curr_dist
      else:
        relative = curr_dist / dist

      threshold = temp * (0.5 - (1.0 - relative) * 25)
      if DEBUG:
        print >> sys.stderr, "Relative: %f" % relative
        print >> sys.stderr, "Chance of acceptance: %f" % threshold
      accept = p < threshold
    
    if accept:
      curr_dist = dist
    else:
      # Undo changes to mapping
      permute_reverse(network.rank2coord, swaps)
      
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
  frac_cycle = float(total_cycles - cycle)

  cycle_temp = frac_cycle / total_cycles

  #c = 0.05
  #cycle_temp = c / (cycle_frac + c)
  
  temp = cycle_temp * (CYCLE_LENGTH - (i % CYCLE_LENGTH)) / float(CYCLE_LENGTH)

  return temp ** 3
 

def average_distance(logical, network, neighbour_lists):
  max_neighbour_dist, sum_neighbour_dist, sum_neighbour_paths, total_neighbours = \
              mapping.compute_distances(logical, network, neighbour_lists)

  return sum_neighbour_dist / float(total_neighbours)

def select_permutation(nranks, nswaps):
  p = [0] * (nswaps * 2)
  for i in xrange(nswaps):
    p[i * 2] = random.randint(0, nranks - 1)
    p[i * 2 + 1] = random.randint(0, nranks - 1)
  return p

def permute_reverse(rank2net, swaps):
  last = len(swaps) - 1
  for i in xrange(len(swaps) / 2):
    i1 = swaps[last - i * 2]
    i2 = swaps[last - i * 2 - 1]
    t = rank2net[i1]
    rank2net[i1] = rank2net[i2]
    rank2net[i2] = t

def permute(rank2net, swaps):
  for i in xrange(len(swaps) / 2):
    i1 = swaps[i * 2]
    i2 = swaps[i * 2 + 1]
    t = rank2net[i1]
    rank2net[i1] = rank2net[i2]
    rank2net[i2] = t

if __name__ == "__main__":
    main()
