#!/bin/bash

# Module: Truncate Bits
# Desc: Truncates a binary file from start to stop index
# Auth: James
# Ver: 1.0
# ARG: input_file:str:Path to input binary file
# ARG: start:int:Start index
# ARG: stop:int:Stop index
# ARG: output_file:str:Path to output file
# Usage: ./truncate.sh input_file start stop output_file

input_file=$1
start=$2
stop=$3
temp_file=downloads/tmp.bit
output_file=downloads/out.bit

echo Processing:

python3 plugins/bit_packer.py unpack_bits $input_file $temp_file
python3 plugins/truncate_bits.py $temp_file $start $stop $temp_file
python3 plugins/bit_packer.py pack_bits $temp_file $temp_file
python3 plugins/write_bytes.py $temp_file $output_file

echo Almost works perfectly, just need the left align right pad function added
