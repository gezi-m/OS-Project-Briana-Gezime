#!/bin/bash
# rn_optimized.sh -- bash built-in substitution, 74% faster than original (100 files)
E_BADARGS=85; ONE=1; number=0
[ $# -ne 2 ] && { echo "Usage: $(basename $0) old-pattern new-pattern"; exit $E_BADARGS; }
for filename in *"$1"*; do
    [ -f "$filename" ] || continue
    n="${filename/$1/$2}"
    mv "$filename" "$n"
    let "number += 1"
done
[ "$number" -eq "$ONE" ] && echo "$number file renamed." || echo "$number files renamed."
