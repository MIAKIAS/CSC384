'''
    Fall 2022 - CSC384 - Lab2
    Author: Weizhou Wang
    Student#: 1004421262
'''

from inspect import getargvalues
import string
import copy
from sys import argv

# Compute the ultility value of the state
def utility(state:list) -> int:
    score = 0
    for row in list:
        for item in row:
            if item == 'r':
                score += 1
            elif item == 'R':
                score += 2
            elif item == 'b':
                score -= 1
            elif item == 'B':
                score -= 2
    return score

# Deal with multiple jumps
def jump_finder(state:list, tile:string, i:int, j:int, successors:list, firstCall:bool) -> None:
    isJump = False
    if (tile == 'r' or tile == 'R'):
        # Red can jump to up-left
        if (i-1 >= 0 and j-1 >= 0 and (state[i-1][j-1] == 'b' or state[i-1][j-1] == 'B') and i-2 >= 0 and j-2 >= 0 and state[i-2][j-2] == '.'):
            isJump = True
            temp_state = copy.deepcopy(state)
            temp_state[i][j] = '.'
            temp_state[i-1][j-1] = '.'
            temp_state[i-2][j-2] = tile
            # Upgrade to a king
            if (i-2 == 0):
                tile = 'R'
            #print("jump to up-left")
            jump_finder(temp_state, tile, i-2, j-2, successors, False)
        # Red can jump to up-right
        if (i-1 >= 0 and j+1 < 8 and (state[i-1][j+1] == 'b' or state[i-1][j+1] == 'B') and i-2 >= 0 and j+2 < 8 and state[i-2][j+2] == '.'):
            isJump = True
            temp_state = copy.deepcopy(state)
            temp_state[i][j] = '.'
            temp_state[i-1][j+1] = '.'
            temp_state[i-2][j+2] = tile
            # Upgrade to a king
            if (i-2 == 0):
                tile = 'R'
            #print("jump to up-right")
            jump_finder(temp_state, tile, i-2, j+2, successors, False)
        if (tile == 'R'):
            # RED KING can jump to down-left
            if (i+1 < 8 and j-1 >= 0 and (state[i+1][j-1] == 'b' or state[i+1][j-1] == 'B') and i+2 >= 0 and j-2 >= 0 and state[i+2][j-2] == '.'):
                isJump = True
                temp_state = copy.deepcopy(state)
                temp_state[i][j] = '.'
                temp_state[i+1][j-1] = '.'
                temp_state[i+2][j-2] = tile
                #print("jump to down-left")
                jump_finder(temp_state, tile, i+2, j-2, successors, False)
            # RED KING can jump to down-right
            if (i+1 < 8 and j+1 < 8 and (state[i+1][j+1] == 'b' or state[i+1][j+1] == 'B') and i+2 < 8 and j+2 < 8 and state[i+2][j+2] == '.'):
                isJump = True
                temp_state = copy.deepcopy(state)
                temp_state[i][j] = '.'
                temp_state[i+1][j+1] = '.'
                temp_state[i+2][j+2] = tile
                #print("jump to down-right")
                jump_finder(temp_state, tile, i+2, j+2, successors, False)
    else:
        # Black can jump to down-left
        if (i+1 < 8 and j-1 >= 0 and (state[i+1][j-1] == 'r' or state[i+1][j-1] == 'R') and i+2 >= 0 and j-2 >= 0 and state[i+2][j-2] == '.'):
            isJump = True
            temp_state = copy.deepcopy(state)
            temp_state[i][j] = '.'
            temp_state[i+1][j-1] = '.'
            temp_state[i+2][j-2] = tile
            # Upgrade to a king
            if (i+2 == 7):
                tile = 'B'
            print("(%d;%d) jump to down-left" %(i,j))
            jump_finder(temp_state, tile, i+2, j-2, successors, False)
        # Black can jump to down-right
        if (i+1 < 8 and j+1 < 8 and (state[i+1][j+1] == 'r' or state[i+1][j+1] == 'R') and i+2 < 8 and j+2 < 8 and state[i+2][j+2] == '.'):
            isJump = True
            temp_state = copy.deepcopy(state)
            temp_state[i][j] = '.'
            temp_state[i+1][j+1] = '.'
            temp_state[i+2][j+2] = tile
            # Upgrade to a king
            if (i+2 == 7):
                tile = 'B'
            print("jump to down-right")
            jump_finder(temp_state, tile, i+2, j+2, successors, False)
        if (tile == 'B'):
            # BLACK KING can jump to up-left
            if (i-1 >= 0 and j-1 >= 0 and (state[i-1][j-1] == 'r' or state[i-1][j-1] == 'R') and i-2 >= 0 and j-2 >= 0 and state[i-2][j-2] == '.'):
                isJump = True
                temp_state = copy.deepcopy(state)
                temp_state[i][j] = '.'
                temp_state[i-1][j-1] = '.'
                temp_state[i-2][j-2] = tile
                print("jump to up-left")
                jump_finder(temp_state, tile, i-2, j-2, successors, False)
            # BLACK KING can jump to up-right
            if (i-1 >= 0 and j+1 < 8 and (state[i-1][j+1] == 'r' or state[i-1][j+1] == 'R') and i-2 >= 0 and j+2 < 8 and state[i-2][j+2] == '.'):
                isJump = True
                temp_state = copy.deepcopy(state)
                temp_state[i][j] = '.'
                temp_state[i-1][j+1] = '.'
                temp_state[i-2][j+2] = tile
                print("jump to up-right")
                jump_finder(temp_state, tile, i-2, j+2, successors, False)
    if (not isJump and not firstCall):
        successors.append(state)
        return
    return

# Find all possible successors
def successors(state:list, isRed:bool) -> list:
    successors = []
    
    # First check if the player can jump
    for i in range(8):
        for j in range(8):
            # Continue if no tile on the location, or the tile is not current payler's
            if (state[i][j] == '.' or (isRed and (state[i][j] == 'b' or state[i][j] == 'B')) or (not isRed and (state[i][j] == 'r' or state[i][j] == 'R'))):
                continue
            jump_finder(state, state[i][j], i, j, successors, True)
    # Return if the player can jump
    if (len(successors) != 0):
        return successors

    # Seek for single move
    for i in range(8):
        for j in range(8):
            # Continue if no tile on the location, or the tile is not current payler's
            if (state[i][j] == '.' or (isRed and (state[i][j] == 'b' or state[i][j] == 'B')) or (not isRed and (state[i][j] == 'r' or state[i][j] == 'R'))):
                continue
            if (isRed):
                # Red can move up-left
                if (i-1 >= 0 and j-1 >= 0 and state[i-1][j-1] == '.'):
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = '.'
                    # Upgrade to a king
                    if (i-1 == 0 and state[i][j] == 'r'):
                        new_state[i-1][j-1] = 'R'
                    else:
                        new_state[i-1][j-1] = state[i][j]
                    successors.append(new_state)
                # Red can move up-right
                if (i-1 >= 0 and j+1 < 8 and state[i-1][j+1] == '.'):
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = '.'
                    # Upgrade to a king
                    if (i-1 == 0 and state[i][j] == 'r'):
                        new_state[i-1][j+1] = 'R'
                    else:
                        new_state[i-1][j+1] = state[i][j]
                    successors.append(new_state)
                # RED KING can move down-left
                if (state[i][j] == 'R' and i+1 < 8 and j-1 >= 0 and state[i+1][j-1] == '.'):
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = '.'
                    new_state[i+1][j-1] = state[i][j]
                    successors.append(new_state)
                # RED KING can move down-right
                if (state[i][j] == 'R' and i+1 < 8 and j+1 < 8 and state[i+1][j+1] == '.'):
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = '.'
                    new_state[i+1][j+1] = state[i][j]
                    successors.append(new_state)
            else:
                # Black can move down-left
                if (i+1 < 8 and j-1 >= 0 and state[i+1][j-1] == '.'):
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = '.'
                    # Upgrade to a king
                    if (i+1 == 7 and state[i][j] == 'b'):
                        new_state[i+1][j-1] = 'B'
                    else:
                        new_state[i+1][j-1] = state[i][j]
                    successors.append(new_state)
                # Black can move down-right
                if (i+1 < 8 and j+1 < 8 and state[i+1][j+1] == '.'):
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = '.'
                    # Upgrade to a king
                    if (i+1 == 7 and state[i][j] == 'b'):
                        new_state[i+1][j+1] = 'B'
                    else:
                        new_state[i+1][j+1] = state[i][j]
                    successors.append(new_state)
                # BLACK KING can move up-left
                if (state[i][j] == 'B' and i-1 >= 0 and j-1 >= 0 and state[i-1][j-1] == '.'):
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = '.'
                    new_state[i-1][j-1] = state[i][j]
                    successors.append(new_state)
                # BLACK KING can move up-right
                if (state[i][j] == 'B' and i-1 >= 0 and j+1 < 8 and state[i-1][j+1] == '.'):
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = '.'
                    new_state[i-1][j+1] = state[i][j]
                    successors.append(new_state)
    return successors


if __name__== "__main__":
    if len(argv) != 3:
        print('Wrong input/output parameters...')
        exit(1)

    # Read in the input/output file names
    __, input_file, output_file = argv

    # Read initial state from input file
    initial_state = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Convert the board format to a 8x8 list
            line = list(line.strip())
            initial_state.append(line)
        for i in initial_state:
            print(i)
        print('==========================================')

        ans = successors(initial_state, True)
        print("%d moves"%len(ans))
        for i in ans[1]:
            print(i)

        

            




