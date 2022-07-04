import copy
import datetime as dt
import random as rd


def reversed_type(a):
    if (a == "X"):
        return "O"
    return "X"

class TicTacToe:
    def __init__(self, size):
        self.size = size **2
        self.map = {i:"-" for i in range(self.size)}
        self.sqrt_size = size
    
    def is_full(self):
        return all(i != "-" for i in self.map.values())
    
    def set(self, position, type):
        self.map[position] = type
        
    def is_valid(self, position):
        return self.map[position] == "-" and ( 0 <= position < self.size)
    
    def draw_board(self):
        for i in range(self.sqrt_size):
            for j in range(self.sqrt_size):
                print(self.map[i*self.sqrt_size + j], end=" | ")
            print()
    
    def vertical_win(self):
        
        n = self.sqrt_size
        
        for i in range(n):
            if all(self.map[i + n*j ] == "X" for j in range(n))\
                or all(self.map[i + n*j ] == "O" for j in range(n)):
                
                return self.map[i]
        return None
            
    def horizontal_win(self):
        
        n = self.sqrt_size
        for i in range(0, self.size, n):
            if all(self.map[i + j] == "X" for j in range(n))\
                or all(self.map[i + j] == "O" for j in range(n)):
        
                return self.map[i]
        return None

    def diagonal_win(self):
        
        n = self.sqrt_size
        if all(self.map[n*i + i] == "X" for i in range(n)) \
            or all(self.map[n*i + i] == "O" for i in range(n)):

            return self.map[0][0]
        return None
    
    def second_diagonal_win(self):
        
        n = self.sqrt_size
        if all(self.map[n*i - i] == "O" for i in range(1, n + 1))\
            or all(self.map[n*i - i] == "X" for i in range(1, n + 1)):
            
            return self.map[n - 1][0]
        
        return None
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
    
    def get_board_position(self ,position):
        column = position% self.sqrt_size
        row = position//self.sqrt_size
        return row, column
    
    def count_x_in_col(self, type):
        count = 0
        n = self.sqrt_size
        
        for i in range(n):
            for k in range(n):
                if self.map[i + n*k] ==  type:
                    count += 1
                    if count > 2:
                        return i # return column
            
            count = 0
        
        return None

    def count_x_in_row(self, type):
        count = 0
        n = self.sqrt_size
        for i in range(n):
            for j in range(n):
                if (self.map[n*i + j] ==  type):
                    count += 1
                    if count > 2:
                        return i # row
            
            count = 0
        
        return None
        
    def heuristic(self, pos, type):
        
        n = self.sqrt_size
        x, y = self.get_board_position(pos)
  
        #check same column

        if any(self.map[y + n*j] == type for j in range(n))\
            and all(self.map[y + n*j] != reversed_type(type)  for j in range(n)):
            return True
        # check same row
        elif any(self.map[n*x + j] == type for j in range(n))\
            and all(self.map[n*x + j] != reversed_type(type)  for j in range(n)):
            return True
        #check same diagonal
        elif (x == y) and\
            any(self.map[n*i + i] == type for i in range(n)):
            return True
        #check same secondary diagonal
        elif (x == n - y - 1) and\
            any(self.map[n*i - i] == type for i in range(n))\
            and all(self.map[n*i - i] != reversed_type(type)  for i in range(n)):
            return True
        return False
        
    def make_child(self, type, list_idx_child):
        child = copy.deepcopy(self)
        for i in range(self.size):
            if child.map[i] == "-" and i not in list_idx_child:
                child.map[i] = type
                return child, i
        return None, None
    
    def random_child(self, type):
        pos = rd.randint(0, self.size - 1)
        count = 0
        child = copy.deepcopy(self)


        # the heuristic
        n_r = self.count_x_in_row("X")
        n_c = self.count_x_in_col("X")
        n = self.sqrt_size
        test = 0
        if n_r is not None or n_c is not None:
            while True:
                if n_r is None:
                    # choose position in the same column
                    if any(n_c + n*j == pos for j in range(n))\
                        and self.is_valid(pos)\
                            and all(self.map[n_c + n*j] != type for j in range(n)):
                            break  
                    #choose the position of the same position
                elif n_r is not None:
                    if any(n_r*n + j == pos for j in range(n))\
                        and self.is_valid(pos)\
                        and all(self.map[n_r*n + j] != type for j in range(n)):
                            break
                pos = rd.randint(0, self.size - 1)
                count += 1
                if count >= self.size*2: break
        else:
            while self.is_valid(pos) != 1 and (self.heuristic(pos, reversed_type(type)) != 1):
                pos = rd.randint(0, self.size-1)
                count += 1
                if count >= self.size*2: break
      
        if self.is_valid(pos) and self.heuristic(pos, reversed_type(type)):
            child.map[pos] = type
            return child
            
            
        if count > self.size * 2 or count == 0:
            while self.is_valid(pos) != 1:
                pos = rd.randint(0, self.size - 1) 
        
        print("This is test " + str(test)) 
        print("This is count " + str(count))
        child.map[pos] = type
        return child
                  
        
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
    
    
    
### alpha beta prunning algorithm


class AlphaBeta:
    # print utility value of root node (assuming it is max)
    # print names of all nodes visited during search
    def __init__(self, game_tree):
        self.game_tree = game_tree.map  # GameTree
        #self.root = game_tree.root  # GameNode
        return

    def alpha_beta_search(self, node, type, start_time, time_limit):
        infinity = float('inf')
        alpha = - infinity #initial alpha = - infinity, beta = inf
        beta = infinity 
        
        #fisrt move always X
        successors = self.getSuccessors(node, type) # take all successors from current node
        best_state = None #initial best state
        
        #Browse each successor
        for state in successors:
            value = self.min_value(state, alpha, beta, start_time, time_limit)
            if value == 2:
                best_state = node.random_child("O")
                break
            if value > alpha:
                alpha = value
                best_state = state
            
        # print("AlphaBeta:  Utility Value of Root Node: = " + str(alpha))
        # print( "AlphaBeta:  Best State is: ")
        # best_state.draw_board()
        
        return best_state

    def max_value(self, node, alpha, beta,start_time, time_limit):
        
        if(node.size > 9):
            if (dt.datetime.now() - start_time >= time_limit):
                return 2
        
        result = self.getUtility(node)
        if result is not None:
            return result
        
        infinity = float('inf')
        value = - infinity

        successors = self.getSuccessors(node, "O")
        for state in successors:
            value = max(value, self.min_value(state, alpha, beta, start_time, time_limit))
            if value == 2:
                return 2
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value


    def min_value(self, node, alpha, beta, start_time, time_limit):

        if(node.size > 9):
            if (dt.datetime.now() - start_time >= time_limit):
                return 2
        
        result = self.getUtility(node)
        if result is not None:
            return result
        
        infinity = float('inf')
        value = infinity

        successors = self.getSuccessors(node, "X")
        for state in successors:
            value = min(value, self.max_value(state, alpha, beta, start_time, time_limit))
            if value == 2:
                return 2
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value
    #                   
    
    # alpha beta with limit time
    def limit_alpha_beta(self, node, LIMIT_TIME):
        start_time = dt.datetime.now()
        end_time = start_time + dt.timedelta(0, LIMIT_TIME)
        best = None
        count = 0
        
        if (node.size < 10): # if size of tic tac toe < 3x3 = 9 -> no limit
            inf_time = start_time + dt.timedelta(0, 1000000000)
            best = self.alpha_beta_search(node, "O", start_time, inf_time)
        else:
            while True:
                current_time = dt.datetime.now()
                if current_time > end_time:
                    break
                if (count == 0):
                    if node.is_valid((node.size + 1)/2):
                        node.map[(node.size - 1)/2] = "O"
                        best = node
                        return best
                        
                best = self.alpha_beta_search(node, "O", current_time, end_time - current_time)
                if node.is_full(): break
                if best is not None: break
                count +=1
        return best
    #                     
    # successor states in a game tree are the child nodes…
    def getSuccessors(self, node, state):
        children = node.make_children(state)
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
        


    #normal alphabeta:
    def ab_search(self, node, type):
        infinity = float('inf')
        alpha = - infinity #initial alpha = - infinity, beta = inf
        beta = infinity 
        
        #fisrt move always X
        successors = self.getSuccessors(node, type) # take all successors from current node
        best_state = None #initial best state
        
        #Browse each successor
        for state in successors:
            value = self.n_min_value(state, alpha, beta)
            if value > alpha:
                alpha = value
                best_state = state
            
        print("AlphaBeta:  Utility Value of Root Node: = " + str(alpha))
        print( "AlphaBeta:  Best State is: ")
        best_state.draw_board()
        
        return best_state

    def n_max_value(self, node, alpha, beta):

        result = self.getUtility(node)
        if result is not None:
            return result
        
        infinity = float('inf')
        value = - infinity

        successors = self.getSuccessors(node, "O")
        for state in successors:
            value = max(value, self.n_min_value(state, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value


    def n_min_value(self, node, alpha, beta):
        
        result = self.getUtility(node)
        if result is not None:
            return result
        
        infinity = float('inf')
        value = infinity

        successors = self.getSuccessors(node, "X")
        for state in successors:
            value = min(value, self.n_max_value(state, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value
        
        
# a = TicTacToe(4)
# a.map[2] = "X"
# b = AlphaBeta(a)
# b.ab_search(a, "O")




# a.draw_board()
# print("___________________________\n")
# children = a.make_children("X")
# for child in children:
#     child.draw_board()
#     print("-------------")
# a.map = {0:"O", 1:"X", 2:"O", 3:"X", 4: "O", 5:"X", 6:"X", 7:"O", 8: "X"}
# a.set(0, "X")
# a.set(0, "O")
# for i in range(a.size):
#     print(a.heuristic(i, "O")) # 0, 1, 2 - 1, 4, 7


            
# a.set(2, "O")
# a.set(4, "X")
# a.set(3, "X")
# a.set(5, "X")
# a.set(8, "O")
# a.draw_board()
# print(a.is_valid(2))
#print(a.is_end())
# a.draw_board()
