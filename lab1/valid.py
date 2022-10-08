import copy
import random
import time
import queue
import sys
from queue import PriorityQueue

class State:
  def __init__(self, board, pieces, parent=None):
    self.board = copy.deepcopy(board)
    self.pieces = copy.deepcopy(pieces)
    self.parent = parent
    self.cost = 0 if self.parent == None else parent.cost + 1
    self.f = get_cost(self) + get_heuristic(self)
  
  def __lt__(self, other):
    return self.f < other.f

def read_puzzle(id):
  f = open('./inputs/'+str(id) + '.txt', 'r')
  lines = f.readlines()
  raw = [[int(x) for x in l.rstrip()] for l in lines]
  board = copy.deepcopy(raw)
  pieces = []
  for i in range(8):
    piece = []
    for a in range(len(raw)):
      for b in range(len(raw[a])):
        if (raw[a][b] == i):
          piece.append([a, b])
    pieces.append(piece)
    if raw[piece[0][0]][piece[0][1]] < 2:
      pass
    elif raw[piece[0][0]][piece[0][1]] == 7:
      for p in piece:
        board[p[0]][p[1]] = 4
    elif (len(piece) == 2) and piece[0][0] == piece[1][0]:
      for p in piece:
        board[p[0]][p[1]] = 2
    elif (len(piece) == 2) and piece[0][1] == piece[1][1]:
      for p in piece:
        board[p[0]][p[1]] = 3
  init = State(board, pieces, None)
  return init

def get_cost(state):
  return state.cost

def get_heuristic(state):
  return 0

def is_goal(state):
  return state.board[4][1] == 1 and state.board[4][2] == 1

def get_successors(state):
  successors = []
  for i in range(len(state.pieces[0])):
    p = state.pieces[0][i]
    if (p[0] > 0): #bounds down
      if (state.board[p[0]-1][p[1]] == 4):
        new_board = copy.deepcopy(state.board)
        new_pieces = copy.deepcopy(state.pieces)
        new_board[p[0]-1][p[1]] = 0
        new_board[p[0]][p[1]] = 4
        new_pieces[7].remove([p[0]-1, p[1]])
        new_pieces[7].append([p[0], p[1]])
        new_pieces[0][i] = [p[0]-1, p[1]]
        successors.append(State(new_board, new_pieces, state))
      elif (p[0] > 1 and state.board[p[0]-1][p[1]] == 3):
        new_board = copy.deepcopy(state.board)
        new_pieces = copy.deepcopy(state.pieces)
        new_board[p[0]-2][p[1]] = 0
        new_board[p[0]][p[1]] = 3
        for z in new_pieces:
          if [p[0]-2, p[1]] in z:
            z.remove([p[0]-2, p[1]])
            z.append([p[0], p[1]])
        new_pieces[0][i] = [p[0]-2, p[1]]
        successors.append(State(new_board, new_pieces, state))
      elif (i == 0 and p[0] > 0 and (state.board[p[0]-1][p[1]] == 2 or state.board[p[0]-1][p[1]] == 1) and ((p[1] > 0 and state.board[p[0]][p[1]-1] == 0) or (p[1] < 3 and state.board[p[0]][p[1]+1] == 0))):
        new_board = copy.deepcopy(state.board)
        new_pieces = copy.deepcopy(state.pieces)
        p_ = None
        mp = (state.board[p[0]-1][p[1]] == 1)
        for z in new_pieces:
          if ([p[0]-1,p[1]] in z):
            p_ = z
            if ([p[0]-1,state.pieces[0][1-i][1]] in z):
              z.remove([p[0]-1-mp, p[1]])
              z.append([p[0], p[1]])
              z.remove([p[0]-1-mp,state.pieces[0][1-i][1]])
              z.append([p[0],state.pieces[0][1-i][1]])
              new_pieces[0][i] = [p[0]-1-mp, p[1]]
              new_pieces[0][1-i] = [p[0]-1-mp,state.pieces[0][1-i][1]]
              new_board[p[0]][p[1]] = 2 - mp
              new_board[p[0]][state.pieces[0][1-i][1]] = 2 - mp
              new_board[p[0]-1-mp][p[1]] = 0
              new_board[p[0]-1-mp][state.pieces[0][1-i][1]] = 0
          if (p_ != None):
            break
        successors.append(State(new_board, new_pieces, state))
    if (p[0] < 4): #bounds up
      if (state.board[p[0]+1][p[1]] == 4):
        new_board = copy.deepcopy(state.board)
        new_pieces = copy.deepcopy(state.pieces)
        new_board[p[0]+1][p[1]] = 0
        new_board[p[0]][p[1]] = 4
        new_pieces[7].remove([p[0]+1, p[1]])
        new_pieces[7].append([p[0], p[1]])
        new_pieces[0][i] = [p[0]+1, p[1]]
        successors.append(State(new_board, new_pieces, state))
      elif (p[0] < 3 and state.board[p[0]+1][p[1]] == 3):
        new_board = copy.deepcopy(state.board)
        new_pieces = copy.deepcopy(state.pieces)
        new_board[p[0]+2][p[1]] = 0
        new_board[p[0]][p[1]] = 3
        for z in new_pieces:
          if [p[0]+2, p[1]] in z:
            z.remove([p[0]+2, p[1]])
            z.append([p[0], p[1]])
        new_pieces[0][i] = [p[0]+2, p[1]]
        successors.append(State(new_board, new_pieces, state))
      elif (i == 0 and p[0] < 4 and (state.board[p[0]+1][p[1]] == 1 or state.board[p[0]+1][p[1]] == 2) and ((p[1] < 3 and state.board[p[0]][p[1]+1] == 0) or (p[1] > 0 and state.board[p[0]][p[1]-1] == 0))):
        new_board = copy.deepcopy(state.board)
        new_pieces = copy.deepcopy(state.pieces)
        p_ = None
        mp = (state.board[p[0]+1][p[1]] == 1)
        for z in new_pieces:
          if ([p[0]+1,p[1]] in z):
            p_ = z
            if ([p[0]+1,state.pieces[0][1-i][1]] in z):
              z.remove([p[0]+1+mp, p[1]])
              z.append([p[0], p[1]])
              z.remove([p[0]+1+mp,state.pieces[0][1-i][1]])
              z.append([p[0],state.pieces[0][1-i][1]])
              new_pieces[0][i] = [p[0]+1+mp, p[1]]
              new_pieces[0][1-i] = [p[0]+1+mp,state.pieces[0][1-i][1]]
              new_board[p[0]][p[1]] = 2-mp
              new_board[p[0]][state.pieces[0][1-i][1]] = 2-mp
              new_board[p[0]+1+mp][p[1]] = 0
              new_board[p[0]+1+mp][state.pieces[0][1-i][1]] = 0
          if (p_ != None):
            break
        successors.append(State(new_board, new_pieces, state))
    if (p[1] > 0): #bounds left
      if (state.board[p[0]][p[1]-1] == 4):
        new_board = copy.deepcopy(state.board)
        new_pieces = copy.deepcopy(state.pieces)
        new_board[p[0]][p[1]-1] = 0
        new_board[p[0]][p[1]] = 4
        new_pieces[7].remove([p[0], p[1]-1])
        new_pieces[7].append([p[0], p[1]])
        new_pieces[0][i] = [p[0], p[1]-1]
        successors.append(State(new_board, new_pieces, state))
      elif (p[1] > 1 and state.board[p[0]][p[1]-1] == 2):
        new_board = copy.deepcopy(state.board)
        new_pieces = copy.deepcopy(state.pieces)
        new_board[p[0]][p[1]-2] = 0
        new_board[p[0]][p[1]] = 2
        for z in new_pieces:
          if [p[0], p[1]-2] in z:
            z.remove([p[0], p[1]-2])
            z.append([p[0], p[1]])
        new_pieces[0][i] = [p[0], p[1]-2]
        successors.append(State(new_board, new_pieces, state))
      elif (i == 0 and p[1] > 0 and (state.board[p[0]][p[1]-1] == 1 or state.board[p[0]][p[1]-1] == 3) and ((p[0] > 0 and state.board[p[0]-1][p[1]] == 0) or (p[0] < 4 and state.board[p[0]+1][p[1]] == 0))):
        new_board = copy.deepcopy(state.board)
        new_pieces = copy.deepcopy(state.pieces)
        p_ = None
        mp = (state.board[p[0]][p[1]-1] == 1)
        for z in new_pieces:
          if ([p[0],p[1]-1] in z):
            p_ = z
            if ([state.pieces[0][1-i][0],p[1]-1] in z):
              z.remove([p[0],p[1]-1-mp])
              z.append([p[0],p[1]])
              z.remove([state.pieces[0][1-i][0],p[1]-1-mp])
              z.append([state.pieces[0][1-i][0],p[1]])
              new_pieces[0][i] = [p[0],p[1]-1-mp]
              new_pieces[0][1-i] = [state.pieces[0][1-i][0],p[1]-1-mp]
              new_board[state.pieces[0][1-i][0]][p[1]] = 3-mp-mp
              new_board[p[0]][p[1]] = 3-mp-mp
              new_board[state.pieces[0][1-i][0]][p[1]-1-mp] = 0
              new_board[p[0]][p[1]-1-mp] = 0
          if (p_ != None):
            break
        successors.append(State(new_board, new_pieces, state))
    if (p[1] < 3): #bounds right
      if (state.board[p[0]][p[1]+1] == 4):
        new_board = copy.deepcopy(state.board)
        new_pieces = copy.deepcopy(state.pieces)
        new_board[p[0]][p[1]+1] = 0
        new_board[p[0]][p[1]] = 4
        new_pieces[7].remove([p[0], p[1]+1])
        new_pieces[7].append([p[0], p[1]])
        new_pieces[0][i] = [p[0], p[1]+1]
        successors.append(State(new_board, new_pieces, state))
      elif (p[1] < 2 and state.board[p[0]][p[1]+1] == 2):
        new_board = copy.deepcopy(state.board)
        new_pieces = copy.deepcopy(state.pieces)
        new_board[p[0]][p[1]+2] = 0
        new_board[p[0]][p[1]] = 2
        for z in new_pieces:
          if [p[0], p[1]+2] in z:
            z.remove([p[0], p[1]+2])
            z.append([p[0], p[1]])
        new_pieces[0][i] = [p[0], p[1]+2]
        successors.append(State(new_board, new_pieces, state))
      elif (i == 0 and p[1] < 3 and (state.board[p[0]][p[1]+1] == 1 or state.board[p[0]][p[1]+1] == 3) and ((p[0] < 4 and state.board[p[0]+1][p[1]] == 0) or (p[0] > 0 and state.board[p[0]-1][p[1]] == 0))):
        new_board = copy.deepcopy(state.board)
        new_pieces = copy.deepcopy(state.pieces)
        p_ = None
        mp = (state.board[p[0]][p[1]+1] == 1)
        for z in new_pieces:
          if ([p[0],p[1]+1] in z):
            p_ = z
            if ([state.pieces[0][1-i][0],p[1]+1] in z):
              z.remove([p[0],p[1]+1+mp])
              z.append([p[0],p[1]])
              z.remove([state.pieces[0][1-i][0],p[1]+1+mp])
              z.append([state.pieces[0][1-i][0],p[1]])
              new_pieces[0][i] = [p[0],p[1]+1+mp]
              new_pieces[0][1-i] = [state.pieces[0][1-i][0],p[1]+1+mp]
              new_board[state.pieces[0][1-i][0]][p[1]] = 3-mp-mp
              new_board[p[0]][p[1]] = 3-mp-mp
              new_board[state.pieces[0][1-i][0]][p[1]+1+mp] = 0
              new_board[p[0]][p[1]+1+mp] = 0
          if (p_ != None):
            break
        successors.append(State(new_board, new_pieces, state))
  return successors

def astar(initial_state):
  expanded = 0
  expanded_set = set()
  frontier = PriorityQueue()
  frontier.put((initial_state.f, initial_state))

  while(frontier.empty() == False):
    selected = frontier.get()[1]
    if(state_to_key(selected) in expanded_set):
      continue
    else:
      expanded_set.add(state_to_key(selected))
      successors = get_successors(selected)
      expanded += 1
      for scs in successors:
        if(is_goal(scs)):
          return(scs, expanded)
        else:
          frontier.put((scs.f, scs))
  return (None, -1)

def dfs(initial_state):
  expanded = 0
  expanded_set = set()
  frontier = []
  frontier.append(initial_state)
  expanded_set.add(state_to_key(initial_state))

  while(len(frontier) != 0):
    selected = frontier.pop()
    successors = get_successors(selected)
    expanded += 1
    for scs in successors:
      if(is_goal(scs)):
        return(scs, expanded)
      if(state_to_key(scs) not in expanded_set):
        frontier.append(scs)
        expanded_set.add(state_to_key(scs))
  return (None, -1)

def state_to_key(state):
  return (''.join(''.join(str(x) for x in z) for z in state.board))

def print_board(b):
  strg = ''
  for i in b:
    for j in i:
      strg += str(j)
    strg += '\n'
  strg += '\n'
  return strg

if __name__ == '__main__':
  init = read_puzzle(int(sys.argv[1]))
  succ = get_successors(init)
  file_read = open(sys.argv[2], "r")
  lines = file_read.readlines()
  board_ = []
  start = False
  start2 = False
  for l in lines:
    if start and start2:
      if l == "\n":
        passed = False
        for x in succ:
          if x.board == board_:
            passed = True
            init = x
        succ = get_successors(init)
        if not passed:
          print("FAILED\n")
        #break
        board_ = []
      else:
        temp = l.rstrip()
        arr = []
        for i in temp:
          arr.append(int(i))
        board_.append(arr)
    if start:
      if l == "\n":
        start2 = True
    if l.startswith("Cost of the solution:"):
      start = True