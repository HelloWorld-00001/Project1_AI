import time
import numpy as np

class TicTacToe:
    def __init__(self, size):
        self.size = size
        self.map = np.array([["-" for _ in range(self.size)] for _ in range(self.size)])
        self.player_turn = 'X'

    def draw_board(self):
        for i in range(0, 3):
            for j in range(0, 3):
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

    def is_full(self):
                # Is whole board full?
        for i in range(self.size):
            for j in range(self.size):
                # There's an empty field, we continue the game
                if (self.map[i][j] == "-"):
                    return 0
        return 1
                
    def is_end(self):
        

                
        # Vertical win
        for i in range(0, 3):
            if (all(x == "X" for x in self.map[:,i])):
                    return 'X'
            elif (all(x == "O" for x in self.map[:,i])):
                return 'O'

        # Horizontal win
        for i in range(self.size):
            if (all(x == "X" for x in self.map[i])):
                return 'X'
            elif (all(x == "O" for x in self.map[i])):
                return 'O'

        # Main diagonal win
        for i in range(self.size - 1):
            if (self.map[i][i] != self.map[i+1][i + 1]): #
                return "draw"
            return self.map[i][i]
                

        # Second diagonal win
        for i in range(self.size - 1):
            #0, 3-0-1=2 <=> 0 + 1 = 1, 3 - 0 - 1 = 2
            if (self.map[i][self.size - i - 1] != self.map[i + 1][self.size - i - 2]): #
                return "draw"
            return self.map[i][self.size - i - 1]

       

        # It's a tie!
        return None

    def max_alpha_beta(self, alpha, beta):
            maxv = -2
            px = None
            py = None

            result = self.is_end()

            if result == 'X':
                return (-1, 0, 0)
            elif result == 'O':
                return (1, 0, 0)
            elif result == "-":
                return (0, 0, 0)

            for i in range(0, 3):
                for j in range(0, 3):
                    if self.map[i][j] == "-":
                        self.map[i][j] = 'O'
                        (m, min_i, in_j) = self.min_alpha_beta(alpha, beta)
                        if m > maxv:
                            maxv = m
                            px = i
                            py = j
                        self.map[i][j] = "-"

                        # Next two ifs in Max and Min are the only difference between regular algorithm and minimax
                        if maxv >= beta:
                            return (maxv, px, py)

                        if maxv > alpha:
                            alpha = maxv

            return (maxv, px, py)
        
    def min_alpha_beta(self, alpha, beta):
        
            minv = 2

            qx = None
            qy = None

            result = self.is_end()

            if result == 'X':
                return (-1, 0, 0)
            elif result == 'O':
                return (1, 0, 0)
            elif result == "-":
                return (0, 0, 0)

            for i in range(0, 3):
                for j in range(0, 3):
                    if self.map[i][j] == "-":
                        self.map[i][j] = 'X' 
                        (m, max_i, max_j) = self.max_alpha_beta(alpha, beta)
                        if m < minv:
                            minv = m
                            qx = i
                            qy = j
                        self.map[i][j] = "-"

                        if minv <= alpha:
                            return (minv, qx, qy)

                        if minv < beta:
                            beta = minv

            return (minv, qx, qy)
    def play_alpha_beta(self):
        while True:
            self.draw_board()
            self.result = self.is_end()

     
            if self.result == 'X':
                print('The winner is X!')
                break
            elif self.result == 'O':
                print('The winner is O!')
                break


            if self.player_turn == 'X':

                while True:
                    start = time.time()
                    (m, qx, qy) = self.min_alpha_beta(-2, 2)
                    end = time.time()
                    print('Evaluation time: {}s'.format(round(end - start, 7)))
                    print('Recommended move: X = {}, Y = {}'.format(qx, qy))

                    px = int(input('Insert the X coordinate: '))
                    py = int(input('Insert the Y coordinate: '))

                    qx = px
                    qy = py

                    if self.is_valid(px, py):
                        self.map[px][py] = 'X'
                        self.player_turn = 'O'
                        break
                    else:
                        print('The move is not valid! Try again.')

            else:
                (m, px, py) = self.max_alpha_beta(-2, 2)
                self.map[px][py] = 'O'
                self.player_turn = 'X'
                
def main():
    g = TicTacToe(3)
    g.play_alpha_beta()

if __name__ == "__main__":
    main()