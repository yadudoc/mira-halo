#!/usr/bin/python

import os
import sys

BGQ_NET_DIMS = 5
BGQ_NET_DIM_IS_TORUS = [ True ] * (BGQ_NET_DIMS + 1)
# Count ABCD dimensions, ignore E nodeboard link, and T core dimension
BGQ_NET_DIM_SAME_NODE = [ False, False, False, False, True, True ]

DEBUG = False
PAIRWISE_DEBUG = False

if os.getenv("DEBUG") is not None:
  DEBUG = True

if os.getenv("PAIRWISE_DEBUG") is not None:
  PAIRWISE_DEBUG = True


class LogicalMapping:
  def __init__(self, dims, nranks, rank2coord, coord2rank):
    self.dims = dims
    self.nranks = nranks
    self.rank2coord = rank2coord
    self.coord2rank = coord2rank
    
class NetworkMapping:
  def __init__(self, dims, nranks, wrap_dims, same_node_dims, rank2coord):
    self.dims = dims
    self.nranks = nranks
    self.wrap_dims = wrap_dims
    self.same_node_dims = same_node_dims
    self.rank2coord = rank2coord
    self.dist_include_dims = self.calc_include_dims(dims, same_node_dims)

  def calc_include_dims(self, dims, same_node_dims):
    d = []
    for i in range(len(dims)):
      if not same_node_dims[i]:
        d.append(i)
    return d

def load_mapping_file(mapping_file, wrap_dims, same_node_dims):
  """
  Load and do some validation of mapping
  return (rank to coordinate mapping, dimensions of network)
  """
  if DEBUG:
    print >> sys.stderr, "Loading mapping file: %s" % mapping_file

  failed = False

  rank2net = {}
  mapped_coords = set()

  max_coords = [0] * (BGQ_NET_DIMS + 1)

  rank = 0
  with open(mapping_file, "r") as mf:
    for map_line in mf:
      net_coords = map_line.split()
      if (len(net_coords) != BGQ_NET_DIMS + 1):
        print >> sys.stderr, "Invalid number of dimensions in: %s" % \
                             str(net_coords)
        continue

      bad_coord = False
      for i in range(len(net_coords)):
        try:
          net_coords[i] = int(net_coords[i])
          if net_coords[i] < 0:
            print >> sys.stderr, "Invalid coordinate: %d" % net_coords[i]
            bad_coord = True
            failed = True
            break

          max_coords[i] = max(max_coords[i], net_coords[i])
        except ValueError, e:
          print >> sys.stderr, "Invalid coordinates: %s" % str(net_coords)
          bad_coord = True
          failed = True
          break

      if bad_coord:
        continue

      if tuple(net_coords) in mapped_coords:
        print >> sys.stderr, "Duplicate coordinates: %s" % str(net_coords)
        failed = True
        continue
      mapped_coords.add(tuple(net_coords))

      rank2net[rank] = tuple(net_coords)
      rank += 1

  if not failed:
    exp_ranks = 1
    for max_coord in max_coords:
      exp_ranks *= (max_coord + 1)

    # Check if contiguous
    if rank != exp_ranks:
      print >> sys.stderr, "Gaps in mapping: product of dim sizes was %d but only %d mapping lines provided" % (exp_ranks, rank)
      failed = True

  if failed:
      print >> sys.stderr, ("Mapping file load fail b/c of previous errors")
      sys.exit(1)

  net_dims = []
  for max_coord in max_coords:
    net_dims.append(max_coord + 1)

  return NetworkMapping(net_dims, exp_ranks, wrap_dims, same_node_dims, rank2net)

def write_mapping(out, rank2coord):
  for rank, coord in enumerate(rank2coord):
    out.write(' '.join(map(str, coord)) + "\n")

def dims_from_string(dim_str):
  """
  returns nranks, dimension size list
  """
  dims = dim_str.split(",")
  size = 1
  for i in range(len(dims)):
    try:
      dims[i] = int(dims[i])
      size *= dims[i]
    except ValueError, e:
      raise ValueError("Invalid dimension: %s" % dims[i])

  return size, dims

def basic_mapping(dims, nranks):
  rank2coord = [None] * nranks
  coord2rank = {}

  for rank in range(nranks):
    if rank == 0:
      coords = [0] * len(dims)
    else:
      # TODO: what order is used for dimensions
      # For now, increment last first
      dim = len(coords) - 1

      while dim >= 0:
        coords[dim] = (coords[dim] + 1) % dims[dim]
        if coords[dim] != 0:
          break
        dim -= 1
    rank2coord[rank] = tuple(coords)
    coord2rank[tuple(coords)] = rank

  
  return rank2coord, coord2rank

def compute_logical_mapping(logical_dims, nranks):
  rank2log, log2rank = basic_mapping(logical_dims, nranks)

  return LogicalMapping(logical_dims, nranks, rank2log, log2rank)

def compute_neighbour_lists(logical, bothways):
  neighbour_lists = [None] * logical.nranks
  for rank in xrange(logical.nranks):
    neighbour_ranks = []
    cs = logical.rank2coord[rank]
    for ncs in neighbours(cs, logical.dims, [True] * len(logical.dims)):
      n_rank = logical.coord2rank[ncs]
      if bothways or n_rank < rank:
        neighbour_ranks.append(n_rank)

    neighbour_lists[rank] = neighbour_ranks

  return neighbour_lists

def neighbours(coords, dims, wrap_dims):
  """
  Compute neighbours of coordinate.  Returns list of coordinates.
  coords: coordinates of rank
  dims: dimension sizes
  wrap_dims: list of which dimensions wrap around
  """
  result = []
  assert len(coords) == len(dims)
  assert len(dims) == len(wrap_dims)

  for dim in range(len(dims)):
    coord = coords[dim]

    if (dims[dim] > 2):
      # Two potential neighbours in this dimension
      incs = [-1, 1]
    elif (dims[dim] == 2):
      # One neighbour in this dimension
      incs = [1]
    else:
      assert dims[dim] == 1
      # No neighbours in this dimension
      incs = []

    for inc in incs:
      neighbour_coord = (coord + inc)
      if wrap_dims[dim]:
        neighbour_coord = neighbour_coord % dims[dim]
        if neighbour_coord == coord:
          continue
      elif neighbour_coord < 0 or neighbour_coord >= dims[dim]:
        # No wrapping
        continue

      neighbour = list(coords)
      neighbour[dim] = neighbour_coord
      result.append(tuple(neighbour))

  return result

def net_coord_dist(coord1, coord2, network):
  return coord_dist(coord1, coord2, network.dims, network.wrap_dims, \
                    network.dist_include_dims)

def coord_dist(coord1, coord2, dims, wrap_dims, dist_include_dims):
  """
  Compute manhattan distance between coordinates
  wrap_dims: whether dims wrap
  dist_include_dims: list of the dim indices to include 
  """
  dist = 0.0
  #assert len(coord1) == len(dims)
  #assert len(coord2) == len(dims)

  #assert len(dims) == len(dims)
  #assert len(wrap_dims) == len(dims)
  #assert len(ignore_dims) == len(dims)

  # Ignore last dimension (core)
  for dim in dist_include_dims:
    c1 = coord1[dim]
    c2 = coord2[dim]
    dim_dist = c1 - c2
    
    if dim_dist == 0:
      continue
    elif dim_dist < 0:
      dim_dist = -dim_dist

    if wrap_dims[dim]:
      # compute wraparound distance, take minimum
      wrap_dist = dims[dim] - dim_dist

      dim_dist = dim_dist if dim_dist < wrap_dist else wrap_dist

    dist += dim_dist

  return dist

def compute_distances(logical, network, neighbour_lists):
  #assert logical.nranks == network.nranks

  max_neighbour_dist = 0.0
  sum_neighbour_dist = 0.0
  total_neighbours = 0
  
  net_dims = network.dims
  net_wrap_dims = network.wrap_dims
  net_include_dims = network.dist_include_dims
  net_rank2coord = network.rank2coord

  for rank in xrange(logical.nranks):
    #ns = []
    coords = net_rank2coord[rank]
    for n_rank in neighbour_lists[rank]:
      #assert rank != n_rank
      dist = coord_dist(coords, net_rank2coord[n_rank], net_dims,
                        net_wrap_dims, net_include_dims)
                      
      #ns.append((n_rank, ncs, dist))

      max_neighbour_dist = max(max_neighbour_dist, dist)
      sum_neighbour_dist += dist
      total_neighbours += 1

    #if DEBUG and False:
    #  print "%d %s neighbours: %s" % (rank, str(cs), str(ns))

  return max_neighbour_dist, sum_neighbour_dist, total_neighbours


def usage():
  print >> sys.stderr, "Usage: mapping.py <nranks> <mapping file> <dims>\n"
  print >> sys.stderr, "    nranks: total number of MPI ranks"
  print >> sys.stderr, "    mapping file: BQ/Q Cobalt mapping file for physical layout"
  print >> sys.stderr, "    dims: comma-separated list of logical dim sizes"
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

  # TODO: bgq parameters are hardcoded here
  network = load_mapping_file(sys.argv[2], BGQ_NET_DIM_IS_TORUS, BGQ_NET_DIM_SAME_NODE)

  if network.nranks != nranks:
    print >> sys.stderr, ("Number of mapped ranks from mapping file %d " + \
                          "doesn't match nranks %d") % (network.nranks, nranks)
    sys.exit(1)

  try: 
    logical_size, logical_dims = dims_from_string(sys.argv[3])
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

  logical = compute_logical_mapping(logical_dims, nranks)

  if DEBUG:
    print "Rank2Net: %s" % str(network.rank2coord)
    print "Rank2Log: %s" % str(logical.rank2coord)
    print "Log2Rank: %s" % str(logical.coord2rank)

  if PAIRWISE_DEBUG:
    for rank1 in range(nranks):
      for rank2 in range(nranks):
        dist = net_coord_dist(network.rank2coord[rank1], network.rank2coord[rank2], network)
        print "%d <-> %d distance: %f" % (rank1, rank2, dist)

  neighbour_lists = compute_neighbour_lists(logical, False)

  max_neighbour_dist, sum_neighbour_dist, total_neighbours = \
                            compute_distances(logical, network, neighbour_lists)

  print "Max Neighbour Distance: %f" % max_neighbour_dist
  print "Sum of Neighbour Distances: %f" % (sum_neighbour_dist)
  print "Average Neighbour Distance: %f" % (
        sum_neighbour_dist / total_neighbours)
  print "Total Neighbours: %d" % total_neighbours

if __name__ == "__main__":
    main()
