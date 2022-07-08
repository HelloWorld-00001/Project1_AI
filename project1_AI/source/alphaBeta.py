import numpy as np
import copy

class AlphaBeta:
    # print utility value of root node (assuming it is max)
    # print names of all nodes visited during search
    def __init__(self, game_tree):
        self.game_tree = game_tree.map  # GameTree
        #self.root = game_tree.root  # GameNode
        return

    def alpha_beta_search(self, node, type):
        infinity = float('inf')
        alpha = - infinity #initial alpha = - infinity, beta = inf
        beta = infinity 
        
        #fisrt move always X
        successors = self.getSuccessors(node, type) # take all successors from current node
        best_state = None #initial best state
        
        #Browse each successor
        for state in successors:
            value = self.min_value(state, alpha, beta)
            if value > alpha:
                alpha = value
                best_state = state
        # print("AlphaBeta:  Utility Value of Root Node: = " + str(alpha))
        # print( "AlphaBeta:  Best State is: ")
        # best_state.draw_board()
        
        return best_state

    def max_value(self, node, alpha, beta):

        
        result = self.getUtility(node)
        if result is not None:
            return result
        
        infinity = float('inf')
        value = - infinity

        successors = self.getSuccessors(node, "O")
        for state in successors:
            value = max(value, self.min_value(state, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value


    def min_value(self, node, alpha, beta):

        result = self.getUtility(node)
        if result is not None:
            return result
        
        infinity = float('inf')
        value = infinity

        successors = self.getSuccessors(node, "X")
        for state in successors:
            value = min(value, self.max_value(state, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value
    #                     
    # successor states in a game tree are the child nodes…
    def getSuccessors(self, node, state):
        children = np.array(node.make_children(state))
        return children

    def getUtility(self, node):
        x = node.is_end()
        if ( x == "O"):
            return 1
        elif ( x == "X"):
            return -1
        elif ( x == "draw"):
            return 0
        else:
            return None
        
class TicTacToe:
    def __init__(self, size):
        self.size = size
        self.map = np.array([["-" for _ in range(self.size)] for _ in range(self.size)])
        self.player_turn = 'X'

    def set(self, x, y, type):
        
        if self.map[x][y] == '-':
            self.map[x][y] = type
            return True
        return False
        
    def draw_board(self):
        if (self.map.shape[0] == 0):
            return "nothing"
        for i in range(self.size):
            for j in range(self.size):
                print('{}|'.format(self.map[i][j]), end=" ")
            print()
        print()
        
    def is_valid(self, x, y):
        if x < self.map.shape[0]:
            if y < self.map.shape[1]:
                if self.map[x][y] == "X" or self.map[x][y] == "O":
                    return 0
            else:
                return 0
        else:
            return 0
        return 1

    
            
    #create child state
    def make_child(self, type, list_idx_child):
        child = copy.deepcopy(self);
        for i in range(self.size):
            for j in range(self.size):
                if child.map[i][j] == "-" and (i, j) not in list_idx_child:
                    child.map[i][j] = type
                    return child, (i, j)
        return None, None
    
    def make_children(self, type):
        list_children = []
        list_idx_child = []
        while True:
            child, l_idx = self.make_child( type, list_idx_child)
            if child is None:
                break
            list_children.append(child)
            list_idx_child.append(l_idx)
        return list_children

    
    def is_full(self):
        for i in range(self.size):
            for j in range(self.size):
                # There's an empty field, we continue the game
                if (self.map[i][j] == "-"):
                    return 0
        return 1
    
    def vertical_win(self):
        for i in range(self.size):
            if (all(x == "X" for x in self.map[:,i])):
                    return 'X'
            elif (all(x == "O" for x in self.map[:,i])):
                return 'O'
        return None  
    
    def horizontal_win(self):
        for i in range(self.size):
            if (all(x == "X" for x in self.map[i])):
                return 'X'
            elif (all(x == "O" for x in self.map[i])):
                return 'O'
        return None 
    
    def diagonal_win(self):
        for i in range(self.size - 1):
            if (self.map[i][i] != self.map[i+1][i + 1]) or self.map[i][i] == "-": #
                return None
        return self.map[0][0]
    
    def second_diagonal_win(self):
        for i in range(self.size - 1):
            if (self.map[i][self.size - i - 1] != self.map[i + 1][self.size - i - 2]) or self.map[i][self.size - i - 1] == "-": #
                return None
        return self.map[0][self.size-1]
    
    def split_matrix(self):
        sub_map = TicTacToe(3)
        
        n = self.size - 2
        for k in range(n):#make all submatrix
            for i in range(n): #make a submatrix
                for j in range(n):
                    sub_map.map[j] = self.map[j+k, i:i+3]
                if (sub_map.is_end() is not None):
                    if (sub_map.is_end() != "draw"): # if submatrix has any win -> return result
                        return sub_map
        return None #if no result return none     
          
    def is_end(self):
        #if(self.map.shape[0] > 3):
        #    self.split_matrix()
        #Vertical win
        result = self.vertical_win()
        if result is not None:
            return result

        # Horizontal win
        result = self.horizontal_win()
        if result is not None:
            return result

        # Main diagonal win
        result = self.diagonal_win()
        if result is not None:
            return result
                

        # Second diagonal win
        result = self.second_diagonal_win()
        if result is not None:
            return result
        
        if self.is_full():
            return "draw"
        return None

def menu(a, b):
    print(a.is_end())
    while a.is_end() is None:
        x = int(input("Your move, input x: "))
        y = int(input("Your move, input y: "))
        while a.is_valid(x, y) == 0:
            print("wrong index: please re-enter")
            x = int(input("Your move, input x: "))
            y = int(input("Your move, input y: "))
        a.set(x, y, "X")
        bot = b.alpha_beta_search(a, "O")
        a = bot
        a.draw_board()
        
        
        

#menu(a, b)
# a.set(0, 2, "X")
# a.draw_board()
# b.alpha_beta_search(a, "O")
