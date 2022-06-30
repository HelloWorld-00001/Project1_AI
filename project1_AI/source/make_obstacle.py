import numpy as np

def make_obstacle(matrix, vertex):
    
    
    n = len(vertex)
    
    # set all vertex in matrix to 1
    for i in range(0, n - 1, 2):
        matrix[vertex[i]][vertex[i+1]] = 1
        
        
    # add first vertex to the end of the list vertex
    for i in range(2):
        vertex = np.append(vertex, vertex[i]) 
           
    for i in range(0, n - 1, 2):
        start, end, flag = find_start_end(vertex[i], vertex[i+1], vertex[i+ 2], vertex[i+3])        
        if (flag == 1):
            draw_in_row(matrix, start, end, vertex[i])
        elif (flag == 2):
            draw_in_diagonal(matrix, vertex[i], vertex[i+1], vertex[i+2], vertex[i+3])
        else:
            draw_in_col(matrix, start, end, vertex[i + 1])

def draw_in_col(matrix, start, end, col):
    for i in range(start, end):
        matrix[i][col] = 1

def draw_in_row(matrix, start, end, row):
    for i in range(start, end):
        matrix[row][i] = 1
        
def draw_in_diagonal(matrix, a1, a2, b1, b2):
    #case 1: if A(a1, a2), B(b1, b2) has a1 > b1 & a2 > b2
    if (a1 > b1) and (a2 > b2):
        for i in range(1, (a1 - b1)):
            matrix[b1 + i][b2 + i] = 1
    if (a1 < b1) and (a2 < b2):
        for i in range(1, (b1 - a1)):
            matrix[a1 + i][a2 + i] = 1
    if (a1 < b1) and (a2 > b2):
        for i in range(1, (b1 - a1)):
            matrix[a1 + i][a2 - i] = 1
    if (a1 > b1) and (a2 < b2):
        for i in range(1, (a1 - b1)):
            matrix[a1 - i][a2 + i] = 1
    
    
        
        
def find_start_end(v11, v12, v21, v22):
    flag = 0 # flag = 0 mean draw in column
    if ( abs(v21 - v11) < abs(v22 - v12)):
        flag = 1 # flag = 1 mean draw in row
        return min(v12, v22), max(v12, v22) , flag
    elif ( abs(v21 - v11) == abs(v22 - v12)):
        flag = 2 # flag = 1 mean draw in diagonal
        return min(v12, v22), max(v12, v22) , flag

    return min(v11, v21), max(v11, v21), flag
    
