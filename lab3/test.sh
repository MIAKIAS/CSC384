#!/bin/bash

rm output*.txt
time timeout -s SIGKILL 5 python3 battle.py ./battle_validate/input_easy1.txt output_easy1.txt
retVal=$?
if [ $retVal -ne 0 ]; then
    exit $retVal
fi
python3 ./battle_validate/battle_validate.py output_easy1.txt /h/u17/c1/00/wangw222/csc384/lab3/battle_validate/solution_easy1.txt
retVal=$?
if [ $retVal -ne 0 ]; then
    exit $retVal
fi

time timeout -s SIGKILL 5 python3 battle.py ./battle_validate/input_easy2.txt output_easy2.txt
retVal=$?
if [ $retVal -ne 0 ]; then
    exit $retVal
fi
python3 ./battle_validate/battle_validate.py output_easy2.txt /h/u17/c1/00/wangw222/csc384/lab3/battle_validate/solution_easy2.txt
retVal=$?
if [ $retVal -ne 0 ]; then
    exit $retVal
fi

time timeout -s SIGKILL 5 python3 battle.py ./battle_validate/input_medium1.txt output_medium1.txt
retVal=$?
if [ $retVal -ne 0 ]; then
    exit $retVal
fi
python3 ./battle_validate/battle_validate.py output_medium1.txt /h/u17/c1/00/wangw222/csc384/lab3/battle_validate/solution_medium1.txt
retVal=$?
if [ $retVal -ne 0 ]; then
    exit $retVal
fi

time timeout -s SIGKILL 5 python3 battle.py ./battle_validate/input_medium2.txt output_medium2.txt
retVal=$?
if [ $retVal -ne 0 ]; then
    exit $retVal
fi
python3 ./battle_validate/battle_validate.py output_medium2.txt /h/u17/c1/00/wangw222/csc384/lab3/battle_validate/solution_medium2.txt
retVal=$?
if [ $retVal -ne 0 ]; then
    exit $retVal
fi

time timeout -s SIGKILL 5 python3 battle.py ./battle_validate/input_hard1.txt output_hard1.txt
retVal=$?
if [ $retVal -ne 0 ]; then
    exit $retVal
fi
python3 ./battle_validate/battle_validate.py output_hard1.txt /h/u17/c1/00/wangw222/csc384/lab3/battle_validate/solution_hard1.txt
retVal=$?
if [ $retVal -ne 0 ]; then
    exit $retVal
fi

time timeout -s SIGKILL 5 python3 battle.py ./battle_validate/input_hard2.txt output_hard2.txt
retVal=$?
if [ $retVal -ne 0 ]; then
    exit $retVal
fi
python3 ./battle_validate/battle_validate.py output_hard2.txt /h/u17/c1/00/wangw222/csc384/lab3/battle_validate/solution_hard2.txt
retVal=$?
if [ $retVal -ne 0 ]; then
    exit $retVal
fi

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
    retVal=$?
    if [ $retVal -ne 0 ]; then
        exit $retVal
    fi
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
    python3 ./battle_validate/battle_validate.py ./testcases_out/${i}out.txt ./Output_wwz/${i}out.txt
    retVal=$?
    if [ $retVal -ne 0 ]; then
        exit $retVal
    fi
    
done