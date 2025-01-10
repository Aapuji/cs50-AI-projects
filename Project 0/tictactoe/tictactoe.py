"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


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
    n = 0

    for row in board:
        for cell in row:
            if cell == X:
                n += 1
            elif cell == O:
                n -= 1
    
    if n == 0:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is EMPTY:
                moves.add((i, j))

    return moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] is not EMPTY:
        raise Exception("Invalid action")
    
    char = player(board)

    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = char

    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    def check_for_winner(char):
        for i in range(len(board)):
            if all(cell == char for cell in board[i]):
                return True
        
        cols_true = [True for cell in board[0]]
        for i in range(len(board[0])):
            cols_true[i] = True

            for row in board:
                if row[i] != char:
                    cols_true[i] = False
                    break
        
        if any(cols_true):
            return True
        
        is_true = True
        for i in range(len(board)):
            if board[i][i] != char:
                is_true = False
                break
        
        if is_true:
            return True
        
        is_true = True
        for i in range(len(board)):
            if board[i][-i-1] != char:
                is_true = False
                break
        
        return is_true

    if check_for_winner(X):
        return X
    
    if check_for_winner(O):
        return O
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    any_empty = False
    for row in board:
        for cell in row:
            if cell is EMPTY:
                any_empty = True
                break
        
        if any_empty:
            break
    
    if not any_empty:
        return True

    return winner(board) is not None

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    won = winner(board)

    if won == X:
        return 1
    
    if won == O:
        return -1
    
    return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None
    
    char = player(board)
    moves = actions(board)

    best_move = None
    best_utility = -math.inf if char == X else math.inf

    for move in moves:
        outcome = result(board, move)

        minimax_result = minimax(outcome)

        if minimax_result is None:
            util = utility(outcome)

            if char == X:
                if util >= best_utility:
                    best_move = move
                    best_utility = util
            else:
                if util <= best_utility:
                    best_move = move
                    best_utility = util
            
            continue

        outcome = result(outcome, minimax_result)
        util = value(outcome)

        if char == X:
            if util >= best_utility:
                best_move = move
                best_utility = util
        else:
            if util <= best_utility:
                best_move = move
                best_utility = util
    
    return best_move

def value(board):
    """
    Returns the value of a given board, even if it isn't finished
    """

    if terminal(board):
        return utility(board)
    
    current_player = player(board)
    moves = actions(board)

    best_value = -10 if current_player == X else 10 

    for move in moves:
        outcome = result(board, move)

        new_value = value(outcome)
        if current_player == X:
            if new_value > best_value:
                best_value = new_value
        elif current_player == O:
            if new_value < best_value: 
                best_value = new_value
    
    return best_value
        


