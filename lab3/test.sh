#!/bin/bash

rm *out.txt
for i in $(seq 0 15)
do
    echo "=====================Test $i====================="
    time timeout -s SIGKILL 5 python3 battle.py ./battle_validate/$i.txt ${i}out.txt
    retVal=$?
    if [ $retVal -ne 0 ]; then
        exit $retVal
    fi
    python3 ./battle_validate/battle_validate.py ${i}out.txt ./battle_validate/${i}ref.txt
done

rm ./testcases_out/*
for i in $(seq 0 301)
do
    echo "=====================New Testcase $i====================="
    time timeout -s SIGKILL 3m python3 battle.py ./testcases/$i.txt ./testcases_out/${i}out.txt
    retVal=$?
    if [ $retVal -ne 0 ]; then
        exit $retVal
    fi
    
done