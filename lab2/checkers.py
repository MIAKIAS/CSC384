'''
    Fall 2022 - CSC384 - Lab2
    Author: Weizhou Wang
    Student#: 1004421262
'''

'''
FIXME: 1. Timer
       2. Cache: Finished, but need to tune if comparing depth
       3. Heuristic
       15 level, 156sec
'''

from cmath import inf
from queue import PriorityQueue
import string
import copy
from sys import argv

# Global Variables
depth_limit = 15
state_cache = {}

# Compute the ultility value of the state
def utility(state:list) -> int:
    score = 0
    for row in state:
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

# Check if the game has ended
def is_game_end(state:list) -> bool:
    isRed = False
    isBlack = False
    for row in state:
        if isRed and isBlack:
            return False
        for item in row:
            if item == 'r' or item == 'R':
                isRed = True
            elif item == 'b' or item == 'B':
                isBlack = True
    return not (isRed and isBlack)

# Deal with multiple jumps
def jump_finder(state:list, tile:string, i:int, j:int, successors:PriorityQueue, firstCall:bool) -> None:
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
            if (i+1 < 8 and j-1 >= 0 and (state[i+1][j-1] == 'b' or state[i+1][j-1] == 'B') and i+2 < 8 and j-2 >= 0 and state[i+2][j-2] == '.'):
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
        if (i+1 < 8 and j-1 >= 0 and (state[i+1][j-1] == 'r' or state[i+1][j-1] == 'R') and i+2 < 8 and j-2 >= 0 and state[i+2][j-2] == '.'):
            isJump = True
            temp_state = copy.deepcopy(state)
            temp_state[i][j] = '.'
            temp_state[i+1][j-1] = '.'
            temp_state[i+2][j-2] = tile
            # Upgrade to a king
            if (i+2 == 7):
                tile = 'B'
            #print("(%d;%d) jump to down-left" %(i,j))
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
            #print("jump to down-right")
            jump_finder(temp_state, tile, i+2, j+2, successors, False)
        if (tile == 'B'):
            # BLACK KING can jump to up-left
            if (i-1 >= 0 and j-1 >= 0 and (state[i-1][j-1] == 'r' or state[i-1][j-1] == 'R') and i-2 >= 0 and j-2 >= 0 and state[i-2][j-2] == '.'):
                isJump = True
                temp_state = copy.deepcopy(state)
                temp_state[i][j] = '.'
                temp_state[i-1][j-1] = '.'
                temp_state[i-2][j-2] = tile
                #print("jump to up-left")
                jump_finder(temp_state, tile, i-2, j-2, successors, False)
            # BLACK KING can jump to up-right
            if (i-1 >= 0 and j+1 < 8 and (state[i-1][j+1] == 'r' or state[i-1][j+1] == 'R') and i-2 >= 0 and j+2 < 8 and state[i-2][j+2] == '.'):
                isJump = True
                temp_state = copy.deepcopy(state)
                temp_state[i][j] = '.'
                temp_state[i-1][j+1] = '.'
                temp_state[i-2][j+2] = tile
                #print("jump to up-right")
                jump_finder(temp_state, tile, i-2, j+2, successors, False)
    if (not isJump and not firstCall):
        if (tile == 'r' or tile == 'R'):
            successors.put((-1 * utility(state), successors.qsize(), state))
        else:
            successors.put((utility(state), successors.qsize(), state))
        return
    return

# Find all possible successors
def successors(state:list, isRed:bool) -> PriorityQueue:
    successors = PriorityQueue()
    # Change to inscending or descending depends on player
    priority_parameter = -1 if isRed else 1
    
    # First check if the player can jump
    for i in range(8):
        for j in range(8):
            # Continue if no tile on the location, or the tile is not current payler's
            if (state[i][j] == '.' or (isRed and (state[i][j] == 'b' or state[i][j] == 'B')) or (not isRed and (state[i][j] == 'r' or state[i][j] == 'R'))):
                continue
            jump_finder(state, state[i][j], i, j, successors, True)
    # Return if the player can jump
    if (successors.qsize() != 0):
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
                    successors.put((priority_parameter * utility(new_state), successors.qsize(), new_state))
                # Red can move up-right
                if (i-1 >= 0 and j+1 < 8 and state[i-1][j+1] == '.'):
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = '.'
                    # Upgrade to a king
                    if (i-1 == 0 and state[i][j] == 'r'):
                        new_state[i-1][j+1] = 'R'
                    else:
                        new_state[i-1][j+1] = state[i][j]
                    successors.put((priority_parameter * utility(new_state), successors.qsize(), new_state))
                # RED KING can move down-left
                if (state[i][j] == 'R' and i+1 < 8 and j-1 >= 0 and state[i+1][j-1] == '.'):
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = '.'
                    new_state[i+1][j-1] = state[i][j]
                    successors.put((priority_parameter * utility(new_state), successors.qsize(), new_state))
                # RED KING can move down-right
                if (state[i][j] == 'R' and i+1 < 8 and j+1 < 8 and state[i+1][j+1] == '.'):
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = '.'
                    new_state[i+1][j+1] = state[i][j]
                    successors.put((priority_parameter * utility(new_state), successors.qsize(), new_state))
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
                    successors.put((priority_parameter * utility(new_state), successors.qsize(), new_state))
                # Black can move down-right
                if (i+1 < 8 and j+1 < 8 and state[i+1][j+1] == '.'):
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = '.'
                    # Upgrade to a king
                    if (i+1 == 7 and state[i][j] == 'b'):
                        new_state[i+1][j+1] = 'B'
                    else:
                        new_state[i+1][j+1] = state[i][j]
                    successors.put((priority_parameter * utility(new_state), successors.qsize(), new_state))
                # BLACK KING can move up-left
                if (state[i][j] == 'B' and i-1 >= 0 and j-1 >= 0 and state[i-1][j-1] == '.'):
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = '.'
                    new_state[i-1][j-1] = state[i][j]
                    successors.put((priority_parameter * utility(new_state), successors.qsize(), new_state))
                # BLACK KING can move up-right
                if (state[i][j] == 'B' and i-1 >= 0 and j+1 < 8 and state[i-1][j+1] == '.'):
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = '.'
                    new_state[i-1][j+1] = state[i][j]
                    successors.put((priority_parameter * utility(new_state), successors.qsize(), new_state))
    return successors

# Alpha-Beta Pruning Implementation
def AlphaBeta(state:list, isRed:bool, alpha:int, beta:int, depth:int) -> tuple[list, int]:
    global depth_limit
    best_move = None
    # Check whether we reach the depth limit or the game has ended
    if (depth == depth_limit or is_game_end(state)):
        return best_move, utility(state)
    potential_position = successors(state, isRed)

    # Check whether it is a terminal state
    if (potential_position.qsize() == 0):
        return best_move, utility(state)

    # Initial value
    value = int()
    if (isRed):
        value = -inf
    else:
        value = inf
    
    # Recurcively iterate nodes as in DFS
    while not potential_position.empty():
        next_position = potential_position.get()[2]

        '''=================================Cache Check======================================'''
        next_value = int()
        # Convert the state into string format used in cache
        next_position_string = ''.join(''.join(row) for row in next_position) + ('R' if isRed else 'B')
        # Check if the state is in cache and the stored state have a lower level than the current
        if next_position_string in state_cache and depth >= state_cache[next_position_string][-1]:
            next_value = state_cache[next_position_string][0]
        else:
            # Switch to opponent and increment depth
            __, next_value = AlphaBeta(next_position, not isRed, alpha, beta, depth+1)
            # Add to cache
            state_cache[next_position_string] = (next_value, depth)
        '''=================================================================================='''

        # Red == Ourselves == MAX
        if (isRed):
            if (value < next_value):
                value, best_move = next_value, next_position
            if (value >= beta):
                return best_move, value
            alpha = max(alpha, value)
        else:
            if (value > next_value):
                value, best_move = next_value, next_position
            if (value <= alpha):
                return best_move, value
            beta = min(beta, value)

    # Return the best move and value of root
    return best_move, value

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
    print('=================='+ input_file + '=================')
    for i in initial_state:
        print(i)

    print('==========================================')
    next_move, __ = AlphaBeta(initial_state, True, -inf, inf, 0)
    if (next_move == None):
        print("Game already ended")
        next_move = initial_state
    for i in next_move:
        print(i)

    with open(output_file, 'w', encoding='utf-8') as f:
        text = ''
        for row in next_move:
            text += ''.join(row)
            text += '\n'
        f.write(text.strip())

        

            




