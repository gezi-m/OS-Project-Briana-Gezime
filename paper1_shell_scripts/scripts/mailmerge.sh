#!/bin/bash
# mailmerge.sh -- generate personalized letters from NAME template
TEMPLATE="template.txt"; NAMES="names"
[ ! -f "$TEMPLATE" ] && { echo "Missing $TEMPLATE"; exit 1; }
[ ! -f "$NAMES" ] && { echo "Missing $NAMES"; exit 1; }
while read name; do
    sed "s/NAME/$name/g" "$TEMPLATE" > "letter_${name}.txt"
    echo "Created letter for $name"
done < "$NAMES"
