'''
    Fall 2022 - CSC384 - Lab2
    Author: Weizhou Wang
    Student#: 1004421262
'''

'''
FIXME: 
       2. Cache: Finished, but need to tune if comparing depth
       3. Heuristic
       15 level, 64.02sec
'''

from cmath import inf
from queue import PriorityQueue
import string
import copy
from sys import argv

# Global Variables
depth_limit = 10
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

# Compute my own heuristic value of the state using researched heuristic function
# def heuristic(state:list) -> int:

#     # Number of corresponding tiles
#     num_pawns_r = 0
#     num_pawns_b = 0
#     num_kings_R = 0
#     num_kings_B = 0
#     # # Number of tiles adjacent to edges
#     # num_safe_pawns = 0
#     # num_safe_kings = 0
#     # # Number of tiles that can move
#     # num_move_pawns = 0
#     # num_move_kings = 0
#     # Number of tiles that can jump
#     num_jump_pawns = 0
#     num_jump_kings = 0
#     # # Aggregated distance of the pawns to two promotion lines
#     # agg_distance = 0
#     # # Number of unoccupied fields on promotion line
#     # unoccupied_promotion_field = 0
#     # Number of pyramid shapes
#     num_pyramids = 0
#     # Number of bridges
#     num_bridges = 0
#     # Number of blocks
#     num_blocks = 0

    
#     # for item in state[0]:
#     #     if item == '.':
#     #         unoccupied_promotion_field += 1
#     # for item in state[7]:
#     #     if item == '.':
#     #         unoccupied_promotion_field -= 1

#     for row in range(len(state)):
#         for col in range(len(state[row])):
#             if state[row][col] == '.':
#                 continue
#             elif state[row][col] == 'r':
#                 # if col == 0 or col == 7:
#                 #     num_safe_pawns += 1

#                 # if row-1 >= 0 and ((col-1 >= 0 and state[row-1][col-1] == '.') or (col+1 < 8 and state[row-1][col+1]) == '.'):
#                 #     num_move_pawns += 1

#                 if (row-2 >= 0 and col-2 >= 0 and (state[row-1][col-1] == 'b' or state[row-1][col-1] == 'B') and state[row-2][col-2] == '.'):
#                     num_jump_pawns += 1

#                 if (row-2 >= 0 and col+2 <  8 and (state[row-1][col+1] == 'b' or state[row-1][col+1] == 'B') and state[row-2][col+2] == '.'):
#                     num_jump_pawns += 1

#                 if (row+1 <  8 and col-1 >= 0 and col+1 <  8 and (state[row+1][col-1] == 'r' or state[row+1][col-1] == 'R') and (state[row+1][col+1] == 'r' or state[row+1][col+1] == 'R')):
#                     num_pyramids += 1
#                 if (col == 0 and row-2 >= 0 and (state[row-1][col+1] == 'b' or state[row-1][col+1] == 'B') and (state[row-2][col+2] == 'b' or state[row-2][col+2] == 'B')):
#                     num_blocks -= 1

#                 # if (row <= 3):
#                 #     agg_distance -= row
#                 # else:
#                 #     agg_distance -= 7 - row

#                 num_pawns_r += 1
#             elif state[row][col] == 'R':
#                 # if row == 0 or row == 7 or col == 0 or col == 7:
#                 #     num_safe_kings += 1

#                 # if (row-1 >= 0 and ((col-1 >= 0 and state[row-1][col-1] == '.') or (col+1 < 8 and state[row-1][col+1] == '.'))) \
#                 # or (row+1 <  8 and ((col-1 >= 0 and state[row+1][col-1] == '.') or (col+1 < 8 and state[row+1][col+1] == '.'))):
#                 #     num_move_kings += 1

#                 if (row-2 >= 0 and col-2 >= 0 and (state[row-1][col-1] == 'b' or state[row-1][col-1] == 'B') and state[row-2][col-2] == '.'):
#                     num_jump_kings += 1
#                 if (row-2 >= 0 and col+2 <  8 and (state[row-1][col+1] == 'b' or state[row-1][col+1] == 'B') and state[row-2][col+2] == '.'):
#                     num_jump_kings += 1 
#                 if (row+2 <  8 and col-2 >= 0 and (state[row+1][col-1] == 'b' or state[row+1][col-1] == 'B') and state[row+2][col-2] == '.'):
#                     num_jump_kings += 1
#                 if (row+2 <  8 and col+2 <  8 and (state[row+1][col+1] == 'b' or state[row+1][col+1] == 'B') and state[row+2][col+2] == '.'):
#                     num_jump_kings += 1

#                 if (row+1 <  8 and col-1 >= 0 and col+1 <  8 and (state[row+1][col-1] == 'r' or state[row+1][col-1] == 'R') and (state[row+1][col+1] == 'r' or state[row+1][col+1] == 'R')):
#                     num_pyramids += 1

#                 if (col == 0 and row-2 >= 0 and row+2 < 8 and (state[row-1][col+1] == 'b' or state[row-1][col+1] == 'B') and (state[row-2][col+2] == 'b' or state[row-2][col+2] == 'B') \
#                     and (state[row+1][col+1] == 'b' or state[row+1][col+1] == 'B') and (state[row+2][col+2] == 'b' or state[row+2][col+2] == 'B')):
#                     num_blocks -= 1

#                 num_kings_R += 1
#             elif state[row][col] == 'b':
#                 # if col == 0 or col == 7:
#                 #     num_safe_pawns -= 1

#                 # if row+1 <  8 and ((col-1 >= 0 and state[row+1][col-1] == '.') or (col+1 < 8 and state[row+1][col+1] == '.')):
#                 #     num_move_pawns -= 1

#                 if (row+2 <  8 and col-2 >= 0 and (state[row+1][col-1] == 'r' or state[row+1][col-1] == 'R') and state[row+2][col-2] == '.'):
#                     num_jump_pawns -= 1
#                 if (row+2 <  8 and col+2 <  8 and (state[row+1][col+1] == 'r' or state[row+1][col+1] == 'R') and state[row+2][col+2] == '.'):
#                     num_jump_pawns -= 1

#                 if (row-1 >= 0 and col-1 >= 0 and col+1 <  8 and (state[row-1][col-1] == 'b' or state[row-1][col-1] == 'B') and (state[row-1][col+1] == 'b' or state[row-1][col+1] == 'B')):
#                     num_pyramids -= 1

#                 if (col == 7 and row+2 < 8 and (state[row+1][col-1] == 'r' or state[row+1][col-1] == 'R') and (state[row+2][col-2] == 'r' or state[row+2][col-2] == 'R')):
#                     num_blocks += 1

#                 # if (row <= 3):
#                 #     agg_distance += row
#                 # else:
#                 #     agg_distance += 7 - row

#                 num_pawns_b += 1
#             else: # state[row][col] == 'B'
#                 # if row == 0 or row == 7 or col == 0 or col == 7:
#                 #     num_safe_kings -= 1

#                 # if (row-1 >= 0 and ((col-1 >= 0 and state[row-1][col-1] == '.') or (col+1 < 8 and state[row-1][col+1] == '.'))) \
#                 # or (row+1 <  8 and ((col-1 >= 0 and state[row+1][col-1] == '.') or (col+1 < 8 and state[row+1][col+1] == '.'))):
#                 #     num_move_kings -= 1

#                 if (row-2 >= 0 and col-2 >= 0 and (state[row-1][col-1] == 'r' or state[row-1][col-1] == 'R') and state[row-2][col-2] == '.'):
#                     num_jump_kings -= 1
#                 if (row-2 >= 0 and col+2 <  8 and (state[row-1][col+1] == 'r' or state[row-1][col+1] == 'R') and state[row-2][col+2] == '.'):
#                     num_jump_kings -= 1
#                 if (row+2 <  8 and col-2 >= 0 and (state[row+1][col-1] == 'r' or state[row+1][col-1] == 'R') and state[row+2][col-2] == '.'):
#                     num_jump_kings -= 1
#                 if (row+2 <  8 and col+2 <  8 and (state[row+1][col+1] == 'r' or state[row+1][col+1] == 'R') and state[row+2][col+2] == '.'):
#                     num_jump_kings -= 1

#                 if (row-1 >= 0 and col-1 >= 0 and col+1 <  8 and (state[row-1][col-1] == 'b' or state[row-1][col-1] == 'B') and (state[row-1][col+1] == 'b' or state[row-1][col+1] == 'B')):
#                     num_pyramids -= 1

#                 if (col == 7 and row-2 >= 0 and row+2 < 8 and (state[row-1][col-1] == 'r' or state[row-1][col-1] == 'R') and (state[row-2][col-2] == 'r' or state[row-2][col-2] == 'R') \
#                     and (state[row+1][col-1] == 'r' or state[row+1][col-1] == 'R') and (state[row+2][col-2] == 'r' or state[row+2][col-2] == 'R')):
#                     num_blocks -= 1

#                 num_kings_B += 1

#     if (state[7][2] == 'r' or state[7][2] == 'R') and (state[7][6] == 'r' or state[7][6] == 'R'):
#         num_bridges += 1
#     if (state[0][1] == 'b' or state[0][1] == 'B') and (state[0][5] == 'b' or state[0][5] == 'B'):
#         num_bridges -= 1
#     if (state[1][0] == 'r' and (state[0][1] == 'b' or state[0][1] == 'B')):
#         num_blocks -= 1
#     if (state[6][7] == 'b' and (state[7][6] == 'r' or state[7][6] == 'R')):
#         num_blocks += 1

#     return num_pawns_r - num_pawns_b + 2 * (num_kings_R - num_kings_B) + num_pyramids + 0.5 * (num_jump_kings + num_jump_pawns) + num_blocks + num_bridges

# Check if the game has ended
def is_game_end(state:list, isRed:bool) -> bool:
    redExist = False
    blackExist = False
    for row in state:
        for item in row:
            if item == 'r' or item == 'R':
                redExist = True
            elif item == 'b' or item == 'B':
                blackExist = True
    
    if (not (redExist and blackExist)):
        return True

    if successors(state, not isRed, True).qsize() == 0:
        return True

    return False

# Deal with multiple jumps
def jump_finder(state:list, tile:string, i:int, j:int, successors:PriorityQueue, firstCall:bool, terminateCheck:bool=False) -> bool:
    isJump = False
    if (tile == 'r' or tile == 'R'):
        # Red can jump to up-left
        if (i-1 >= 0 and j-1 >= 0 and (state[i-1][j-1] == 'b' or state[i-1][j-1] == 'B') and i-2 >= 0 and j-2 >= 0 and state[i-2][j-2] == '.'):
            isJump = True
            temp_state = copy.deepcopy(state)
            # Upgrade to a king
            if (i-2 == 0):
                tile = 'R'
            temp_state[i][j] = '.'
            temp_state[i-1][j-1] = '.'
            temp_state[i-2][j-2] = tile
            ## print("jump to up-left")
            if terminateCheck:
                return True
            jump_finder(temp_state, tile, i-2, j-2, successors, False)
        # Red can jump to up-right
        if (i-1 >= 0 and j+1 < 8 and (state[i-1][j+1] == 'b' or state[i-1][j+1] == 'B') and i-2 >= 0 and j+2 < 8 and state[i-2][j+2] == '.'):
            isJump = True
            temp_state = copy.deepcopy(state)
            # Upgrade to a king
            if (i-2 == 0):
                tile = 'R'
            temp_state[i][j] = '.'
            temp_state[i-1][j+1] = '.'
            temp_state[i-2][j+2] = tile
            ## print("jump to up-right")
            if terminateCheck:
                return True
            jump_finder(temp_state, tile, i-2, j+2, successors, False)
        if (tile == 'R'):
            # RED KING can jump to down-left
            if (i+1 < 8 and j-1 >= 0 and (state[i+1][j-1] == 'b' or state[i+1][j-1] == 'B') and i+2 < 8 and j-2 >= 0 and state[i+2][j-2] == '.'):
                isJump = True
                temp_state = copy.deepcopy(state)
                temp_state[i][j] = '.'
                temp_state[i+1][j-1] = '.'
                temp_state[i+2][j-2] = tile
                ## print("jump to down-left")
                if terminateCheck:
                    return True
                jump_finder(temp_state, tile, i+2, j-2, successors, False)
            # RED KING can jump to down-right
            if (i+1 < 8 and j+1 < 8 and (state[i+1][j+1] == 'b' or state[i+1][j+1] == 'B') and i+2 < 8 and j+2 < 8 and state[i+2][j+2] == '.'):
                isJump = True
                temp_state = copy.deepcopy(state)
                temp_state[i][j] = '.'
                temp_state[i+1][j+1] = '.'
                temp_state[i+2][j+2] = tile
                ## print("jump to down-right")
                if terminateCheck:
                    return True
                jump_finder(temp_state, tile, i+2, j+2, successors, False)
    else:
        # Black can jump to down-left
        if (i+1 < 8 and j-1 >= 0 and (state[i+1][j-1] == 'r' or state[i+1][j-1] == 'R') and i+2 < 8 and j-2 >= 0 and state[i+2][j-2] == '.'):
            isJump = True
            temp_state = copy.deepcopy(state)
            # Upgrade to a king
            if (i+2 == 7):
                tile = 'B'
            temp_state[i][j] = '.'
            temp_state[i+1][j-1] = '.'
            temp_state[i+2][j-2] = tile
            ## print("(%d;%d) jump to down-left" %(i,j))
            if terminateCheck:
                return True
            jump_finder(temp_state, tile, i+2, j-2, successors, False)
        # Black can jump to down-right
        if (i+1 < 8 and j+1 < 8 and (state[i+1][j+1] == 'r' or state[i+1][j+1] == 'R') and i+2 < 8 and j+2 < 8 and state[i+2][j+2] == '.'):
            isJump = True
            temp_state = copy.deepcopy(state)
            # Upgrade to a king
            if (i+2 == 7):
                tile = 'B'
            temp_state[i][j] = '.'
            temp_state[i+1][j+1] = '.'
            temp_state[i+2][j+2] = tile
            ## print("jump to down-right")
            if terminateCheck:
                return True
            jump_finder(temp_state, tile, i+2, j+2, successors, False)
        if (tile == 'B'):
            # BLACK KING can jump to up-left
            if (i-1 >= 0 and j-1 >= 0 and (state[i-1][j-1] == 'r' or state[i-1][j-1] == 'R') and i-2 >= 0 and j-2 >= 0 and state[i-2][j-2] == '.'):
                isJump = True
                temp_state = copy.deepcopy(state)
                temp_state[i][j] = '.'
                temp_state[i-1][j-1] = '.'
                temp_state[i-2][j-2] = tile
                ## print("jump to up-left")
                if terminateCheck:
                    return True
                jump_finder(temp_state, tile, i-2, j-2, successors, False)
            # BLACK KING can jump to up-right
            if (i-1 >= 0 and j+1 < 8 and (state[i-1][j+1] == 'r' or state[i-1][j+1] == 'R') and i-2 >= 0 and j+2 < 8 and state[i-2][j+2] == '.'):
                isJump = True
                temp_state = copy.deepcopy(state)
                temp_state[i][j] = '.'
                temp_state[i-1][j+1] = '.'
                temp_state[i-2][j+2] = tile
                ## print("jump to up-right")
                if terminateCheck:
                    return True
                jump_finder(temp_state, tile, i-2, j+2, successors, False)
    if (not isJump and not firstCall):
        if (tile == 'r' or tile == 'R'):
            successors.put((-1 * utility(state), successors.qsize(), state))
        else:
            successors.put((utility(state), successors.qsize(), state))
        return False
    return False

# Find all possible successors
def successors(state:list, isRed:bool, terminateCheck:bool=False) -> PriorityQueue:
    successors = PriorityQueue()
    # Change to inscending or descending depends on player
    priority_parameter = -1 if isRed else 1
    
    # First check if the player can jump
    for i in range(8):
        for j in range(8):
            # Continue if no tile on the location, or the tile is not current payler's
            if (state[i][j] == '.' or (isRed and (state[i][j] == 'b' or state[i][j] == 'B')) or (not isRed and (state[i][j] == 'r' or state[i][j] == 'R'))):
                continue
            if (jump_finder(state, state[i][j], i, j, successors, True, terminateCheck)):
                successors.put((0,0))
                return successors
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
                    if terminateCheck:
                        return successors
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
                    if terminateCheck:
                        return successors
                # RED KING can move down-left
                if (state[i][j] == 'R' and i+1 < 8 and j-1 >= 0 and state[i+1][j-1] == '.'):
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = '.'
                    new_state[i+1][j-1] = state[i][j]
                    successors.put((priority_parameter * utility(new_state), successors.qsize(), new_state))
                    if terminateCheck:
                        return successors
                # RED KING can move down-right
                if (state[i][j] == 'R' and i+1 < 8 and j+1 < 8 and state[i+1][j+1] == '.'):
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = '.'
                    new_state[i+1][j+1] = state[i][j]
                    successors.put((priority_parameter * utility(new_state), successors.qsize(), new_state))
                    if terminateCheck:
                        return successors
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
                    if terminateCheck:
                        return successors
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
                    if terminateCheck:
                        return successors
                # BLACK KING can move up-left
                if (state[i][j] == 'B' and i-1 >= 0 and j-1 >= 0 and state[i-1][j-1] == '.'):
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = '.'
                    new_state[i-1][j-1] = state[i][j]
                    successors.put((priority_parameter * utility(new_state), successors.qsize(), new_state))
                    if terminateCheck:
                        return successors
                # BLACK KING can move up-right
                if (state[i][j] == 'B' and i-1 >= 0 and j+1 < 8 and state[i-1][j+1] == '.'):
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = '.'
                    new_state[i-1][j+1] = state[i][j]
                    successors.put((priority_parameter * utility(new_state), successors.qsize(), new_state))
                    if terminateCheck:
                        return successors
    return successors

# Alpha-Beta Pruning Implementation
def AlphaBeta(state:list, isRed:bool, alpha:int, beta:int, depth:int) -> tuple[list, int]:
    global depth_limit
    best_move = None
    # Check whether we reach the depth limit or the game has ended
    if (depth == depth_limit or is_game_end(state, isRed)):
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
        # print('Wrong input/output parameters...')
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
    # print('=================='+ input_file + '=================')
    # for i in initial_state:
    #     print(i)

    # print('==========================================')
    next_move, __ = AlphaBeta(initial_state, True, -inf, inf, 0)
    if (next_move == None):
        # print("Game already ended")
        next_move = initial_state
    # for i in next_move:
    #     print(i)

    with open(output_file, 'w', encoding='utf-8') as f:
        text = ''
        for row in next_move:
            text += ''.join(row)
            text += '\n'
        f.write(text.strip())

        

            




