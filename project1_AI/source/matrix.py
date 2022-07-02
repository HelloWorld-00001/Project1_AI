import numpy as np
import copy

def init_map(size):
    return np.array([["-" for _ in range(size)] for _ in range(size)])

def set(matrix, x, y, type):
    if matrix[x][y] == '-':
        matrix[x][y] = type
        return True
    return False
    
def draw_board(matrix):
    for i in range(0, 3):
        for j in range(0, 3):
            print('{}|'.format(matrix[i][j]), end=" ")
        print()
    print()
    
def is_valid(matrix, x, y):
    if x < matrix.shape[0]:
        if y < matrix.shape[1]:
            if matrix[x][y] == "X" or matrix[x][y] == "O":
                return 0
        else:
            return 0
    else:
        return 0
    return 1


        
#create child state
def make_child(matrix, type, list_idx_child):
    child = copy.deepcopy(matrix);
    size = matrix.shape[0]
    for i in range(size):
        for j in range(size):
            if child[i][j] == "-" and (i, j) not in list_idx_child:
                child[i][j] = type
                return child, (i, j)
    return None, None

def make_children( type):
    list_children = []
    list_idx_child = []
    while True:
        child, l_idx = make_child( type, list_idx_child)
        if child is None:
            break
        list_children.append(child)
        list_idx_child.append(l_idx)
    return list_children


def is_full(matrix):
            # Is whole board full?
    size = matrix.shape[0]
    for i in range(size):
        for j in range(size):
            # There's an empty field, we continue the game
            if (matrix[i][j] == "-"):
                return 0
    return 1

def vertical_win(matrix):
    size = matrix.shape[0]
    for i in range(size):
        if (all(x == "X" for x in matrix[:,i])):
                return 'X'
        elif (all(x == "O" for x in matrix[:,i])):
            return 'O'
    return None  

def horizontal_win(matrix):
    size = matrix.shape[0]
    for i in range(size):
        if (all(x == "X" for x in matrix[i])):
            return 'X'
        elif (all(x == "O" for x in matrix[i])):
            return 'O'
    return None 

def diagonal_win(matrix):
    size = matrix.shape[0]
    for i in range(size - 1):
        if (matrix[i][i] != matrix[i+1][i + 1]): #
            return "draw"
        return matrix[i][i]
    return None

def second_diagonal_win(matrix):
    size = matrix.shape[0]
    for i in range(size - 1):
        if (matrix[i][size - i - 1] != matrix[i + 1][size - i - 2]): #
            return "draw"
        return matrix[i][size - i - 1]
    return None

                
def is_end(matrix):
    if is_full(matrix):
    # Vertical win
        result = vertical_win(matrix)
        if result is not None:
            return result

        # Horizontal win
        result = horizontal_win(matrix)
        if result is not None:
            return result

        # Main diagonal win
        result = diagonal_win(matrix)
        if result is not None:
            return result
                

        # Second diagonal win
        result = second_diagonal_win(matrix)
        if result is not None:
            return result

    return None
