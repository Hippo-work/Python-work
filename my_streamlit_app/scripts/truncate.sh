#!/bin/bash
input_file=$1
start=$2
stop=$3
temp_file=$4
output_file=$5
echo Processing:
python3 plugins/truncate_bits.py $input_file $start $stop $temp_file
python3 plugins/write_bytes.py $temp_file $output_file
