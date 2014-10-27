#!/usr/bin/python

import os
import sys

BGQ_NET_DIMS = 5
# TODO: should load somehow
net_dim_is_torus = [ True ] * (BGQ_NET_DIMS + 1)
# TODO: right?
BGQ_NET_DIM_SAME_NODE = [ False, False, False, False, False, True ]

DEBUG = False
PAIRWISE_DEBUG = False

if os.getenv("DEBUG") is not None:
  DEBUG = True

if os.getenv("PAIRWISE_DEBUG") is not None:
  PAIRWISE_DEBUG = True

def load_mapping_file(mapping_file):
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

  return rank2net, net_dims

def compute_logical_mapping(logical_dims, nranks):
  rank2log = {}
  log2rank = {}


  for rank in range(nranks):
    if rank == 0:
      coords = [0] * len(logical_dims)
    else:
      # TODO: what order is used for dimensions
      # For now, increment last first
      dim = len(coords) - 1

      while dim >= 0:
        coords[dim] = (coords[dim] + 1) % logical_dims[dim]
        if coords[dim] != 0:
          break
        dim -= 1
    rank2log[rank] = tuple(coords)
    log2rank[tuple(coords)] = rank

  return rank2log, log2rank

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

def coord_dist(coord1, coord2, dims, wrap_dims, ignore_dims):
  """
  Compute manhattan distance between coordinates
  wrap_dims: whether dims wrap
  ignore_dims: if true, don't count towards distance
  """
  dist = 0.0
  assert len(coord1) == len(dims)
  assert len(coord2) == len(dims)

  assert len(dims) == len(dims)
  assert len(wrap_dims) == len(dims)
  assert len(ignore_dims) == len(dims)

  # Ignore last dimension (core)
  for dim in range(len(dims)):
    if not ignore_dims[dim]:
      dim_dist = abs(coord1[dim] - coord2[dim])

      if wrap_dims[dim]:
        # compute wraparound distance, take minimum
        if coord1[dim] > coord2[dim]:
          wrap_dist = dims[dim] - coord1[dim] + coord2[dim]
        else:
          wrap_dist = dims[dim] - coord2[dim] + coord1[dim]

        dim_dist = min(dim_dist, wrap_dist)

      dist += dim_dist

  return dist

def usage():
  print >> sys.stderr, "Usage: mapping.py <nranks> <mapping file> <dims>\n"
  print >> sys.stderr, "    nranks: total number of MPI ranks"
  print >> sys.stderr, "    mapping file: BQ/Q Cobalt mapping file for physical layout"
  print >> sys.stderr, "    dims: comma-separated list of logical dim sizes"
  sys.exit(1)

if (len(sys.argv) != 4):
  usage()

try:
  nranks = int(sys.argv[1])
except ValueError, e:
  print >> sys.stderr, "Invalid nranks: %s" % sys.argv[1]
  usage()

if DEBUG:
  print >> sys.stderr, "nranks: %d" % nranks

rank2net, net_dims = load_mapping_file(sys.argv[2])

if len(rank2net) != nranks:
  print >> sys.stderr, ("Number of mapped ranks from mapping file %d " + \
                        "doesn't match nranks %d") % (len(rank2net), nranks)
  sys.exit(1)

logical_dims = sys.argv[3].split(",")
logical_size = 1
for i in range(len(logical_dims)):
  try:
    logical_dims[i] = int(logical_dims[i])
    logical_size *= logical_dims[i]
  except ValueError, e:
    print >> sys.stderr, "Invalid dimension: %s" % logical_dims[i]
    usage()

if DEBUG:
  print >> sys.stderr, "Logical dims: %s size: %d" % (
          str(tuple(logical_dims)), logical_size)

if logical_size != nranks:
  print >> sys.stderr, "Logical size %d doesn't match nranks %d" % (
                        logical_size, nranks)
  sys.exit(1)

rank2log, log2rank = compute_logical_mapping(logical_dims, nranks)

if DEBUG:
  print "Rank2Net: %s" % str(rank2net)
  print "Rank2Log: %s" % str(rank2log)
  print "Log2Rank: %s" % str(log2rank)

if PAIRWISE_DEBUG:
  for rank1 in range(nranks):
    for rank2 in range(nranks):
      dist = coord_dist(rank2net[rank1], rank2net[rank2], net_dims,
                      net_dim_is_torus, BGQ_NET_DIM_SAME_NODE)
      print "%d <-> %d distance: %f" % (rank1, rank2, dist)

max_neighbour_dist = 0.0
sum_neighbour_dist = 0.0
total_neighbours = 0

for rank in range(nranks):
  ns = []
  cs = rank2log[rank]
  for ncs in neighbours(cs, logical_dims, [True] * len(logical_dims)):
    n_rank = log2rank[ncs]
    assert rank != n_rank
    dist = coord_dist(rank2net[rank], rank2net[n_rank], net_dims,
                    net_dim_is_torus, BGQ_NET_DIM_SAME_NODE)
    ns.append((n_rank, ncs, dist))

    max_neighbour_dist = max(max_neighbour_dist, dist)
    sum_neighbour_dist += dist
    total_neighbours += 1

  if DEBUG:
    print "%d %s neighbours: %s" % (rank, str(cs), str(ns))

print "Max Neighbour Distance: %f" % max_neighbour_dist
print "Sum of Neighbour Distances: %f" % (sum_neighbour_dist)
print "Average Neighbour Distance: %f" % (
      sum_neighbour_dist / total_neighbours)
print "Total Neighbours: %d" % total_neighbours
