#!/bin/bash
# rn.sh -- rename files by substituting old-pattern with new-pattern
E_BADARGS=85; ONE=1; number=0
[ $# -ne 2 ] && { echo "Usage: $(basename $0) old-pattern new-pattern"; exit $E_BADARGS; }
for filename in *"$1"*; do
    [ -f "$filename" ] || continue
    fname=$(basename "$filename")
    n=$(echo "$fname" | sed -e "s/$1/$2/")
    mv "$fname" "$n"
    let "number += 1"
done
[ "$number" -eq "$ONE" ] && echo "$number file renamed." || echo "$number files renamed."
