
# coding: utf-8

# In[ ]:


import numpy as np
from math import inf
import platform
import time
from os import system
from pprint import pprint


# In[ ]:


HUMAN = -1
COMP = +1

board = np.zeros((3,3), dtype=np.int)


# In[ ]:


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


# In[ ]:


# # example:
# state = np.zeros((3,3), dtype=np.int)
# state[1,1] = 1
# state[2,2] = -1
# state[0,0] = 1
# print_state(state.tolist())


# In[ ]:


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
        
    return score


# In[ ]:


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


# In[ ]:


def game_over(state):
    """
    This function returns True one of the players won the game in the current state.
    :param state: the state (np.array of size 3X3)
    :return: True if game is won, False if not.
    """
    return wins(state, HUMAN) or wins(state, COMP)


# In[ ]:


def empty_locations(state):
    """
    This function returns a list with all empty locations (x,y) on board for a given state.
    :param state: the state (np.array of size 3X3)
    :return: list of (x,y) tuples of the empty locations.
    """
    locs = list(zip(*np.where(state==0)))
    return locs


# In[ ]:


def valid_move(x,y):
    """
    This function returns True if location (x,y) is empty.
    - uses the global "board" variable.
    :param x: row index
    :param y: col index
    :return: True if (x,y) loc is empty. False otherwise.
    """
    return board[x,y]==0


# In[ ]:


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


# In[ ]:


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


# In[ ]:


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


def render(state, c_choice="X", h_choice="O"):
    """
    This function prints a state to the screen.
    :param state: the state (np.array of size 3X3)
    :return: only prints. returns None.
    """
    for row in state:
        print("|", end="")
        for element in row:
            if element==-1:
                print(" %s |"%h_choice, end="")
            elif element==1:
                print(" %s |"%c_choice, end="")
            else:
                print("   |", end="")
        print()


# In[ ]:


def ai_turn(c_choice="X", h_choice="O"):
    """
    This function runs the ai turn.
    :param c_choice: how to mark AI's moves (X/O)
    :param h_choice: how to mark human's moves (X/O)
    :return: only changes the board state. returns None.
    """
    depth = len(empty_locations(board))
    if depth==0 or game_over(board):
        return 
    
    clean()
    players_markers = "HUMAN: %s; COMP: %s"%(h_choice, c_choice)
    print(players_markers)
    print('Computer turn [{}]\n'.format(c_choice))
    render(board, c_choice, h_choice) # prints current board.
    if depth==9: # random pick if it's first move
        x=np.random.choice([0,1,2])
        y=np.random.choice([0,1,2])
    else: # depth in the range of 1-8 - use the minimax to pick best move
        move = minimax(board, depth, COMP)
        (x,y) = move[0], move[1]
        
    set_move(x, y, COMP)
    time.sleep(1)   


# In[1]:


all_moves_string = """

| 1 | 2 | 3 |
| 4 | 5 | 6 |
| 7 | 8 | 9 |
"""


# In[ ]:


def human_turn(c_choice="X", h_choice="O"):
    """
    This function runs the human turn - the human player picks its move.
    :param c_choice: how to mark AI's moves (X/O)
    :param h_choice: how to mark human's moves (X/O)
    :return: only changes the board state. returns None.
    """
    depth = len(empty_locations(board))
    if depth==0 or game_over(board):
        return 
    
    # Dictionary of valid moves
    move = -1
    moves= dict()
    for i in range(3):
        for j in range(3):
            counter = i*3+j+1
            moves[counter] = [i, j] # eventually: moves={1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0]... 9:[2,2]}
            
    clean()
    players_markers = "HUMAN: %s; COMP: %s"%(h_choice, c_choice)
    print(players_markers)
    print('Human turn [{}]\n'.format(h_choice))
    render(board, c_choice, h_choice) # prints current board.
    print(all_moves_string)
    
    while (move<1 or move>9):
        try:
            move = int(input('Use nampad (only 0 to 9).'))
            coord = moves[move]
            try_move = set_move(coord[0], coord[1], HUMAN)
            
            if try_move==False:
                print('Bad Move!')
                move = -1
                
        except KeyboardInterrupt:
            print('Bye...')
            exit()
        except:
            print('Bad Choice')


# In[2]:


def main():
    """
    Main function that calls all functions
    """
    clean()
    h_choice = "-"
    
    while h_choice not in "OX":
        try:
            h_choice = input('Choose X or O\nChosen: ')
            h_choice = h_choice.upper()
        except KeyboardInterrupt:
            print('Bye')
            exit()
        except:
            print('Bad choice')

    # Setting computer's choice
    if h_choice == 'X':
        first = "HUMAN"
        c_choice = 'O'
    else:
        first="COMP"
        c_choice = 'X'

    # Human may starts first
    clean()

    # Main loop of this game
    while len(empty_locations(board)) > 0 and not game_over(board):
        if first == 'COMP':
            ai_turn(c_choice, h_choice)
            first = ''

        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    # Game over message
    if wins(board, HUMAN):
        clean()
        print('Human turn [{}]\n'.format(h_choice))
        render(board, c_choice, h_choice)
        print('\nYOU WIN!\n')
    elif wins(board, COMP):
        clean()
        print('Computer turn [{}]\n'.format(c_choice))
        render(board, c_choice, h_choice)
        print('\nYOU LOSE!\n')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('\nDRAW!\n')

    exit()


# In[ ]:


if __name__ == '__main__':
    main()

