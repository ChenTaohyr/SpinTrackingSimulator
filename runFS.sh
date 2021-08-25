#!/bin/bash
Speed=(3000 2000 1000 700 400 100 70 40 10 7 4 1 0.7 0.4 0.1 0)
for ((k=0;k<=14;k++))
do
    python /Users/chentao/mywork_Duanz/SpinDynamics/SpinTracking/spintracking.py  parameters.txt
    sed -i '' "11s/${Speed[k]}/${Speed[k+1]}/" parameters.txt

done
sed -i '' '11s/0/3000/' parameters.txt
python DrawFS.py FSData_test2.txt

