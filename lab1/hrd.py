'''
    Fall 2022 - CSC384 - Lab1
    Author: Weizhou Wang
    Student#: 1004421262
    Usage: To run the advanced heuristic, simply change "heuristic" from "Manhattan" to "Advanced"
'''
import string
import copy
from sys import argv
from queue import PriorityQueue


# This is the class representing a state
class State:
    # Init the list storing the coordinate of the top-left block of each piece
    state = [[], # empty
            [],  # 2x2
            [],  # 1x2
            [],  # 2x1
            []]  # 1x1
    # Record the previous state, for tracing back the route
    parent = None
    # Distance from intial state. Used by A*
    distance = int()

    # Helper function for sorting state list
    def sort_state(self):
        for sublist in self.state:
            if len(sublist) > 1:
                sublist.sort()
    # Calculate the Manhattan and advanced heuristic
    def heuristic(self) -> int:
        global heuristic
        if (heuristic == 'Manhattan'):
            return (3 - self.state[1][0][0]) + abs(self.state[1][0][1] - 1)
        else: # Advanced heuristic
            # For each piece, except the 2x2 piece, check if it is at the goal positions
            for i in range(2, 5):
                for j in range(len(self.state[i])):
                    # Check if any block in a tile is overlapping with the goal positions
                    # Note that "self.state[i][j]" is the coordinate of the top-left block
                    # So we also need to check the other block in that piece
                    # This is why the elements in the lists below are different
                    if ((i == 2 and self.state[i][j] in [[3,0],[4,0],[3,1],[3,2],[4,1],[4,2]])
                    or (i == 3 and self.state[i][j] in [[2,1],[2,2],[3,1],[3,2]])
                    or (i == 4 and self.state[i][j] in [[3,1],[3,2],[4,1],[4,2]])):
                        # if so, the heuristic will be Manhattan+1
                        return (3 - self.state[1][0][0]) + abs(self.state[1][0][1] - 1) + 1           
            # if no one is at that positions, just return the Manhattan heuristic
            return (3 - self.state[1][0][0]) + abs(self.state[1][0][1] - 1)

# A set to check explored state in the route
duplicate_checker = set()
# Frontier for DFS
frontier_stack = list()
# Frontier for A*
frontier_Astr = PriorityQueue()
# Tie breaker for A* Frontier
priority_index = 0
# Current heuristic function
heuristic = 'Manhattan'

# Trace back from the goal state to get the path
def trace_back(state: State) -> list:
    ans = list()
    # use the 'parent' member to trace back
    while (state is not None):
        ans.append(state.state)
        state = state.parent
    ans.reverse()
    return ans

# Check if the current state is the goal state
def goal_checker(state: State) -> bool:
    return state.state[1][0] == [3,1] # if the top-left block of 2x2 piece is at (3,1)

# Save the final answer to the output file
def ans_to_output(ans:list, file:string):
    grid = [['','','',''],
            ['','','',''],
            ['','','',''],
            ['','','',''],
            ['','','','']]
    text = ''
    text += 'Cost of the solution: {0}\n'.format(len(ans) - 1)
    for cur in ans:
        # Fill out the grid by the numbers
        for i in range(len(cur)):
            for j in range(len(cur[i])):
                grid[cur[i][j][0]][cur[i][j][1]] = str(i)
                if i == 1:
                    grid[cur[i][j][0]+1][cur[i][j][1]] = str(i)
                    grid[cur[i][j][0]][cur[i][j][1]+1] = str(i)
                    grid[cur[i][j][0]+1][cur[i][j][1]+1] = str(i)
                elif i == 2:
                    grid[cur[i][j][0]][cur[i][j][1]+1] = str(i)
                elif i == 3:
                    grid[cur[i][j][0]+1][cur[i][j][1]] = str(i)

        # Turn the grid into string
        for row in grid:
            text += ''.join(row)
            text += '\n'
        text += '\n'

    with open(file, 'w') as f:
        f.write(text)

        

# Find the non-duplicate successor of current state, and push to the DFS frontier stack
def successor(state: State, frontier):
    global priority_index
    for i in range(1, 5):
        for j in range(len(state.state[i])):
            # 2x2 Block
            if i == 1:
                # Move up 1 unit
                if [state.state[i][j][0]-1, state.state[i][j][1]] in state.state[0] and [state.state[i][j][0]-1, state.state[i][j][1]+1] in state.state[0]:
                    # print(str(state.state[i][j][0]) + ', ' + str(state.state[i][j][1]) + ' up')
                    new_state = State()
                    new_state.state = copy.deepcopy(state.state)
                    new_state.parent = state
                    new_state.distance = state.distance + 1
                    
                    # Empty blocks move down 2 units
                    new_state.state[0][0][0] += 2
                    new_state.state[0][1][0] += 2
                    # 2x2 moves up 1 unit
                    new_state.state[i][j][0] -= 1

                    # Sort state to avoid hitting explored state again
                    new_state.sort_state()
                    # Add state to the frontier
                    if type(frontier) == list:
                        frontier.append(new_state)
                    else:
                        frontier.put((new_state.heuristic() + new_state.distance, priority_index,  new_state))
                        priority_index += 1

                # Move down 1 unit
                elif [state.state[i][j][0]+2, state.state[i][j][1]] in state.state[0] and [state.state[i][j][0]+2, state.state[i][j][1]+1] in state.state[0]:
                    # print(str(state.state[i][j][0]) + ', ' + str(state.state[i][j][1]) + ' down')
                    new_state = State()
                    new_state.state = copy.deepcopy(state.state)
                    new_state.parent = state
                    new_state.distance = state.distance + 1
                    
                    # Empty blocks move up 2 units
                    new_state.state[0][0][0] -= 2
                    new_state.state[0][1][0] -= 2
                    # 2x2 moves down 1 unit
                    new_state.state[i][j][0] += 1

                    # Sort state to avoid hitting explored state again
                    new_state.sort_state()
                    # Add state to the frontier
                    if type(frontier) == list:
                        frontier.append(new_state)
                    else:
                        frontier.put((new_state.heuristic() + new_state.distance, priority_index,  new_state))
                        priority_index += 1

                # Move left 1 unit
                elif [state.state[i][j][0], state.state[i][j][1]-1] in state.state[0] and [state.state[i][j][0]+1, state.state[i][j][1]-1] in state.state[0]:
                    # print(str(state.state[i][j][0]) + ', ' + str(state.state[i][j][1]) + ' left')
                    new_state = State()
                    new_state.state = copy.deepcopy(state.state)
                    new_state.parent = state
                    new_state.distance = state.distance + 1
                    
                    # Empty blocks move right 2 units
                    new_state.state[0][0][1] += 2
                    new_state.state[0][1][1] += 2
                    # 2x2 moves left 1 unit
                    new_state.state[i][j][1] -= 1

                    # Sort state to avoid hitting explored state again
                    new_state.sort_state()
                    # Add state to the frontier
                    if type(frontier) == list:
                        frontier.append(new_state)
                    else:
                        frontier.put((new_state.heuristic() + new_state.distance, priority_index,  new_state))
                        priority_index += 1

                # Move right 1 unit
                elif [state.state[i][j][0], state.state[i][j][1]+2] in state.state[0] and [state.state[i][j][0]+1, state.state[i][j][1]+2] in state.state[0]:
                    # print(str(state.state[i][j][0]) + ', ' + str(state.state[i][j][1]) + ' right')
                    new_state = State()
                    new_state.state = copy.deepcopy(state.state)
                    new_state.parent = state
                    new_state.distance = state.distance + 1
                    
                    # Empty blocks move left 2 units
                    new_state.state[0][0][1] -= 2
                    new_state.state[0][1][1] -= 2
                    # 2x2 moves right 1 unit
                    new_state.state[i][j][1] += 1

                    # Sort state to avoid hitting explored state again
                    new_state.sort_state()
                    # Add state to the frontier
                    if type(frontier) == list:
                        frontier.append(new_state)
                    else:
                        frontier.put((new_state.heuristic() + new_state.distance, priority_index,  new_state))
                        priority_index += 1
                
            # 1x2 Block
            elif i == 2:
                # Move up 1 unit
                if [state.state[i][j][0]-1, state.state[i][j][1]] in state.state[0] and [state.state[i][j][0]-1, state.state[i][j][1]+1] in state.state[0]:
                    # print(str(state.state[i][j][0]) + ', ' + str(state.state[i][j][1]) + ' up')
                    new_state = State()
                    new_state.state = copy.deepcopy(state.state)
                    new_state.parent = state
                    new_state.distance = state.distance + 1
                    
                    # Empty blocks move down 1 units
                    new_state.state[0][0][0] += 1
                    new_state.state[0][1][0] += 1
                    # 1x2 moves up 1 unit
                    new_state.state[i][j][0] -= 1
                    
                    # Sort state to avoid hitting explored state again
                    new_state.sort_state()
                    # Add state to the frontier
                    if type(frontier) == list:
                        frontier.append(new_state)
                    else:
                        frontier.put((new_state.heuristic() + new_state.distance, priority_index,  new_state))
                        priority_index += 1

                # Move down 1 unit
                elif [state.state[i][j][0]+1, state.state[i][j][1]] in state.state[0] and [state.state[i][j][0]+1, state.state[i][j][1]+1] in state.state[0]:
                    # print(str(state.state[i][j][0]) + ', ' + str(state.state[i][j][1]) + ' down')
                    new_state = State()
                    new_state.state = copy.deepcopy(state.state)
                    new_state.parent = state
                    new_state.distance = state.distance + 1
                    
                    # Empty blocks move up 1 units
                    new_state.state[0][0][0] -= 1
                    new_state.state[0][1][0] -= 1
                    # 1x2 moves down 1 unit
                    new_state.state[i][j][0] += 1

                    # Sort state to avoid hitting explored state again
                    new_state.sort_state()
                    # Add state to the frontier
                    if type(frontier) == list:
                        frontier.append(new_state)
                    else:
                        frontier.put((new_state.heuristic() + new_state.distance, priority_index,  new_state))
                        priority_index += 1

                else:
                    # Move left 1 unit
                    if [state.state[i][j][0], state.state[i][j][1]-1] in state.state[0]:
                        # print(str(state.state[i][j][0]) + ', ' + str(state.state[i][j][1]) + ' left')
                        index = state.state[0].index([state.state[i][j][0], state.state[i][j][1]-1])
                        new_state = State()
                        new_state.state = copy.deepcopy(state.state)
                        new_state.parent = state
                        new_state.distance = state.distance + 1
                        
                        # Empty block moves right 2 units
                        new_state.state[0][index][1] += 2
                        # 1x2 moves left 1 unit
                        new_state.state[i][j][1] -= 1

                        # Sort state to avoid hitting explored state again
                        new_state.sort_state()
                        # Add state to the frontier
                        if type(frontier) == list:
                            frontier.append(new_state)
                        else:
                            frontier.put((new_state.heuristic() + new_state.distance, priority_index,  new_state))
                            priority_index += 1

                    # Move right 1 unit
                    if [state.state[i][j][0], state.state[i][j][1]+2] in state.state[0]:
                        # print(str(state.state[i][j][0]) + ', ' + str(state.state[i][j][1]) + ' right')
                        index = state.state[0].index([state.state[i][j][0], state.state[i][j][1]+2])
                        new_state = State()
                        new_state.state = copy.deepcopy(state.state)
                        new_state.parent = state
                        new_state.distance = state.distance + 1
                        
                        # Empty block moves left 2 units
                        new_state.state[0][index][1] -= 2
                        # 1x2 moves right 1 unit
                        new_state.state[i][j][1] += 1

                        # Sort state to avoid hitting explored state again
                        new_state.sort_state()
                        # Add state to the frontier
                        if type(frontier) == list:
                            frontier.append(new_state)
                        else:
                            frontier.put((new_state.heuristic() + new_state.distance, priority_index,  new_state))
                            priority_index += 1
                        
            # 2x1 Block
            elif i == 3:
                # Move left 1 unit
                if [state.state[i][j][0], state.state[i][j][1]-1] in state.state[0] and [state.state[i][j][0]+1, state.state[i][j][1]-1] in state.state[0]:
                    # print(str(state.state[i][j][0]) + ', ' + str(state.state[i][j][1]) + ' left')
                    new_state = State()
                    new_state.state = copy.deepcopy(state.state)
                    new_state.parent = state
                    new_state.distance = state.distance + 1
                    
                    # Empty blocks move right 1 unit
                    new_state.state[0][0][1] += 1
                    new_state.state[0][1][1] += 1
                    # 2x1 moves left 1 unit
                    new_state.state[i][j][1] -= 1

                    # Sort state to avoid hitting explored state again
                    new_state.sort_state()
                    # Add state to the frontier
                    if type(frontier) == list:
                        frontier.append(new_state)
                    else:
                        frontier.put((new_state.heuristic() + new_state.distance, priority_index,  new_state))
                        priority_index += 1

                # Move right 1 unit
                elif [state.state[i][j][0], state.state[i][j][1]+1] in state.state[0] and [state.state[i][j][0]+1, state.state[i][j][1]+1] in state.state[0]:
                    # print(str(state.state[i][j][0]) + ', ' + str(state.state[i][j][1]) + ' right')
                    new_state = State()
                    new_state.state = copy.deepcopy(state.state)
                    new_state.parent = state
                    new_state.distance = state.distance + 1
                    
                    # Empty blocks move left 1 unit
                    new_state.state[0][0][1] -= 1
                    new_state.state[0][1][1] -= 1
                    # 2x1 moves right 1 unit
                    new_state.state[i][j][1] += 1

                    # Sort state to avoid hitting explored state again
                    new_state.sort_state()
                    # Add state to the frontier
                    if type(frontier) == list:
                        frontier.append(new_state)
                    else:
                        frontier.put((new_state.heuristic() + new_state.distance, priority_index,  new_state))
                        priority_index += 1

                else:
                    # Move up 1 unit
                    if [state.state[i][j][0]-1, state.state[i][j][1]] in state.state[0]:
                        # print(str(state.state[i][j][0]) + ', ' + str(state.state[i][j][1]) + ' up')
                        index = state.state[0].index([state.state[i][j][0]-1, state.state[i][j][1]])
                        new_state = State()
                        new_state.state = copy.deepcopy(state.state)
                        new_state.parent = state
                        new_state.distance = state.distance + 1
                        
                        # Empty block moves down 2 units
                        new_state.state[0][index][0] += 2
                        # 2x1 moves up 1 unit
                        new_state.state[i][j][0] -= 1

                        # Sort state to avoid hitting explored state again
                        new_state.sort_state()
                        # Add state to the frontier
                        if type(frontier) == list:
                            frontier.append(new_state)
                        else:
                            frontier.put((new_state.heuristic() + new_state.distance, priority_index,  new_state))
                            priority_index += 1

                    # Move down 1 unit
                    if [state.state[i][j][0]+2, state.state[i][j][1]] in state.state[0]:
                        # print(str(state.state[i][j][0]) + ', ' + str(state.state[i][j][1]) + ' down')
                        index = state.state[0].index([state.state[i][j][0]+2, state.state[i][j][1]])
                        new_state = State()
                        new_state.state = copy.deepcopy(state.state)
                        new_state.parent = state
                        new_state.distance = state.distance + 1
                        
                        # Empty block moves up 2 units
                        new_state.state[0][index][0] -= 2
                        # 2x1 moves down 1 unit
                        new_state.state[i][j][0] += 1

                        # Sort state to avoid hitting explored state again
                        new_state.sort_state()
                        # Add state to the frontier
                        if type(frontier) == list:
                            frontier.append(new_state)
                        else:
                            frontier.put((new_state.heuristic() + new_state.distance, priority_index,  new_state))
                            priority_index += 1

            # 1x1 Block
            else:
                # Move up 1 unit
                if [state.state[i][j][0]-1, state.state[i][j][1]] in state.state[0]:
                    # print(str(state.state[i][j][0]) + ', ' + str(state.state[i][j][1]) + ' up')
                    index = state.state[0].index([state.state[i][j][0]-1, state.state[i][j][1]])
                    new_state = State()
                    new_state.state = copy.deepcopy(state.state)
                    new_state.parent = state
                    new_state.distance = state.distance + 1
                    
                    # Empty block moves down 1 unit
                    new_state.state[0][index][0] += 1
                    # Block moves up 1 unit
                    new_state.state[i][j][0] -= 1

                    # Sort state to avoid hitting explored state again
                    new_state.sort_state()
                    # Add state to the frontier
                    if type(frontier) == list:
                        frontier.append(new_state)
                    else:
                        frontier.put((new_state.heuristic() + new_state.distance, priority_index,  new_state))
                        priority_index += 1

                # Move down 1 unit
                if [state.state[i][j][0]+1, state.state[i][j][1]] in state.state[0]:
                    # print(str(state.state[i][j][0]) + ', ' + str(state.state[i][j][1]) + ' down')
                    index = state.state[0].index([state.state[i][j][0]+1, state.state[i][j][1]])
                    new_state = State()
                    new_state.state = copy.deepcopy(state.state)
                    new_state.parent = state
                    new_state.distance = state.distance + 1
                    
                    # Empty block moves up 1 unit
                    new_state.state[0][index][0] -= 1
                    # Block moves down 1 unit
                    new_state.state[i][j][0] += 1

                    # Sort state to avoid hitting explored state again
                    new_state.sort_state()
                    # Add state to the frontier
                    if type(frontier) == list:
                        frontier.append(new_state)
                    else:
                        frontier.put((new_state.heuristic() + new_state.distance, priority_index,  new_state))
                        priority_index += 1

                # Move left 1 unit
                if [state.state[i][j][0], state.state[i][j][1]-1] in state.state[0]:
                    # print(str(state.state[i][j][0]) + ', ' + str(state.state[i][j][1]) + ' left')
                    index = state.state[0].index([state.state[i][j][0], state.state[i][j][1]-1])
                    new_state = State()
                    new_state.state = copy.deepcopy(state.state)
                    new_state.parent = state
                    new_state.distance = state.distance + 1
                    
                    # Empty block moves right 1 unit
                    new_state.state[0][index][1] += 1
                    # Block moves left 1 unit
                    new_state.state[i][j][1] -= 1

                    # Sort state to avoid hitting explored state again
                    new_state.sort_state()
                    # Add state to the frontier
                    if type(frontier) == list:
                        frontier.append(new_state)
                    else:
                        frontier.put((new_state.heuristic() + new_state.distance, priority_index,  new_state))
                        priority_index += 1

                # Move right 1 unit
                if [state.state[i][j][0], state.state[i][j][1]+1] in state.state[0]:
                    # print(str(state.state[i][j][0]) + ', ' + str(state.state[i][j][1]) + ' right')
                    index = state.state[0].index([state.state[i][j][0], state.state[i][j][1]+1])
                    new_state = State()
                    new_state.state = copy.deepcopy(state.state)
                    new_state.parent = state
                    new_state.distance = state.distance + 1
                    
                    # Empty block moves left 1 unit
                    new_state.state[0][index][1] -= 1
                    # Block moves right 1 unit
                    new_state.state[i][j][1] += 1

                    # Sort state to avoid hitting explored state again
                    new_state.sort_state()
                    # Add state to the frontier
                    if type(frontier) == list:
                        frontier.append(new_state)
                    else:
                        frontier.put((new_state.heuristic() + new_state.distance, priority_index,  new_state))
                        priority_index += 1



if __name__== "__main__":
    if len(argv) != 4:
        print('Wrong input/output parameters...')
        exit(1)
    
    # Read in the input/output file names
    __, input_file, DFS_output, Astr_output = argv

    init_state = State()
    ans = list()

    init_state.distance = 0
    init_state.parent = None

    # Read initial state from file to list
    with open(input_file, 'r', encoding='utf-8') as f:
        row = 0
        zero_counter = 0
        one_counter = 0
        two_counter = 0
        for line in f:
            col = 0
            line = line.strip()
            while col < len(line):
                num = int(line[col])
                # Empty Block
                if num == 0:
                    init_state.state[0].append([row, col])
                # 1x1 Block
                elif num == 7:
                    init_state.state[4].append([row, col])
                # 2x2 Block
                elif num == 1:
                    if len(init_state.state[1]) == 0:
                        init_state.state[1].append([row, col])
                else:
                    # Horizontal 1x2
                    if col+1 < len(line) and line[col]==line[col+1]:
                        init_state.state[2].append([row, col])
                        col += 1
                    # Vertical 2x1
                    elif [row-1, col] not in init_state.state[3]:
                        init_state.state[3].append([row, col])
                        
                col += 1
            row += 1
    
    # Sort the state to Sort state to avoid hitting explored state again
    init_state.sort_state()

    # ==========================================DFS======================================================
    # Push to the frontier stack
    frontier_stack.append(init_state)

    while (len(frontier_stack) > 0):
        # Pop the first element from stack
        cur = frontier_stack.pop()
        state_string = ''.join([str(element) for i in cur.state for j in i for element in j])
        # If state has not been explored
        if not state_string in duplicate_checker:
            # Add to the explored set
            duplicate_checker.add(state_string)
            # If state is a goal state
            if goal_checker(cur):
                # Find the route
                ans = trace_back(cur)
                print('Find DFS answer, with {0} steps'.format(len(ans) - 1))
                ans_to_output(ans, DFS_output)
                break
            # Add curr's successors to the stack
            successor(cur, frontier_stack)

    # Empty the checker for next algorithm
    duplicate_checker = set()

    # ==========================================Manhattan Astr======================================================
    # Push to the frontier PQ
    frontier_Astr.put((init_state.heuristic() + init_state.distance, priority_index,  init_state))
    priority_index += 1

    while (not frontier_Astr.empty()):
        # Pop the first element from frontier
        cur = frontier_Astr.get()[2]
        state_string = ''.join([str(element) for i in cur.state for j in i for element in j])
        # If state has not been explored
        if not state_string in duplicate_checker:
            # Add to the explored set
            duplicate_checker.add(state_string)
            # If state is a goal state
            if goal_checker(cur):
                # Find the route
                ans = trace_back(cur)
                print('Find Manhattan A* answer, with {0} steps'.format(len(ans) - 1))
                ans_to_output(ans, Astr_output)
                break
            # Add curr's successors to the Frontier
            successor(cur, frontier_Astr)
    # Empty the checker for next algorithm
    frontier_Astr = PriorityQueue()
    duplicate_checker = set()
    priority_index = 0
    
    # ==========================================Advanced Astr======================================================
    # heuristic = 'Advanced'
    # # Push to the frontier PQ
    # frontier_Astr.put((init_state.heuristic() + init_state.distance, priority_index,  init_state))
    # priority_index += 1

    # while (not frontier_Astr.empty()):
    #     # Pop the first element from frontier
    #     cur = frontier_Astr.get()[2]
    #     state_string = ''.join([str(element) for i in cur.state for j in i for element in j])
    #     # If state has not been explored
    #     if not state_string in duplicate_checker:
    #         # Add to the explored set
    #         duplicate_checker.add(state_string)
    #         # If state is a goal state
    #         if goal_checker(cur):
    #             # Find the route
    #             ans = trace_back(cur)
    #             print('Find Advanced A* answer, with {0} steps'.format(len(ans) - 1))
    #             ans_to_output(ans, './outputs_Advanced/puzzle5sol_advanced.txt')
    #             break
    #         # Add curr's successors to the Frontier
    #         successor(cur, frontier_Astr)
    