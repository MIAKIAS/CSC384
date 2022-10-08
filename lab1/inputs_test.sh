#!/bin/bash
for i in $(seq 32)
do
    echo "====$i===="
    echo python3 hrd.py ./inputs/$i.txt ./outputs_DFS/puzzle5sol_dfs$i.txt ./outputs_Manhattan/puzzle5sol_astar$i.txt
    python3 hrd.py ./inputs/$i.txt ./outputs_DFS/puzzle5sol_dfs$i.txt ./outputs_Manhattan/puzzle5sol_astar$i.txt
    echo python3 valid.py $i ./outputs_DFS/puzzle5sol_dfs$i.txt
    python3 valid.py $i ./outputs_DFS/puzzle5sol_dfs$i.txt
    echo python3 valid.py $i ./outputs_Manhattan/puzzle5sol_astar$i.txt
    python3 valid.py $i ./outputs_Manhattan/puzzle5sol_astar$i.txt
    # echo python3 valid.py $i ./outputs_Advanced/puzzle5sol_advanced.txt
    # python3 valid.py $i ./outputs_Advanced/puzzle5sol_advanced.txt
done