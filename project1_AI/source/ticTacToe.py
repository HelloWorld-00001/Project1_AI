from multiprocessing.connection import wait
import pygame , sys
import alphabeta as ab
from time import sleep
# initializes pygame
pygame.init()

#Define color and size
SIZE = 600 # size of the screen size x size
BLACK = (0, 0, 0) # use for coloring line
WHITE = (255, 255, 255) # use for coloring O
RED = (255, 51, 51) # use for coloring X
PURPLE = (76, 0, 153) # use for message

LINE_SIZE = 10
BG_COLOR = (0,250,154) #green



SPACE = 55
# ------
# SCREEN
# ------
screen = pygame.display.set_mode( (SIZE, SIZE) )
pygame.display.set_caption( 'SUPER MEAG ULTRA ULTIMATE TIC TAC TOE' )
screen.fill( BG_COLOR )

def make_lines(n_lines):
    pygame.draw.line( screen, BLACK, (0, 0), (SIZE, 0), LINE_SIZE )
    pygame.draw.line( screen, BLACK, (0, 0), (0, SIZE), LINE_SIZE )
    pygame.draw.line( screen, BLACK, (SIZE, 0), (SIZE, SIZE), LINE_SIZE )
    pygame.draw.line( screen, BLACK, (0, SIZE), (SIZE, SIZE), LINE_SIZE )
    
    distance = SIZE/n_lines
    for i in range(1, n_lines):
        #column
        pygame.draw.line( screen, BLACK, (distance * i, 0), (distance * i, SIZE), LINE_SIZE )
        #row
        pygame.draw.line( screen, BLACK, (0, distance * i), (SIZE, distance * i), LINE_SIZE )

def draw_figures(map, n_lines):
    
    square_size = SIZE/n_lines
    for row in range(map.shape[0]):
        for col in range(map.shape[0]):
            if map[row][col] == "O":
                pygame.draw.circle( screen, WHITE, (int( col * square_size + square_size//2 ), int( row * square_size + square_size//2 )), 180/n_lines, LINE_SIZE )
            elif map[row][col] == "X":
                pygame.draw.line( screen, RED, (col * square_size + SPACE, row * square_size + square_size - SPACE), (col * square_size + square_size - SPACE, row * square_size + SPACE), LINE_SIZE )	
                pygame.draw.line( screen, RED, (col * square_size + SPACE, row * square_size + SPACE), (col * square_size + square_size - SPACE, row * square_size + square_size - SPACE), LINE_SIZE )

def catch_mouse(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouseX = event.pos[0] # x
        mouseY = event.pos[1] # y

        clicked_row = int(mouseY // (SIZE/3))
        clicked_col = int(mouseX // (SIZE/3))
        return clicked_row, clicked_col
    return None, None

 

def game_end_message(win):
    pygame.font.init()
    
    if ( win == "X"):
        text = "You win !"
    elif (win == "O"):
        text = "BOT win !"
    else:
        text = "--DRAW--"
    my_font = pygame.font.SysFont('Comic Sans MS', 50)
    text_surface = my_font.render(text, False, PURPLE)
    screen.blit(text_surface, (SIZE/2 - 100,SIZE/2 - 50))

#main
mapT = ab.TicTacToe(3)
alphaBeta = ab.AlphaBeta(mapT)
make_lines(3)
game = True


while game:
    for event in pygame.event.get():
         
        if event.type == pygame.QUIT:
    	    game = False
         
       
        win = mapT.is_end()
        if win != None:
            mapT.draw_board()
            game_end_message(win)
            #game = False
        else:
            x, y = catch_mouse(event)
            if x != None:
                if mapT.is_valid(x, y):
                    mapT.set(x, y, "X")
                    bot = alphaBeta.alpha_beta_search(mapT, "O")
                    if bot != None:
                        mapT = bot
                    draw_figures(mapT.map, 3)

    
    pygame.display.update()