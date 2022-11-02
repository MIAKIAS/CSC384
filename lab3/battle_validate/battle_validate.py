import copy
import random
import time
import queue
import sys
import os

# Validation script for CSC384 A3 : battle.py
# Change input_easy1.txt, output_easy1.txt and solution_easy1.txt to run
#    other test inputs.

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print('Wrong input/output parameters...')
    exit(1)
  __, output_file, solution_file = sys.argv
  
  # Invoke the shell command to test the checkers solver
  print("Testing: " + output_file)
  # os.system("python3 ../battle.py "+ input_file + " " + output_file)

  output_read = open(output_file, "r")
  solution_read = open(solution_file, "r")

  output_lines = output_read.readlines()
  solution_lines = solution_read.readlines()
  passed = True

  for index in range(1, len(output_lines)):
    if output_lines[index].strip() != solution_lines[index].strip():
      print(f"Line {index + 1}: "
                             f"Expected <{output_lines[index].strip()}> "
                             f"Encountered <{solution_lines[index].strip()}>\n")
      passed = False
      sys.exit(1)

  if passed:
    print("Battleship output matches solution file.\n")
