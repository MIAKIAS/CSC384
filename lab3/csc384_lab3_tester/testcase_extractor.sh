#!/bin/bash

i=1
index=0
string=""
while read -r line; do
    if [ $i -eq 0 ]
    then
        echo $string > ./testcases/${index}.txt
        string=""
        ((index+=1))
        i=1
    fi
    string="$string$line"
    ((i+=1))
    ((i%=6))
done < <(grep -A 4 -E "problem\([0-9]+" ./battleship_instances.pl)