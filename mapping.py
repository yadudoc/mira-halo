#!/usr/bin/python

import sys

TORUS_DIMS = 5

mapping_file = sys.argv[1]

print >> sys.stderr, "Mapping file: %s" % mapping_file

logical_map = {}
rank2net = {}

failed = False

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
  print >> sys.stderr, "Failing b/c of previous errors"

print >> sys.stderr, "Rank2Net: %s" % str(rank2net)
