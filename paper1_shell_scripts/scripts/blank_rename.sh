#!/bin/bash
# blank_rename.sh -- replace spaces in filenames with underscores
FOUND=0; number=0
for filename in *; do
    echo "$filename" | grep -q " "
    if [ $? -eq $FOUND ]; then
        fname=$(basename "$filename")
        n=$(echo "$fname" | sed -e "s/ /_/g")
        mv "$fname" "$n"
        let "number += 1"
    fi
done
echo "$number files renamed."
