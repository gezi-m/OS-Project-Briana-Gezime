#!/bin/bash
# days_between.sh -- days between two MM/DD/YYYY dates (Gauss formula)
E_BADARGS=85
DIY=365; LEAPCYCLE=4; MIY=12; ADJ_DIY=367; DIM=1; indexyr=2

strip_leading_zero() { return $((10#$1)); }
day_index() {
    local m=$1 d=$2 y=$3 Days
    let "Days = $DIY*$y + $y/$LEAPCYCLE - $indexyr + $indexyr/$LEAPCYCLE + $ADJ_DIY*$m/$MIY + $d - $DIM"
    echo $Days
}
[ $# -ne 2 ] && { echo "Usage: $(basename $0) MM/DD/YYYY MM/DD/YYYY"; exit $E_BADARGS; }
m1=${1%%/*}; tmp=${1#*/}; d1=${tmp%%/*}; y1=${1##*/}
m2=${2%%/*}; tmp=${2#*/}; d2=${tmp%%/*}; y2=${2##*/}
strip_leading_zero $m1; m1=$?; strip_leading_zero $d1; d1=$?
strip_leading_zero $m2; m2=$?; strip_leading_zero $d2; d2=$?
idx1=$(day_index $m1 $d1 $y1); idx2=$(day_index $m2 $d2 $y2)
let "diff = idx1 - idx2"; [ $diff -lt 0 ] && let "diff = -diff"
echo "Days between $1 and $2: $diff"
