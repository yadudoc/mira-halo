#!/usr/bin/python

import sys

TORUS_DIMS = 5

def load_mapping_file(mapping_file):
  print >> sys.stderr, "Loading mapping file: %s" % mapping_file

  failed = False

  rank2net = {}

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
        except ValueError, e:
          print >> sys.stderr, "Invalid coordinates: %s" % str(net_coords)
          bad_coord = True
          failed = True
          break

      if bad_coord:
        continue
      
      rank2net[rank] = net_coords
      rank += 1
  if failed:
    raise ValueError("Mapping file load fail b/c of previous errors")

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
