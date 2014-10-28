mmps_array=("mmps_5D_1" "mmps_5D_2" "mmps_5D_4" "mmps_5D_8" "mmps_5D_16" "mmps_5D_32" "mmps_5D_64" "mmps_5D_128" \
    "mmps_5D_256" "mmps_5D_512" "mmps_5D_1024" "mmps_5D_2048" "mmps_5D_4096" "mmps_5D_8192" "mmps_5D_10240" "mmps_5D_16384" \
    "mmps_5D_24576" "mmps_5D_32768" "mmps_5D_65536" "mmps_5D_131072" "mmps_5D_262144" "mmps_5D_524288" "mmps_5D_1048576" \
    "mmps_5D_2097152" "mmps_5D_4194304" "mmps_5D_8388608")

splitfiles=($(ls TEST*))

for i in $(seq 0 1 $(( ${#mmps_array[*]} - 1 )) )
do
    split -l 120 ${splitfiles[$i]} -d ${splitfiles[$i]}_
    mv ${splitfiles[$i]}_00 ${mmps_array[$i]}_REGULAR
    mv ${splitfiles[$i]}_01 ${mmps_array[$i]}_SKEWED
    mv ${splitfiles[$i]}_02 ${mmps_array[$i]}_MAXDIST
done
