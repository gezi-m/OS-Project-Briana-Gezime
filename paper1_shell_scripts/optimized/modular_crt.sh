#!/bin/bash
# modular_crt.sh -- O(1) via Chinese Remainder Theorem
# N=LCM(5,7,9)=315; N1=63,N2=45,N3=35; y1=2,y2=5,y3=8 (modular inverses)
# x = (3*63*2 + 4*45*5 + 5*35*8) mod 315 = 2678 mod 315 = 158
x=$(( (3*63*2 + 4*45*5 + 5*35*8) % 315 ))
echo "Number = $x"
echo "Verify: $x%5=$(($x%5)) [need 3], $x%7=$(($x%7)) [need 4], $x%9=$(($x%9)) [need 5]"
