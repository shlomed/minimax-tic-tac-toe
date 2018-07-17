
# coding: utf-8

# In[21]:


import numpy as np
from math import inf
import platform
import time
from os import system
from pprint import pprint


# In[64]:


HUMAN = -1
COMP = +1

board = np.zeros((3,3), dtype=np.int)
pprint(board)


# In[37]:


def print_state(state):
    """
    This function prints a state to the screen.
    :param state: the state (np.array of size 3X3)
    :return: only prints. returns None.
    """
    for row in state:
        print("|", end="")
        for element in row:
            if element==-1:
                print(" o |", end="")
            elif element==1:
                print(" x |", end="")
            else:
                print("   |", end="")
        print()


# In[63]:


# # example:
# state = np.zeros((3,3), dtype=np.int)
# state[1,1] = 1
# state[2,2] = -1
# state[0,0] = 1
# print_state(state.tolist())


# In[68]:


def evaluate(state):
    """
    This function returns (+1) if COMP won in this state, (-1) if HUMAN won, and (0) if none.
    :param state: the state (np.array of size 3X3)
    :return: (+1) if COMP won in this state, (-1) if HUMAN won, and (0) if none.
    """
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0


# In[69]:


def wins(state, player):
    """
    This function returns True if player won the game for the given state.
    :param state: the state (np.array of size 3X3)
    :param player: HUMAN or COMP
    :return: True if player won, False if not.
    """
    # if one of the triplets in the following list is all [1,1,1] then COMP wins. if [-1,-1,-1] then HUMAM wins
    wins_states = [state[0, :].tolist(), # 1st row  
                 state[1, :].tolist(), # 2st row 
                 state[2, :].tolist(), # 3st row 
                 state[:, 0].tolist(), # 1st col 
                 state[:, 1].tolist(), # 2st col 
                 state[:, 2].tolist(), # 3st col 
                 [state[0, 0], state[1, 1], state[2, 2]], # 1st diagonal
                 [state[2, 0], state[1, 1], state[0, 2]]] # 2st diagonal
    
    if [player, player, player] in wins_states:
        return True # player wins
    else:
        return False # player doesn't win


# In[70]:


def game_over(state):
    """
    This function returns True one of the players won the game in the current state.
    :param state: the state (np.array of size 3X3)
    :return: True if game is won, False if not.
    """
    return wins(state, HUMAN) or wins(state, COMP)


# In[79]:


def empty_locations(state):
    """
    This function returns a list with all empty locations (x,y) on board for a given state.
    :param state: the state (np.array of size 3X3)
    :return: list of (x,y) tuples of the empty locations.
    """
    locs = list(zip(*np.where(state==0)))
    return locs


# In[80]:


def valid_move(x,y):
    """
    This function returns True if location (x,y) is empty.
    - uses the global "board" variable.
    :param x: row index
    :param y: col index
    :return: True if (x,y) loc is empty. False otherwise.
    """
    return board[x,y]==0


# In[84]:


def set_move(x, y, player):
    """
    This function changes the state of an empty location (x,y) on board to player (+1 for COMP, -1 for HUMAN).
    - uses the global "board" variable.
    :param x: row index
    :param y: col index
    :return: if valid_state: changes board state and returns True. if not valid: returns False
    """ 
    if valid_move(x,y):
        board[x,y] = player
        return True
    else:
        return False


# In[105]:


def minimax(state, depth, player):
    """
    This is the minimax algorithm. it unfolds (recursively) all the tree from this state down, 
    and finds the best location for the next move according to the minimax algorithm.
    The stop condition of the recursivityis if one of the players wins, or if the depth is 0 (no more plays left to play). 
    :param state: the state (np.array of size 3X3)
    :param depth: how many layers are left to go down. in the initial state, it's 9, and if the board is full - it is 0.
    :param player: HUMAN or COMP
    :return: best, which correspond to the best move for playe from the current state. best = [x, y, score]
    """ 
    if player==COMP:
        best = [-1, -1, -inf] # best should include the best move after the for-loop later. in the form of [x, y, score]
                              # we initiate it with [-1, -1] for no location, and -inf so that the first outcome (score) will override it.
    else: # player==HUMAN:
        best = [-1, -1, +inf] # +inf so that the first outcome (score) will override it.
    
    if depth==0 or game_over(state):
        score = evaluate(state) # returns (+1) if COMP wins, (-1) if HUMAN wins, (0) elsewhere.
        return [-1, -1, score]
    
    for loc in empty_locations(state):
        (x,y) = loc
        state[x,y] = player # we'll change it back after calculating the minimax for this location. don't worry...
        score = minimax(state, depth-1, -player) # run minimax for the (state, player) as if the current move was (x,y)
        state[x,y] = 0
        score = [x, y, score[2]]
        
        if player==COMP: # player==COMP, max move
            if score[2] > best[2]:
                best = score
        else: # player==HUMAN, min move
            if score[2] < best[2]:
                best = score
        
    return best


# In[106]:


def clean():
    """
    Clears the console.
    """
    os_name = platform.system().lower() # returns o/s name in lower case. e.g., 'windows', 'linux', etc.
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


# In[ ]:


def render(state, c_choice, h_choice):
    """
    Prints the board on console
    """


# In[59]:


state = board.copy()
state[2, :] = np.array([1,1,1])
state[2, 2] = 0
state


# In[83]:


print_state(board)
valid_move(2,2)


# In[101]:


a = [[1,2,3]]


# In[102]:


def f(x):
    x[0][2] = 10


# In[103]:


f(a)


# In[104]:


a

