#!/bin/sh

rm *out.txt
for i in $(seq 0 15)
do
    echo "=====================Test $i====================="
    time python3 battle.py ./battle_validate/$i.txt ${i}out.txt
    retVal=$?
    if [ $retVal -ne 0 ]; then
        exit $retVal
    fi
    python3 ./battle_validate/battle_validate.py ${i}out.txt ./battle_validate/${i}ref.txt
done