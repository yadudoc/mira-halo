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

      rank2net[rank] = net_coords
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

print >> sys.stderr, "Rank2Net: %s" % str(rank2net)

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

logical_map = {}
