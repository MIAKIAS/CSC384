'''
    Fall 2022 - CSC384 - Lab3
    Author: Weizhou Wang
    Student#: 1004421262
    Usage: 6.7s all testcases
'''
from sys import argv
import heapq
import copy

# Tile limit per column
COL_LIMIT = list()
# Tile limit per row
ROW_LIMIT = list()
# Number limit per type of ships
SHIP_LIMIT = list()
# Total number of types of ships
NUMBER_TYPES_SHIPS = int()
# Size of the grid
SIZE = int()
# Parameter for 1x1 ship in Priority queue
INDEX_1X1 = 2
# Tie-breaker for the PriorityQueue
priority_index = 0

# Class for storing ships
class Ship:
    # Type/length of the ship
    length = int()
    # Domain of the ship
    domain_row = set()
    domain_col = set()
    # The constructor
    def __init__(self, length, domain_row=None, domain_col=None):
        self.length = length
        self.domain_row = domain_row
        self.domain_col = domain_col

# Class for a state
class State:
    # The constructor
    def __init__(self):
        # Current number of tiles in each row/col
        self.cur_row = [0] * SIZE
        self.cur_col = [0] * SIZE
        # Ship status in the current state
        self.ships = list()
        # Need to be aligned with the intial value
        self.init_value = set()

# The Forward Checking Algorithm
def FC(state:State, ans:list):
    # Return if all variables are assigned
    if (len(state.ships) == 0):
        return ans

    # Pop an unassigned variable
    cur_ship:Ship = heapq.heappop(state.ships)[2]
    '''============================================Horizontal Placement============================================'''
    for row_value in cur_ship.domain_row.copy():
        row = row_value[0]
        col = row_value[1]
        
        # Update the counts
        new_state = copy.deepcopy(state)
        new_state.cur_row[row] += cur_ship.length
        new_state.cur_col[col] += 1
        if (cur_ship.length > 1):
            new_state.cur_col[col+1] += 1
        if (cur_ship.length > 2):
            new_state.cur_col[col+2] += 1
        if (cur_ship.length > 3):
            new_state.cur_col[col+3] += 1

        # Calculate the values that needs to be removed
        remove_set_1 = set()
        remove_set_2_row = set()
        remove_set_2_col = set()
        remove_set_3_row = set()
        remove_set_3_col = set()
        remove_set_4_row = set()
        remove_set_4_col = set()

        for i in range(-1, 2):
            remove_set_2_row.add((row+i, col-2))
            remove_set_3_row.add((row+i, col-3))
            remove_set_4_row.add((row+i, col-4))
            for j in range(-1,cur_ship.length+1):
                remove_set_1.add((row+i, col+j))
        for j in range(-1, cur_ship.length+1):
            remove_set_2_col.add((row-2, col+j))
            remove_set_3_col.add((row-3, col+j))
            remove_set_4_col.add((row-4, col+j))

        # Remove values after placing this ship
        DWO = False
        for ship in new_state.ships:
            ship[2].domain_row -= remove_set_1
            if (ship[2].length > 1):
                ship[2].domain_col -= remove_set_1
                ship[2].domain_col -= remove_set_2_col
                ship[2].domain_row -= remove_set_2_row
                if (ship[2].length > 2):
                    ship[2].domain_row -= remove_set_3_row
                    ship[2].domain_col -= remove_set_3_col
                if (ship[2].length > 3):
                    ship[2].domain_row -= remove_set_4_row
                    ship[2].domain_col -= remove_set_4_col
                if (len(ship[2].domain_col) == 0 and len(ship[2].domain_row) == 0):
                    DWO = True
                    break
                ship[0] = len(ship[2].domain_col) + len(ship[2].domain_row)
            else:
                if (len(ship[2].domain_row) == 0):
                    DWO = True
                    break
                ship[0] = len(ship[2].domain_row) * INDEX_1X1
        # If DWO, try next value
        if (DWO):
            continue

        # Remove any unassigned ships that will exceed the sums
        remove_row_1 = set()
        remove_col_1 = set()
        remove_row_2 = set()
        remove_col_2 = set()
        remove_row_3 = set()
        remove_col_3 = set()
        remove_row_4 = set()
        remove_col_4 = set()
        row_diff = ROW_LIMIT[row] - new_state.cur_row[row]
        col_diff = COL_LIMIT[col] - new_state.cur_col[col]
        col_diff2 = int()
        col_diff3 = int()
        col_diff4 = int()
        if (cur_ship.length > 1):
            col_diff2 = COL_LIMIT[col+1] - new_state.cur_col[col+1]
            if (cur_ship.length > 2):
                col_diff3 = COL_LIMIT[col+2] - new_state.cur_col[col+2]
                if (cur_ship.length > 3):
                    col_diff4 = COL_LIMIT[col+3] - new_state.cur_col[col+3]
        if (row_diff < 4):
            remove_row_4.add(row)
            if (row_diff < 3):
                remove_row_3.add(row)
                if (row_diff < 2):
                    remove_row_2.add(row)
                    if (row_diff < 1):
                        remove_row_1.add(row)
        if (col_diff < 4):
            remove_col_4.add(col)
            if (col_diff < 3):
                remove_col_3.add(col)
                if (col_diff < 2):
                    remove_col_2.add(col)
                    if (col_diff < 1):
                        remove_col_1.add(col)
        if (cur_ship.length > 1):
            if (col_diff2 < 4):
                remove_col_4.add(col+1)
                if (col_diff2 < 3):
                    remove_col_3.add(col+1)
                    if (col_diff2 < 2):
                        remove_col_2.add(col+1)
                        if (col_diff2 < 1):
                            remove_col_1.add(col+1)
            if (cur_ship.length > 2):
                if (col_diff3 < 4):
                    remove_col_4.add(col+2)
                    if (col_diff3 < 3):
                        remove_col_3.add(col+2)
                        if (col_diff3 < 2):
                            remove_col_2.add(col+2)
                            if (col_diff3 < 1):
                                remove_col_1.add(col+2)
                if (cur_ship.length > 3):
                    if (col_diff4 < 4):
                        remove_col_4.add(col+3)
                        if (col_diff4 < 3):
                            remove_col_3.add(col+3)
                            if (col_diff4 < 2):
                                remove_col_2.add(col+3)
                                if (col_diff4 < 1):
                                    remove_col_1.add(col+3)

        DWO = False
        for ship in new_state.ships:
            ship = ship[2]
            if (ship.length == 1):
                for value in ship.domain_row.copy():
                    if (value[0] in remove_row_1 or value[1] in remove_col_1):
                        ship.domain_row.remove(value)
                        if (len(ship.domain_row) == 0):
                            DWO = True
                            break
            elif (ship.length == 2):
                for value in ship.domain_row.copy():
                    if (value[0] in remove_row_2 or value[1] in remove_col_1 or value[1]+1 in remove_col_1):
                        ship.domain_row.remove(value)
                for value in ship.domain_col.copy():
                    if (value[1] in remove_col_2 or value[0] in remove_row_1 or value[0]+1 in remove_row_1):
                        ship.domain_col.remove(value)
                        if (len(ship.domain_col) == 0 and len(ship.domain_row) == 0):
                            DWO = True
                            break
            elif (ship.length == 3):
                for value in ship.domain_row.copy():
                    if (value[0] in remove_row_3 or value[1] in remove_col_1 or value[1]+1 in remove_col_1 or value[1]+2 in remove_col_1):
                        ship.domain_row.remove(value)
                for value in ship.domain_col.copy():
                    if (value[1] in remove_col_3 or value[0] in remove_row_1 or value[0]+1 in remove_row_1 or value[0]+2 in remove_row_1):
                        ship.domain_col.remove(value)
                        if (len(ship.domain_col) == 0 and len(ship.domain_row) == 0):
                            DWO = True
                            break
            elif (ship.length == 4):
                for value in ship.domain_row.copy():
                    if (value[0] in remove_row_4 or value[1] in remove_col_1 or value[1]+1 in remove_col_1 or value[1]+2 in remove_col_1 or value[1]+3 in remove_col_1):
                        ship.domain_row.remove(value)
                for value in ship.domain_col.copy():
                    if (value[1] in remove_col_4 or value[0] in remove_row_1 or value[0]+1 in remove_row_1 or value[0]+2 in remove_row_1 or value[0]+3 in remove_row_1):
                        ship.domain_col.remove(value)
                        if (len(ship.domain_col) == 0 and len(ship.domain_row) == 0):
                            DWO = True
                            break
            if (DWO):
                break
        if (DWO):
            continue

        # Check if we can still align with the initialized values
        if (len(new_state.init_value) != 0):
            # The current placement may achieve some of the values
            if (cur_ship.length == 1):
                new_state.init_value.discard(('S', row, col))
            elif (cur_ship.length == 2):
                new_state.init_value.discard(('L', row, col))
                new_state.init_value.discard(('R', row, col+1))
            elif (cur_ship.length == 3):
                new_state.init_value.discard(('L', row, col))
                new_state.init_value.discard(('M', row, col+1))
                new_state.init_value.discard(('R', row, col+2))
            elif (cur_ship.length == 4):
                new_state.init_value.discard(('L', row, col))
                new_state.init_value.discard(('M', row, col+1))
                new_state.init_value.discard(('M', row, col+2))
                new_state.init_value.discard(('R', row, col+3))
            
            # Check if the remaining values can be covered
            temp_ships = list()
            for item in new_state.ships:
                if (item[2].length > 1):
                    temp_ships.append(item[2])
            temp_init = new_state.init_value.copy()
            if (not initialization_checker(temp_ships, temp_init)):
                cur_ship.domain_row.remove(row_value)
                continue
        
        # If everything is good, we go to the next level
        if (cur_ship.length == 1):
            next_ans = ans.copy()
            next_ans.append(('S', row, col))
            result = FC(new_state, next_ans)
            if (result != None):
                return result
        elif (cur_ship.length == 2):
            next_ans = ans.copy()
            next_ans.extend([('L', row, col), ('R', row, col+1)])
            result = FC(new_state, next_ans)
            if (result != None):
                return result
        elif (cur_ship.length == 3):
            next_ans = ans.copy()
            next_ans.extend([('L', row, col), ('M', row, col+1), ('R', row, col+2)])
            result = FC(new_state, next_ans)
            if (result != None):
                return result
        else:
            next_ans = ans.copy()
            next_ans.extend([('L', row, col), ('M', row, col+1), ('M', row, col+2), ('R', row, col+3)])
            result = FC(new_state, next_ans)
            if (result != None):
                return result

    '''============================================Vertical Placement============================================'''
    if (cur_ship.length > 1):
        for col_value in cur_ship.domain_col.copy():
            row = col_value[0]
            col = col_value[1]

            # Update the counts
            new_state = copy.deepcopy(state)
            new_state.cur_col[col] += cur_ship.length
            new_state.cur_row[row] += 1
            new_state.cur_row[row+1] += 1
            if (cur_ship.length > 2):
                new_state.cur_row[row+2] += 1
            if (cur_ship.length > 3):
                new_state.cur_row[row+3] += 1

            # Calculate the values that needs to be removed
            remove_set_1 = set()
            remove_set_2_row = set()
            remove_set_2_col = set()
            remove_set_3_row = set()
            remove_set_3_col = set()
            remove_set_4_row = set()
            remove_set_4_col = set()

            for i in range(-1, cur_ship.length+1):
                remove_set_2_row.add((row+i, col-2))
                remove_set_3_row.add((row+i, col-3))
                remove_set_4_row.add((row+i, col-4))
                for j in range(-1, 2):
                    remove_set_1.add((row+i, col+j))
            for j in range(-1, 2):
                remove_set_2_col.add((row-2, col+j))
                remove_set_3_col.add((row-3, col+j))
                remove_set_4_col.add((row-4, col+j))

            # Remove values after placing this ship
            DWO = False
            for ship in new_state.ships:
                ship[2].domain_row -= remove_set_1
                if (ship[2].length > 1):
                    ship[2].domain_row -= remove_set_2_row
                    ship[2].domain_col -= remove_set_1
                    ship[2].domain_col -= remove_set_2_col
                    if (ship[2].length > 2):
                        ship[2].domain_row -= remove_set_3_row
                        ship[2].domain_col -= remove_set_3_col
                    if (ship[2].length > 3):
                        ship[2].domain_row -= remove_set_4_row
                        ship[2].domain_col -= remove_set_4_col
                    if (len(ship[2].domain_col) == 0 and len(ship[2].domain_row) == 0):
                        DWO = True
                        break
                    ship[0] = len(ship[2].domain_col) + len(ship[2].domain_row)
                else:
                    if (len(ship[2].domain_row) == 0):
                        DWO = True
                        break
                    ship[0] = len(ship[2].domain_row) * INDEX_1X1
            # If DWO, try next value
            if (DWO):
                continue

            # Remove any unassigned ships that will exceed the sums
            remove_row_1 = set()
            remove_col_1 = set()
            remove_row_2 = set()
            remove_col_2 = set()
            remove_row_3 = set()
            remove_col_3 = set()
            remove_row_4 = set()
            remove_col_4 = set()
            row_diff = ROW_LIMIT[row] - new_state.cur_row[row]
            col_diff = COL_LIMIT[col] - new_state.cur_col[col]
            row_diff2 = int()
            row_diff3 = int()
            row_diff4 = int()
            if (cur_ship.length > 1):
                row_diff2 = ROW_LIMIT[row+1] - new_state.cur_row[row+1]
                if (cur_ship.length > 2):
                    row_diff3 = ROW_LIMIT[row+2] - new_state.cur_row[row+2]
                    if (cur_ship.length > 3):
                        row_diff4 = ROW_LIMIT[row+3] - new_state.cur_row[row+3]
            if (col_diff < 4):
                remove_col_4.add(col)
                if (col_diff < 3):
                    remove_col_3.add(col)
                    if (col_diff < 2):
                        remove_col_2.add(col)
                        if (col_diff < 1):
                            remove_col_1.add(col)
            if (row_diff < 4):
                remove_row_4.add(row)
                if (row_diff < 3):
                    remove_row_3.add(row)
                    if (row_diff < 2):
                        remove_row_2.add(row)
                        if (row_diff < 1):
                            remove_row_1.add(row)
            if (cur_ship.length > 1):
                if (row_diff2 < 4):
                    remove_row_4.add(row+1)
                    if (row_diff2 < 3):
                        remove_row_3.add(row+1)
                        if (row_diff2 < 2):
                            remove_row_2.add(row+1)
                            if (row_diff2 < 1):
                                remove_row_1.add(row+1)
                if (cur_ship.length > 2):
                    if (row_diff3 < 4):
                        remove_row_4.add(row+2)
                        if (row_diff3 < 3):
                            remove_row_3.add(row+2)
                            if (row_diff3 < 2):
                                remove_row_2.add(row+2)
                                if (row_diff3 < 1):
                                    remove_row_1.add(row+2)
                    if (cur_ship.length > 3):
                        if (row_diff4 < 4):
                            remove_row_4.add(row+3)
                            if (row_diff4 < 3):
                                remove_row_3.add(row+3)
                                if (row_diff4 < 2):
                                    remove_row_2.add(row+3)
                                    if (row_diff4 < 1):
                                        remove_row_1.add(row+3)

            DWO = False
            for ship in new_state.ships:
                ship = ship[2]
                if (ship.length == 1):
                    for value in ship.domain_row.copy():
                        if (value[0] in remove_row_1 or value[1] in remove_col_1):
                            ship.domain_row.remove(value)
                            if (len(ship.domain_row) == 0):
                                DWO = True
                                break
                elif (ship.length == 2):
                    for value in ship.domain_row.copy():
                        if (value[0] in remove_row_2 or value[1] in remove_col_1 or value[1]+1 in remove_col_1):
                            ship.domain_row.remove(value)
                    for value in ship.domain_col.copy():
                        if (value[1] in remove_col_2 or value[0] in remove_row_1 or value[0]+1 in remove_row_1):
                            ship.domain_col.remove(value)
                            if (len(ship.domain_col) == 0 and len(ship.domain_row) == 0):
                                DWO = True
                                break
                elif (ship.length == 3):
                    for value in ship.domain_row.copy():
                        if (value[0] in remove_row_3 or value[1] in remove_col_1 or value[1]+1 in remove_col_1 or value[1]+2 in remove_col_1):
                            ship.domain_row.remove(value)
                    for value in ship.domain_col.copy():
                        if (value[1] in remove_col_3 or value[0] in remove_row_1 or value[0]+1 in remove_row_1 or value[0]+2 in remove_row_1):
                            ship.domain_col.remove(value)
                            if (len(ship.domain_col) == 0 and len(ship.domain_row) == 0):
                                DWO = True
                                break
                elif (ship.length == 4):
                    for value in ship.domain_row.copy():
                        if (value[0] in remove_row_4 or value[1] in remove_col_1 or value[1]+1 in remove_col_1 or value[1]+2 in remove_col_1 or value[1]+3 in remove_col_1):
                            ship.domain_row.remove(value)
                    for value in ship.domain_col.copy():
                        if (value[1] in remove_col_4 or value[0] in remove_row_1 or value[0]+1 in remove_row_1 or value[0]+2 in remove_row_1 or value[0]+3 in remove_row_1):
                            ship.domain_col.remove(value)
                            if (len(ship.domain_col) == 0 and len(ship.domain_row) == 0):
                                DWO = True
                                break
                if (DWO):
                    break
            if (DWO):
                continue

            # Check if we can still align with the initialized values
            if (len(new_state.init_value) != 0):
                # The current placement may achieve some of the values
                if (cur_ship.length == 2):
                    new_state.init_value.discard(('T', row, col))
                    new_state.init_value.discard(('B', row+1, col))
                elif (cur_ship.length == 3):
                    new_state.init_value.discard(('T', row, col))
                    new_state.init_value.discard(('M', row+1, col))
                    new_state.init_value.discard(('B', row+2, col))
                elif (cur_ship.length == 4):
                    new_state.init_value.discard(('T', row, col))
                    new_state.init_value.discard(('M', row+1, col))
                    new_state.init_value.discard(('M', row+2, col))
                    new_state.init_value.discard(('B', row+3, col))
                
                # Check if the remaining values can be covered
                temp_ships = list()
                for item in new_state.ships:
                    if (item[2].length > 1):
                        temp_ships.append(item[2])
                temp_init = new_state.init_value.copy()
                if (not initialization_checker(temp_ships, temp_init)):
                    cur_ship.domain_col.remove(col_value)
                    # If DWO, we need to backtrack
                    if (len(cur_ship.domain_col) == 0):
                        return None
                    continue

            # If everything is good, we go to the next level
            if (cur_ship.length == 2):
                next_ans = ans.copy()
                next_ans.extend([('T', row, col), ('B', row+1, col)])
                result = FC(new_state, next_ans)
                if (result != None):
                    return result
            elif (cur_ship.length == 3):
                next_ans = ans.copy()
                next_ans.extend([('T', row, col), ('M', row+1, col), ('B', row+2, col)])
                result = FC(new_state, next_ans)
                if (result != None):
                    return result
            else:
                next_ans = ans.copy()
                next_ans.extend([('T', row, col), ('M', row+1, col), ('M', row+2, col), ('B', row+3, col)])
                result = FC(new_state, next_ans)
                if (result != None):
                    return result

    return None

# Helper function for checking initialized values
# parameters: shallow copies of the originals
def initialization_checker(ships:list, init_values:set) -> bool:
    if (len(init_values) == 0):
        return True
    elif (len(ships) == 0):
        return False
    else:
        init_item = init_values.pop()

    # Handle different values
    if (init_item[0] == 'L'):
        for ship in ships:
            if ((init_item[1], init_item[2]) in ship.domain_row):
                temp_ships = ships.copy()
                temp_ships.remove(ship)
                if (initialization_checker(temp_ships, init_values.copy())):
                    return True
        return False
    elif (init_item[0] == 'R'):
        for ship in ships:
            if (ship.length == 2 and ((init_item[1], init_item[2]-1) in ship.domain_row)) \
                or (ship.length == 3 and ((init_item[1], init_item[2]-2) in ship.domain_row)) \
                    or (ship.length == 4 and ((init_item[1], init_item[2]-3) in ship.domain_row)):
                temp_ships = ships.copy()
                temp_ships.remove(ship)
                if (initialization_checker(temp_ships, init_values.copy())):
                    return True
        return False
    elif (init_item[0] == 'T'):
        for ship in ships:
            if ((init_item[1], init_item[2]) in ship.domain_col):
                temp_ships = ships.copy()
                temp_ships.remove(ship)
                if (initialization_checker(temp_ships, init_values.copy())):
                    return True
        return False
    elif (init_item[0] == 'B'):
        for ship in ships:
            if (ship.length == 2 and ((init_item[1]-1, init_item[2]) in ship.domain_col)) \
                or (ship.length == 3 and ((init_item[1]-2, init_item[2]) in ship.domain_col)) \
                    or (ship.length == 4 and ((init_item[1]-3, init_item[2]) in ship.domain_col)):
                temp_ships = ships.copy()
                temp_ships.remove(ship)
                if (initialization_checker(temp_ships, init_values.copy())):
                    return True
        return False
    else: #'M'
        for ship in ships:
            if (ship.length > 2) \
                and (\
                    ((init_item[1], init_item[2]-1) in ship.domain_row) \
                    or (ship.length == 4 and ((init_item[1], init_item[2]-2) in ship.domain_row)) \
                        or ((init_item[1]-1, init_item[2]) in ship.domain_col) \
                            or (ship.length == 4 and ((init_item[1]-2, init_item[2]) in ship.domain_col))\
                                ):
                temp_ships = ships.copy()
                temp_ships.remove(ship)
                if (initialization_checker(temp_ships, init_values.copy())):
                    return True
        return False

if __name__ == "__main__":
    if len(argv) != 3:
        print('Wrong input/output parameters...')
        exit(1)

    # Read in the input/output file names
    __, input_file, output_file = argv

    # input_file = "/h/u17/c1/00/wangw222/csc384/lab3/battle_validate/0.txt"
    # output_file = "/h/u17/c1/00/wangw222/csc384/lab3/0out.txt"

    grid = list()
    with open(input_file, 'r', encoding='utf-8') as f:
        # Read constraint parameters
        ROW_LIMIT = [int(i) for i in list(f.readline().strip())]
        COL_LIMIT = [int(i) for i in list(f.readline().strip())]
        SHIP_LIMIT = [int(i) for i in list(f.readline().strip())]
        NUMBER_TYPES_SHIPS = len(SHIP_LIMIT)

        # Read initial state and add paddings
        for line in f:
            grid.append(list(line.strip()))

    SIZE = len(grid[0])
    # for i in grid:
    #     print(i)
    # print("==================================")

    # Preprocessing, set zero-col and zero-row to 'W'
    for i in range(SIZE):
        if (ROW_LIMIT[i] == 0):
            for j in range(SIZE):
                grid[i][j] = 'W'
        if (COL_LIMIT[i] == 0):
            for j in range(SIZE):
                grid[j][i] = 'W'
    # for i in grid:
    #     print(i)
    # print("=================================")

    # Initialize the domain of ships
    domain_1x1 = set()
    domain_1x2_row = set()
    domain_1x2_col = set()
    domain_1x3_row = set()
    domain_1x3_col = set()
    domain_1x4_row = set()
    domain_1x4_col = set()

    # Read in the possible domain
    num_init_1x1 = 0
    init_state = State()
    for i in range(SIZE):
        for j in range(SIZE):
            if (grid[i][j] == 'W'):
                continue
            elif (grid[i][j] == '0'):
                if (ROW_LIMIT[i] >= 1 and COL_LIMIT[j] >= 1):
                    domain_1x1.add((i,j))
            # Directly assign values to one 1x1 ship
            elif (grid[i][j] == 'S'):
                num_init_1x1 += 1
                heapq.heappush(init_state.ships, [1, priority_index, Ship(1, {(i,j)})])
                priority_index += 1
                continue
            # We need to check later if the rest of the initialized values are aligned with our assignments
            else:
                init_state.init_value.add((grid[i][j], i, j))

            if (NUMBER_TYPES_SHIPS >= 2):
                if (j+1 < SIZE and (grid[i][j] == '0' or grid[i][j] == 'L') and (grid[i][j+1] == '0' or grid[i][j+1] == 'R')):
                    if (ROW_LIMIT[i] >= 2 and COL_LIMIT[j] >= 1 and COL_LIMIT[j+1] >= 1):
                        domain_1x2_row.add((i,j))
                if (i+1 < SIZE and (grid[i][j] == '0' or grid[i][j] == 'T') and (grid[i+1][j] == '0' or grid[i+1][j] == 'B')):
                    if (COL_LIMIT[j] >= 2 and ROW_LIMIT[i] >= 1 and ROW_LIMIT[i+1] >= 1):
                        domain_1x2_col.add((i,j))
            if (NUMBER_TYPES_SHIPS >= 3):
                if (j+2 < SIZE and (grid[i][j] == '0' or grid[i][j] == 'L') and (grid[i][j+1] == '0' or grid[i][j+1] == 'M') and (grid[i][j+2] == '0' or grid[i][j+2] == 'R')):
                    if (ROW_LIMIT[i] >= 3 and COL_LIMIT[j] >= 1 and COL_LIMIT[j+1] >= 1 and COL_LIMIT[j+2] >= 1):
                        domain_1x3_row.add((i,j))
                if (i+2 < SIZE and (grid[i][j] == '0' or grid[i][j] == 'T') and (grid[i+1][j] == '0' or grid[i+1][j] == 'M') and (grid[i+2][j] == '0' or grid[i+2][j] == 'B')):
                    if (COL_LIMIT[j] >= 3 and ROW_LIMIT[i] >= 1 and ROW_LIMIT[i+1] >= 1 and ROW_LIMIT[i+2] >= 1):
                        domain_1x3_col.add((i,j))
            if (NUMBER_TYPES_SHIPS >= 4):
                if (j+3 < SIZE and (grid[i][j] == '0' or grid[i][j] == 'L') and (grid[i][j+1] == '0' or grid[i][j+1] == 'M') and (grid[i][j+2] == '0' or grid[i][j+2] == 'M') and (grid[i][j+3] == '0' or grid[i][j+3] == 'R')):
                    if (ROW_LIMIT[i] >= 4 and COL_LIMIT[j] >= 1 and COL_LIMIT[j+1] >= 1 and COL_LIMIT[j+2] >= 1 and COL_LIMIT[j+3] >= 1):
                        domain_1x4_row.add((i,j))
                if (i+3 < SIZE and (grid[i][j] == '0' or grid[i][j] == 'T') and (grid[i+1][j] == '0' or grid[i+1][j] == 'M') and (grid[i+2][j] == '0' or grid[i+2][j] == 'M') and (grid[i+3][j] == '0' or grid[i+3][j] == 'B')):
                    if (COL_LIMIT[j] >= 4 and ROW_LIMIT[i] >= 1 and ROW_LIMIT[i+1] >= 1 and ROW_LIMIT[i+2] >= 1 and ROW_LIMIT[i+3] >= 1):
                        domain_1x4_col.add((i,j))

    # Initialize each ship with sizes and domains
    SHIP_LIMIT[0] -= num_init_1x1
    for i in range(NUMBER_TYPES_SHIPS):
        for j in range(SHIP_LIMIT[i]):
            if (i == 0):
                heapq.heappush(init_state.ships, [len(domain_1x1)*INDEX_1X1, priority_index, Ship(i+1, copy.deepcopy(domain_1x1))])
            elif (i == 1):
                heapq.heappush(init_state.ships, [len(domain_1x2_row)+len(domain_1x2_col), priority_index, Ship(i+1, copy.deepcopy(domain_1x2_row), copy.deepcopy(domain_1x2_col))])
            elif (i == 2):
                heapq.heappush(init_state.ships, [len(domain_1x3_row)+len(domain_1x3_col), priority_index, Ship(i+1, copy.deepcopy(domain_1x3_row), copy.deepcopy(domain_1x3_col))])
            else:
                heapq.heappush(init_state.ships, [len(domain_1x4_row)+len(domain_1x4_col), priority_index, Ship(i+1, copy.deepcopy(domain_1x4_row), copy.deepcopy(domain_1x4_col))])
            priority_index += 1
    SHIP_LIMIT[0] += num_init_1x1

    # for item in init_state.ships:
    #     item = item[2]
    #     print(item.length)
    #     print(item.domain_row)
    #     print(item.domain_col)
    #     print("==========================")

    # Call Forward Checking
    temp_ans = list()
    temp_ans = FC(init_state, temp_ans)

    # Output answer
    ans = [(['W'] * SIZE) for i in range(SIZE)]
    
    for item in temp_ans:
        ans[item[1]][item[2]] = item[0]

    with open(output_file, 'w', encoding='utf-8') as f:
        text = ''
        for row in ans:
            text += ''.join(row)
            text += '\n'
        f.write(text.strip())

    # for i in range(SIZE):
    #     ans[i].insert(0, str(ROW_LIMIT[i]))
    # col_limit = [str(i) for i in COL_LIMIT]
    # col_limit.insert(0, ' ')
    # ans.insert(0, col_limit)

    # for i in ans:
    #     print(i)

