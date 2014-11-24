
prefix=opt-mappings/max-8192-run4
for i in $(seq 1 8)
do
  prefix2=$prefix.$i
  iterations=$((500000 * (1 + $i)))
  echo "Starting run with $iterations iterations, output going to $prefix2"
  ./opt.py 8192 4,4,4,4,2,16 32,32,8 Y $iterations \
    $prefix2.logical.out $prefix2.net.out &> $prefix2.log & 
  disown
done
