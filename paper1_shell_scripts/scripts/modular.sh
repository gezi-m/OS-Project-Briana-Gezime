#!/bin/bash
# modular.sh -- brute force: find nr satisfying nr%5=3, nr%7=4, nr%9=5
MAX=10000
for((nr=1; nr<$MAX; nr++)); do
    let "t1 = nr % 5"; [ "$t1" -ne 3 ] && continue
    let "t2 = nr % 7"; [ "$t2" -ne 4 ] && continue
    let "t3 = nr % 9"; [ "$t3" -ne 5 ] && continue
    break
done
echo "Number = $nr"
