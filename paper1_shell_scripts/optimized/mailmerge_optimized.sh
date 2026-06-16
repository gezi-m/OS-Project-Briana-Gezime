#!/bin/bash
# mailmerge_optimized.sh -- template cached in memory, bash substitution, ~50% faster
TEMPLATE="template.txt"; NAMES="names"
[ ! -f "$TEMPLATE" ] && { echo "Missing $TEMPLATE"; exit 1; }
[ ! -f "$NAMES" ] && { echo "Missing $NAMES"; exit 1; }
template=$(cat "$TEMPLATE")
while read name; do
    echo "${template//NAME/$name}" > "letter_${name}.txt"
    echo "Created letter for $name"
done < "$NAMES"
