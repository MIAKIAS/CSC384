'''
    Fall 2022 - CSC384 - Lab3
    Author: Weizhou Wang
    Student#: 1004421262
    Usage: 
'''
from sys import argv
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
    cur_ship:Ship = state.ships.pop()

    '''============================================Horizontal Placement============================================'''
    for row_value in cur_ship.domain_row.copy():
        row = row_value[0]
        col = row_value[1]
        # Check if adding the ship will exceed the row limit
        # FIXME: 现在还是BT，需要改成FC
        if (state.cur_row[row] + cur_ship.length > ROW_LIMIT[row]):
            cur_ship.domain_row.remove((row, col))
            # If DWO, we need to backtrack
            # if (len(cur_ship.domain_row) == 0):
            #     if (cur_ship.length == 1):
            #         return None
            #     break
            continue
        # Check if adding the ship will exceed the col limit
        if (state.cur_col[col] + 1 > COL_LIMIT[col]):
            cur_ship.domain_row.remove((row, col))
            # If DWO, we need to backtrack
            # if (len(cur_ship.domain_row) == 0):
            #     if (cur_ship.length == 1):
            #         return None
            #     break
            continue
        if (cur_ship.length > 1 and state.cur_col[col+1] + 1 > COL_LIMIT[col+1]):
            cur_ship.domain_row.remove((row, col))
            # If DWO, we need to backtrack
            # if (len(cur_ship.domain_row) == 0):
            #     break
            continue
        if (cur_ship.length > 2 and state.cur_col[col+2] + 1 > COL_LIMIT[col+2]):
            cur_ship.domain_row.remove((row, col))
            # If DWO, we need to backtrack
            # if (len(cur_ship.domain_row) == 0):
            #     return
            continue
        if (cur_ship.length > 3 and state.cur_col[col+3] + 1 > COL_LIMIT[col+3]):
            cur_ship.domain_row.remove((row, col))
            # If DWO, we need to backtrack
            # if (len(cur_ship.domain_row) == 0):
            #     break
            continue
        # Calculate the values that needs to be removed
        new_state = copy.deepcopy(state)
        new_state.cur_row[row] += cur_ship.length
        new_state.cur_col[col] += 1
        if (cur_ship.length > 1):
            new_state.cur_col[col+1] += 1
        if (cur_ship.length > 2):
            new_state.cur_col[col+2] += 1
        if (cur_ship.length > 3):
            new_state.cur_col[col+3] += 1
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
            ship.domain_row -= remove_set_1
            if (ship.length > 1):
                ship.domain_col -= remove_set_1
                ship.domain_col -= remove_set_2_col
                ship.domain_row -= remove_set_2_row
                if (ship.length > 2):
                    ship.domain_row -= remove_set_3_row
                    ship.domain_col -= remove_set_3_col
                if (ship.length > 3):
                    ship.domain_row -= remove_set_4_row
                    ship.domain_col -= remove_set_4_col
                if (len(ship.domain_col) == 0 and len(ship.domain_row) == 0):
                    DWO = True
                    break
            elif (len(ship.domain_row) == 0):
                DWO = True
                break
        # If DWO, try next value
        if (DWO):
            continue

        # Check if we can still align with the initialized values
        if (len(new_state.init_value) != 0):
            # The current placement may achieve some of the values
            if (ship.length == 1):
                new_state.init_value.discard(('S', row, col))
            elif (ship.length == 2):
                new_state.init_value.discard(('L', row, col))
                new_state.init_value.discard(('R', row, col+1))
            elif (ship.length == 3):
                new_state.init_value.discard(('L', row, col))
                new_state.init_value.discard(('M', row, col+1))
                new_state.init_value.discard(('R', row, col+2))
            elif (ship.length == 4):
                new_state.init_value.discard(('L', row, col))
                new_state.init_value.discard(('M', row, col+1))
                new_state.init_value.discard(('M', row, col+2))
                new_state.init_value.discard(('R', row, col+3))
            
            # Check if the remaining values can be covered
            # No need to check 1x1 ships
            temp_ships = new_state.ships[SHIP_LIMIT[0]:]
            temp_init = new_state.init_value.copy()
            if (not initialization_checker(temp_ships, temp_init)):
                cur_ship.domain_row.remove((row, col))
                # If DWO, we need to backtrack
                # if (len(cur_ship.domain_row) == 0):
                #     break
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
            # Check if adding the ship will exceed the col limit
            # FIXME: 现在还是BT，需要改成FC
            if (state.cur_col[col] + cur_ship.length > COL_LIMIT[col]):
                cur_ship.domain_col.remove((row, col))
                # If DWO, we need to backtrack
                if (len(cur_ship.domain_col) == 0):
                    return None
                continue
            # Check if adding the ship will exceed the row limit
            if (state.cur_row[row] + 1 > ROW_LIMIT[row]):
                cur_ship.domain_col.remove((row, col))
                # If DWO, we need to backtrack
                if (len(cur_ship.domain_col) == 0):
                    return None
                continue
            if (state.cur_row[row+1] + 1 > ROW_LIMIT[row+1]):
                cur_ship.domain_col.remove((row, col))
                # If DWO, we need to backtrack
                if (len(cur_ship.domain_col) == 0):
                    return None
                continue
            if (cur_ship.length > 2 and state.cur_row[row+2] + 1 > ROW_LIMIT[row+2]):
                cur_ship.domain_col.remove((row, col))
                # If DWO, we need to backtrack
                if (len(cur_ship.domain_col) == 0):
                    return None
                continue
            if (cur_ship.length > 3 and state.cur_row[row+3] + 1 > ROW_LIMIT[row+3]):
                cur_ship.domain_col.remove((row, col))
                # If DWO, we need to backtrack
                if (len(cur_ship.domain_col) == 0):
                    return None
                continue
            # Calculate the values that needs to be removed
            new_state = copy.deepcopy(state)
            new_state.cur_col[col] += cur_ship.length
            new_state.cur_row[row] += 1
            new_state.cur_row[row+1] += 1
            if (cur_ship.length > 2):
                new_state.cur_row[row+2] += 1
            if (cur_ship.length > 3):
                new_state.cur_row[row+3] += 1
            if (cur_ship.length > 4):
                new_state.cur_row[row+4] += 1
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
                ship.domain_row -= remove_set_1
                if (ship.length > 1):
                    ship.domain_row -= remove_set_2_row
                    ship.domain_col -= remove_set_1
                    ship.domain_col -= remove_set_2_col
                    if (ship.length > 2):
                        ship.domain_row -= remove_set_3_row
                        ship.domain_col -= remove_set_3_col
                    if (ship.length > 3):
                        ship.domain_row -= remove_set_4_row
                        ship.domain_col -= remove_set_4_col
                    if (len(ship.domain_col) == 0 and len(ship.domain_row) == 0):
                        DWO = True
                        break
                elif (len(ship.domain_row) == 0):
                    DWO = True
                    break
            # If DWO, try next value
            if (DWO):
                continue

            # Check if we can still align with the initialized values
            if (len(new_state.init_value) != 0):
                # The current placement may achieve some of the values
                if (ship.length == 2):
                    new_state.init_value.discard(('T', row, col))
                    new_state.init_value.discard(('B', row+1, col))
                elif (ship.length == 3):
                    new_state.init_value.discard(('T', row, col))
                    new_state.init_value.discard(('M', row+1, col))
                    new_state.init_value.discard(('B', row+2, col))
                elif (ship.length == 4):
                    new_state.init_value.discard(('T', row, col))
                    new_state.init_value.discard(('M', row+1, col))
                    new_state.init_value.discard(('M', row+2, col))
                    new_state.init_value.discard(('B', row+3, col))
                
                # Check if the remaining values can be covered
                # No need to check 1x1 ships
                temp_ships = new_state.ships[SHIP_LIMIT[0]:]
                temp_init = new_state.init_value.copy()
                if (not initialization_checker(temp_ships, temp_init)):
                    cur_ship.domain_col.remove((row, col))
                    # If DWO, we need to backtrack
                    if (len(cur_ship.domain_col) == 0):
                        return None

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
    else:
        init_item = init_values.pop()

    # Handle different values
    if (init_item[0] == 'L'):
        for ship in ships:
            if ((init_item[1], init_item[2]) in ship.domain_row):
                if (initialization_checker(ships.copy().remove(ship), init_values.copy())):
                    return True
        return False
    elif (init_item[0] == 'R'):
        for ship in ships:
            if (ship.length == 2 and ((init_item[1], init_item[2]-1) in ship.domain_row)) \
                or (ship.length == 3 and ((init_item[1], init_item[2]-2) in ship.domain_row)) \
                    or (ship.length == 4 and ((init_item[1], init_item[2]-3) in ship.domain_row)):
                if (initialization_checker(ships.copy().remove(ship), init_values.copy())):
                    return True
        return False
    elif (init_item[0] == 'T'):
        for ship in ships:
            if ((init_item[1], init_item[2]) in ship.domain_col):
                if (initialization_checker(ships.copy().remove(ship), init_values.copy())):
                    return True
        return False
    elif (init_item[0] == 'B'):
        for ship in ships:
            if (ship.length == 2 and ((init_item[1]-1, init_item[2]) in ship.domain_row)) \
                or (ship.length == 3 and ((init_item[1]-2, init_item[2]) in ship.domain_row)) \
                    or (ship.length == 4 and ((init_item[1]-3, init_item[2]) in ship.domain_row)):
                if (initialization_checker(ships.copy().remove(ship), init_values.copy())):
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
                if (initialization_checker(ships.copy().remove(ship), init_values.copy())):
                    return True
        return False

    


if __name__ == "__main__":
    if len(argv) != 3:
        print('Wrong input/output parameters...')
        exit(1)

    # Read in the input/output file names
    __, input_file, output_file = argv

    # input_file = "/h/u17/c1/00/wangw222/csc384/lab3/battle_validate/input_easy1.txt"
    # output_file = "/h/u17/c1/00/wangw222/csc384/lab3/output_easy1.txt"

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
    temp_ans = list()
    for i in range(SIZE):
        for j in range(SIZE):
            if (grid[i][j] == 'W'):
                continue
            elif (grid[i][j] == '0'):
                domain_1x1.add((i,j))
            # Directly assign values to one 1x1 ship
            elif (grid[i][j] == 'S'):
                num_init_1x1 += 1
                init_state.ships.append(Ship(1, {(i,j)}))
                continue
            # We need to check later if the rest of the initialized values are aligned with our assignments
            else:
                init_state.init_value.add((grid[i][j], i, j))

            if (NUMBER_TYPES_SHIPS >= 2):
                if (j+1 < SIZE and (grid[i][j] == '0' or grid[i][j] == 'L') and (grid[i][j+1] == '0' or grid[i][j+1] == 'R')):
                    domain_1x2_row.add((i,j))
                if (i+1 < SIZE and (grid[i][j] == '0' or grid[i][j] == 'T') and (grid[i+1][j] == '0' or grid[i+1][j] == 'B')):
                    domain_1x2_col.add((i,j))
            if (NUMBER_TYPES_SHIPS >= 3):
                if (j+2 < SIZE and (grid[i][j] == '0' or grid[i][j] == 'L') and (grid[i][j+1] == '0' or grid[i][j+1] == 'M') and (grid[i][j+2] == '0' or grid[i][j+2] == 'R')):
                    domain_1x3_row.add((i,j))
                if (i+2 < SIZE and (grid[i][j] == '0' or grid[i][j] == 'T') and (grid[i+1][j] == '0' or grid[i+1][j] == 'M') and (grid[i+2][j] == '0' or grid[i+2][j] == 'B')):
                    domain_1x3_col.add((i,j))
            if (NUMBER_TYPES_SHIPS >= 4):
                if (j+3 < SIZE and (grid[i][j] == '0' or grid[i][j] == 'L') and (grid[i][j+1] == '0' or grid[i][j+1] == 'M') and (grid[i][j+2] == '0' or grid[i][j+2] == 'M') and (grid[i][j+3] == '0' or grid[i][j+3] == 'R')):
                    domain_1x4_row.add((i,j))
                if (i+3 < SIZE and (grid[i][j] == '0' or grid[i][j] == 'T') and (grid[i+1][j] == '0' or grid[i+1][j] == 'M') and (grid[i+2][j] == '0' or grid[i+2][j] == 'M') and (grid[i+3][j] == '0' or grid[i+3][j] == 'B')):
                    domain_1x4_col.add((i,j))

    # Initialize each ship with sizes and domains
    SHIP_LIMIT[0] -= num_init_1x1
    for i in range(NUMBER_TYPES_SHIPS):
        for j in range(SHIP_LIMIT[i]):
            if (i == 0):
                init_state.ships.append(Ship(i+1, copy.deepcopy(domain_1x1)))
            elif (i == 1):
                init_state.ships.append(Ship(i+1, copy.deepcopy(domain_1x2_row), copy.deepcopy(domain_1x2_col)))
            elif (i == 2):
                init_state.ships.append(Ship(i+1, copy.deepcopy(domain_1x3_row), copy.deepcopy(domain_1x3_col)))
            else:
                init_state.ships.append(Ship(i+1, copy.deepcopy(domain_1x4_row), copy.deepcopy(domain_1x4_col)))
    SHIP_LIMIT[0] += num_init_1x1

    # for item in init_state.ships:
    #     print(item.length)
    #     print(item.domain_row)
    #     print(item.domain_col)
    #     print("==========================")

    # Call Forward Checking
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

