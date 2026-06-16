#!/bin/bash
# collatz.sh -- hailstone sequence, fixed 200 iterations
MAX_ITERATIONS=200; COLUMNS=10; COLWIDTH=7
h=${1:-$$}
echo "Starting seed: $h"
for (( i=1; i<=MAX_ITERATIONS; i++ )); do
    let "remainder = h % 2"
    if [ "$remainder" -eq 0 ]; then let "h /= 2"; else let "h = h*3 + 1"; fi
    printf "%${COLWIDTH}d" $h
    (( i % COLUMNS == 0 )) && echo
done
echo
