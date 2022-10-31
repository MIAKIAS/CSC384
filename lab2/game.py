import subprocess
import sys
import os
import copy
import time


BOARD_SIZE = 8


def print_helper(board):
    for i in board:
        print(i)
    print('\n')


def successor(board, side, capture=False, x=0, y=0):

    if side == 'b' or side == 'B':
        can_move_down = ['b', 'B']
        can_move_up = ['B']
        opponent = ['r', 'R']
    else:
        can_move_down = ['R']
        can_move_up = ['r', 'R']
        opponent = ['b', 'B']

    if x == 0 and y == 0:
        x_start = 0
        x_end = BOARD_SIZE
        y_start = 0
        y_end = BOARD_SIZE
    else:
        x_start = x
        x_end = x+1
        y_start = y
        y_end = y+1

    successors, successors_no_cap = [], []
    captured = False

    # loop over board
    for i in range(y_start, y_end):
        for j in range(x_start, x_end):

            # bottom
            if board[i][j] in can_move_down:

                # bottom left
                if i < BOARD_SIZE - 1 and j > 0:
                    # empty
                    if board[i+1][j-1] == '.' and not capture:
                        temp_board = copy.deepcopy(board)
                        if i == BOARD_SIZE - 2 and temp_board[i][j] == 'b':
                            temp_board[i+1][j-1] = 'B'
                        else:
                            temp_board[i+1][j-1] = temp_board[i][j]
                        temp_board[i][j] = '.'
                        successors_no_cap.append(temp_board)
                    # capture
                    elif i < BOARD_SIZE - 2 and j > 1:
                        if board[i+1][j-1] in opponent:
                            if board[i+2][j-2] == '.':
                                captured = True
                                temp_board = copy.deepcopy(board)
                                if i == BOARD_SIZE - 3 and temp_board[i][j] == 'b':
                                    temp_board[i+2][j-2] = 'B'
                                else:
                                    temp_board[i+2][j-2] = temp_board[i][j]
                                temp_board[i+1][j-1] = '.'
                                temp_board[i][j] = '.'
                                multi_cap = successor(temp_board, side, True, j-2, i+2)
                                if (len(multi_cap)):
                                    successors.extend(multi_cap)
                                else:
                                    successors.append(temp_board)

                # bottom right
                if i < BOARD_SIZE - 1 and j < BOARD_SIZE - 1:
                    # empty
                    if board[i+1][j+1] == '.' and not capture:
                        temp_board = copy.deepcopy(board)
                        if i == BOARD_SIZE - 2 and temp_board[i][j] == 'b':
                            temp_board[i+1][j+1] = 'B'
                        else:
                            temp_board[i+1][j+1] = temp_board[i][j]
                        temp_board[i][j] = '.'
                        successors_no_cap.append(temp_board)
                    # capture
                    elif i < BOARD_SIZE - 2 and j < BOARD_SIZE - 2:
                        if board[i+1][j+1] in opponent:
                            if board[i+2][j+2] == '.':
                                captured = True
                                temp_board = copy.deepcopy(board)
                                if i == BOARD_SIZE - 3 and temp_board[i][j] == 'b':
                                    temp_board[i+2][j+2] = 'B'
                                else:
                                    temp_board[i+2][j+2] = temp_board[i][j]
                                temp_board[i+1][j+1] = '.'
                                temp_board[i][j] = '.'
                                multi_cap = successor(temp_board, side, True, j+2, i+2)
                                if (len(multi_cap)):
                                    successors.extend(multi_cap)
                                else:
                                    successors.append(temp_board)

            # top
            if board[i][j] in can_move_up:

                # top left
                if i > 0 and j > 0:
                    # empty
                    if board[i-1][j-1] == '.' and not capture:
                        temp_board = copy.deepcopy(board)
                        if i == 1 and temp_board[i][j] == 'r':
                            temp_board[i-1][j-1] = 'R'
                        else:
                            temp_board[i-1][j-1] = temp_board[i][j]
                        temp_board[i][j] = '.'
                        successors_no_cap.append(temp_board)
                    # capture
                    elif i > 1 and j > 1:
                        if board[i-1][j-1] in opponent:
                            if board[i-2][j-2] == '.':
                                captured = True
                                temp_board = copy.deepcopy(board)
                                if i == 2 and temp_board[i][j] == 'r':
                                    temp_board[i-2][j-2] = 'R'
                                else:
                                    temp_board[i-2][j-2] = temp_board[i][j]
                                temp_board[i-1][j-1] = '.'
                                temp_board[i][j] = '.'
                                multi_cap = successor(temp_board, side, True, j-2, i-2)
                                if (len(multi_cap)):
                                    successors.extend(multi_cap)
                                else:
                                    successors.append(temp_board)

                # top right
                if i > 0 and j < BOARD_SIZE - 1:
                    # empty
                    if board[i-1][j+1] == '.' and not capture:
                        temp_board = copy.deepcopy(board)
                        if i == 1 and temp_board[i][j] == 'r':
                            temp_board[i-1][j+1] = 'R'
                        else:
                            temp_board[i-1][j+1] = temp_board[i][j]
                        temp_board[i][j] = '.'
                        successors_no_cap.append(temp_board)
                    # capture
                    elif i > 1 and j < BOARD_SIZE - 2:
                        if board[i-1][j+1] in opponent:
                            if board[i-2][j+2] == '.':
                                captured = True
                                temp_board = copy.deepcopy(board)
                                if i == 2 and temp_board[i][j] == 'r':
                                    temp_board[i-2][j+2] = 'R'
                                else:
                                    temp_board[i-2][j+2] = temp_board[i][j]
                                temp_board[i-1][j+1] = '.'
                                temp_board[i][j] = '.'
                                multi_cap = successor(temp_board, side, True, j+2, i-2)
                                if (len(multi_cap)):
                                    successors.extend(multi_cap)
                                else:
                                    successors.append(temp_board)

    if not captured:
        return successors_no_cap

    return successors
    

# .b.b.b.b
# b.b.b.b.
# .b.b.b.b
# ........
# ........
# r.r.r.r.
# .r.r.r.r
# r.r.r.r.

# 1 moves first as red, 2 as black
checker_ai_1 = ["python3", "lab2/checkers_ultility.py", "input1.txt", "input1.txt"]
checker_ai_2 = ["python3", "lab2/checkers.py", "input2.txt", "input2.txt"]

# print start board
board = []
with open("lab2/checkers_validate/input_test.txt") as f:
    board = [[c for c in line.strip()] for line in f.readlines()]
print_helper(board)

# store start board to input1
with open("input1.txt", 'w') as f:
    for i in board:
        for j in i:
            f.write(j)
        f.write('\n')

move = 0

while (len(successor(board, 'r')) != 0 and len(successor(board, 'b')) != 0):

    # checker 1 moves and store in input1.txt
    start = time.time()
    subprocess.run(checker_ai_1)
    print("Time:", time.time() - start)
    if (time.time() - start >= 100):
        assert("Timeout")
        exit(1)
    move += 1

    # print checker 1 move
    board = []
    with open("input1.txt") as f:
        board = [[c for c in line.strip()] for line in f.readlines()]
    print("AI 1 Move:", move)
    print_helper(board)

    # convert b and r and store in input2.txt
    for i in range(4):
        for j in range(8):
            temp = board[i][j]
            board[i][j] = board[7-i][7-j]
            board[7-i][7-j] = temp
    for i in range(8):
        for j in range(8):
            if board[i][j] == 'r':
                board[i][j] = 'b'
            elif board[i][j] == 'b':
                board[i][j] = 'r'
            elif board[i][j] == 'R':
                board[i][j] = 'B'
            elif board[i][j] == 'B':
                board[i][j] = 'R'
    with open("input2.txt", 'w') as f:
        for i in board:
            for j in i:
                f.write(j)
            f.write('\n')

    # checker 2 moves and store in input2.txt
    start = time.time()
    subprocess.run(checker_ai_2)
    print("Time:", time.time() - start)
    if (time.time() - start >= 100):
        assert("Timeout")
        exit(1)
    move += 1

    # load input2.txt
    board = []
    with open("input2.txt") as f:
        board = [[c for c in line.strip()] for line in f.readlines()]

    # convert b and r and store in input1.txt
    for i in range(4):
        for j in range(8):
            temp = board[i][j]
            board[i][j] = board[7-i][7-j]
            board[7-i][7-j] = temp
    for i in range(8):
        for j in range(8):
            if board[i][j] == 'r':
                board[i][j] = 'b'
            elif board[i][j] == 'b':
                board[i][j] = 'r'
            elif board[i][j] == 'R':
                board[i][j] = 'B'
            elif board[i][j] == 'B':
                board[i][j] = 'R'
    with open("input1.txt", 'w') as f:
        for i in board:
            for j in i:
                f.write(j)
            f.write('\n')

    # print checker 2 move
    print("AI 2 Move:", move)
    print_helper(board)