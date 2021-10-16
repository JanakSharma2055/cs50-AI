"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

count = 1


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    
    """
    Returns player who has the next turn on a board.
    """
    count_x =0
    count_o =0
    for row in board:
        for col in row:
            if col == X:
                count_x=count_x+1
            elif col == O:
                count_o =count_o +1
        
    if count_o >= count_x:
        return X
    elif count_x>count_o:
        return O



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    avail_actions = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if(board[i][j] is  EMPTY):
                avail_actions.append((i, j))

    return avail_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    global count
    row_line,col_line =action
    
    
    if board[row_line][col_line] is not EMPTY:
        raise NameError('Invalid Move')
    
    else:
        temp_board =copy.deepcopy(board)
       
        temp_board[row_line][col_line]=player(board)
       
    
    return temp_board
    
   


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner = None
    #checking in rows
    for row in board:
        if len(set(row)) == 1:
            winner =row[0]
    #checking diagonals
    if len(set([board[i][i] for i in range(len(board))])) == 1:
        winner= board[0][0]
    if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1:
        winner= board[0][len(board)-1]   
    
    #check column by transposing
    for row in list(map(list, zip(*board))):
        if len(set(row)) == 1:
            winner =row[0]

    return winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    else:
        terminated = True
        for i in range(len(board)):
            for j in range(len(board[i])):
                if(board[i][j] is EMPTY):
                    terminated =False
        
        return terminated
    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) ==X:
        return 1
    elif winner(board) ==O:
        return -1
    else:
        return 0
    

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    avail_actions =actions(board)
    #return middle pos initially
    if(len(avail_actions)) ==9:
        return (1,1)
    selected_action = None
    if player(board) ==X:
        maximizing_val = -math.inf  
        
        for action in avail_actions:
            temp_val = minValue(result(board,action))
            if temp_val> maximizing_val:
                maximizing_val =temp_val
                selected_action=action


    elif player(board) ==O:
        minimizing_val = math.inf  
        for action in avail_actions:
            temp_val = maxValue(result(board,action))
            if temp_val < minimizing_val:
                minimizing_val =temp_val
                selected_action =action

    return selected_action


def minValue(board):
    if terminal(board):
        return utility(board)
    min_val =  math.inf
    for action in actions(board):
        min_val = min(min_val, maxValue(result(board,action)))
    return min_val

def maxValue(board):
    if terminal(board):
        return utility(board)
    max_val =  -math.inf
    for action in actions(board):
        max_val = max(max_val, minValue(result(board,action)))
    return max_val
    