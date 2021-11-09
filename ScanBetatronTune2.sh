#!/bin/bash
#ShiftTune=(0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.10 0.11 0.12 0.13 0.14 0.15 0.16 0.17 0.18 0.19 0.20 0.21 0.22 0.23 0.24 0.25 0.26 0.27 0.28 0.29 0.30 0.31)
for((i=0;i<=19;i++))
do
ShiftTune[i]=`echo "8.80+0.01*$i"|bc`
echo ${ShiftTune[i]}
done
ShiftTune[20]=31

for ((k=0;k<=19;k++))
do
    python /Users/chentao/mywork_Duanz/SpinDynamics/SpinTracking/spintracking.py  parameters.txt
    sed -i '' "7s/${ShiftTune[k]}/${ShiftTune[k+1]}/" parameters.txt

done 