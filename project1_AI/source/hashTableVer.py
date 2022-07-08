import copy
import datetime as dt
import random as rd
import numpy as np

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
    
    def check_successor_end(): #is_end 7x7
        pass
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
    
    def is_end(self): #5x5, 3x3
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
    
        #tren dong no dnah co X hay k
        if any(self.map[y + n*j] == type for j in range(n))\
            and all(self.map[y + n*j] != reversed_type(type)  for j in range(n)):
                #tren dong do chua co O nao -> danh
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
        
    def make_child(self, list_idx_child):
        for i in range(self.size):
            if i not in list_idx_child and self.is_valid(i):
                return i
        return None
    
    def make_children(self, type):
        list_idx_child = []
        children = []
        
        while True:
            child_idx = self.make_child(list_idx_child)
            if child_idx is None:
                break
            list_idx_child.append(child_idx)
            
        for i in list_idx_child:
            child = copy.deepcopy(self) # tranh bi anh huong toi node cha
            child.map[i] = type # X/O
            children.append(child) # them con vao danh sach
            
        return children # tra ve danh sach con
    
    def first_heristic(self, pos, type):
        
        n_r = self.count_x_in_row("X") # 3
        n_c = self.count_x_in_col("X") #3
        n = self.sqrt_size # 3
        
        if n_r is not None: # co 3 x tren dong
            count = 0
            while True:

                #kiem tra nuoc di hop le
                if self.is_valid(pos) \
                    and any(n_r*n + j == pos for j in range(n))\
                        and all(self.map[n_r*n + j] != type for j in range(n)):
                    #kiem tra vi tri random do co nam tren dong do hay k
                    # kiem tra xem tren dong do co "O" nao chua
                    return True
                    
                pos = rd.randint(0, self.size - 1)
                count += 1
                if count >= self.size*2: break # size *2 
                
        if n_c is not None:
            count = 0
            while True:
                 #if pos in column n_c a and no type (X/O) in this row
                if self.is_valid(pos)\
                    and any(n_c + n*j == pos for j in range(n))\
                        and all(self.map[n_c + n*j] != type for j in range(n)):
                            
                        return True
                    
                pos = rd.randint(0, self.size - 1)
                count += 1
                if count >= self.size*2: break
        
        if self.is_valid(pos) and self.heuristic(pos, reversed_type(type)):
            return True
        return False
                
    def random_child(self, type):
        pos = rd.randint(0, self.size - 1)
        count = 0
        child = copy.deepcopy(self)


        while self.is_valid(pos) != 1:
            pos = rd.randint(0, self.size - 1) 
        # the heuristic
            if self.first_heristic(pos, type):
                child.map[pos] = type
                return child
            while  (self.heuristic(pos, reversed_type(type)) != 1):
                pos = rd.randint(0, self.size-1)
                count += 1
                if count >= self.size*2: break
        
        print("This is count " + str(count))
        child.map[pos] = type
        return child
    
    #for duyet het cac trang thai con theo hẻuritis
    #for childe in children:
    # ìf childe.first_heuristic():
    #   return child
    # elif childe.heuristic()
    #   retủrn child
    #return np.random.choice(children) 
    #return first
    
                  
        
   
    
    
    
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
        print("masy be here")
        #X 9 ->8->7 ...1 -> 9! trang thai con,  5x5: 25! duoi, 7x7 49! duoi
        #kiem tra xem trng thai con do con co bao nhieu o trong, > 10 o trong -> random successor
        #khoi chay thuat toan, con <=10 chay alpha beta
        #fisrt move always 
        successors = self.getSuccessors(node, type) # take all successors from current node
        best_state = None #initial best state
        
        #Browse each successor
        for state in successors:
            value = self.min_value(state, alpha, beta, start_time, time_limit)
            if value == 2:
                print("infinity loop??")
                best_state = node.random_child("O")
                print("Computer think: ")
                best_state.draw_board()
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
        
        result = self.getUtility(node) # 1 0 -1
        if result is not None:
            return result # return 
        
        infinity = float('inf')
        value = infinity 

        successors = self.getSuccessors(node, "X") # khoi tao con
        for state in successors:
            value = min(value, self.max_value(state, alpha, beta, start_time, time_limit))
            if value == 2: # vuot qua gioi han thoi gian
                return 2
            if value <= alpha:
                return value #prunning
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
                print("here is bug")        
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
        
