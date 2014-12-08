for i in $(seq 7 8)
do
  ./opt.py 8192 4,4,4,4,2,16 32,32,8 Y 1000000 run3-log.$i.out run3-net.$i.out &> /var/tmp/tga/run3.$i.out & 
  disown
done
