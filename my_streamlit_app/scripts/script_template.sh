#!/bin/bash

# Module: Template Script
# Desc: Description of what it does
# Auth: Creators Name
# Ver: 1.0
# ARG: input_file:str:Path to input binary file
# ARG: argument1:int:some integer you want to put into the plugin
# ARG: argument2:str:some string you want to put into the plugin
# ARG: output_file:str:Path to output file
# Usage: ./script_name.sh input_file output_file argument1 argument2 argument3 etc

#default values that are set:
input_file=$1 #input value set from the uploaded file name
arguments=$2 #set from the scripts/scripts.json script name
output_file=downloads/out.bit #fixed value
temp_file=downloads/tmp.bit #fixed value

echo "Processing:"

#example: layout, input file is uploaded onto the Script processor
#example: all other steps use a temp file except the final output
python3 plugins/bit_packer.py unpack_bits $input_file $temp_file
python3 plugins/truncate_bits.py $temp_file $temp_file $arguments
python3 plugins/bit_packer.py pack_bits $temp_file $temp_file
python3 plugins/write_bytes.py $temp_file $output_file

echo "Finished"