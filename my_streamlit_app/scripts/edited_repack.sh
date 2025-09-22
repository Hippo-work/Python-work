#!/bin/bash
# Module: Repack Bits
# Desc: Unpacks then Repacks bits, effectively useless, just for description purposes
# Auth: James
# Ver: 1.0
# ARG: function:str:unpack_bits or pack_bits
# ARG: input_file:str:Path to input file
# ARG: output_file:str:Path to output file
# Usage: ./repack.sh "function" input_file output_file
echo "Unpack bits followed by pack bits and write them out"
input_file=$1
arg1=$2
arg2=$3
temp_file=downloads/tmp.bit
output_file=downloads/out.bit
python3 plugins/bit_packer.py unpack_bits $input_file $temp_file
python3 plugins/bit_packer.py pack_bits $temp_file $output_file
echo test