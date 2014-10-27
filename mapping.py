#!/usr/bin/python

import sys

TORUS_DIMS = 5

def load_mapping_file(mapping_file):
  """
  Load and do some validation of mapping
  """
  print >> sys.stderr, "Loading mapping file: %s" % mapping_file

  failed = False

  rank2net = {}
  mapped_coords = set()

  max_coords = [0] * (TORUS_DIMS + 1)

  rank = 0
  with open(mapping_file, "r") as mf:
    for map_line in mf:
      net_coords = map_line.split()
      if (len(net_coords) != TORUS_DIMS + 1):
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

  return rank2net

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

print >> sys.stderr, "nranks: %d" % nranks

rank2net = load_mapping_file(sys.argv[2])

if len(rank2net) != nranks:
  print >> sys.stderr, ("Number of mapped ranks from mapping file %d " + \
                        "doesn't match nranks %d") % (len(rank2net), nranks)

logical_dims = sys.argv[3].split(",")
logical_size = 1
for i in range(len(logical_dims)):
  try:
    logical_dims[i] = int(logical_dims[i])
    logical_size *= logical_dims[i]
  except ValueError, e:
    print >> sys.stderr, "Invalid dimension: %s" % logical_dims[i]
    usage()

print >> sys.stderr, "Logical dims: %s size: %d" % (
        str(tuple(logical_dims)), logical_size)

if logical_size != nranks:
  print >> sys.stderr, "Logical size %d doesn't match nranks %d" % (
                        logical_size, nranks)
  sys.exit(1)

rank2log, log2rank = compute_logical_mapping(logical_dims, nranks)
print >> sys.stderr, "Rank2Net: %s" % str(rank2net)
print >> sys.stderr, "Rank2Log: %s" % str(rank2log)
print >> sys.stderr, "Log2Rank: %s" % str(log2rank)

for log in log2rank:
  ns = neighbours(log, logical_dims, [True] * len(logical_dims))
  print >> sys.stderr, "%s neighbours: %s" % (str(log), str(ns))

logical_map = {}
