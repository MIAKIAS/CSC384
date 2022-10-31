#!/bin/sh

python3 battle.py ./battle_validate/input_easy1.txt output_easy1.txt
python3 ./battle_validate/battle_validate.py output_easy1.txt ./battle_validate/solution_easy1.txt

python3 battle.py ./battle_validate/input_easy2.txt output_easy2.txt
python3 ./battle_validate/battle_validate.py output_easy2.txt ./battle_validate/solution_easy2.txt

python3 battle.py ./battle_validate/input_medium1.txt output_medium1.txt
python3 ./battle_validate/battle_validate.py output_medium1.txt ./battle_validate/solution_medium1.txt

python3 battle.py ./battle_validate/input_medium2.txt output_medium2.txt
python3 ./battle_validate/battle_validate.py output_medium2.txt ./battle_validate/solution_medium2.txt

python3 battle.py ./battle_validate/input_hard1.txt output_hard1.txt
python3 ./battle_validate/battle_validate.py output_hard1.txt ./battle_validate/solution_hard1.txt

python3 battle.py ./battle_validate/input_hard2.txt output_hard2.txt
python3 ./battle_validate/battle_validate.py output_hard2.txt ./battle_validate/solution_hard2.txt