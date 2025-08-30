#!/bin/bash

echo "File: $1"
echo "Sample Rate: $2"
echo "Center Freq: $3"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRUNCATE_SCRIPT="$SCRIPT_DIR/../plugins/truncate_bits.py"


temp_file="$SCRIPT_DIR/../downloads/tmp.bits"
python3 "$TRUNCATE_SCRIPT" truncate "$1" "$2" "$3" > "$temp_file"
BITSTREAM=$(<"$temp_file")
echo "$BITSTREAM"
python3 "$SCRIPT_DIR/../plugins/write_bytes.py" write "$BITSTREAM" "$SCRIPT_DIR/../downloads/output.bits"
echo "file in /downloads/output.bits"