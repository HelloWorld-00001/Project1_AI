import pygame 
import hashTableVer as hb

# initializes pygame
pygame.init()
SIZE_T = 5
#Define color and size
SIZE = 600 # size of the screen size x size
BLACK = (0, 0, 0) # use for coloring line
WHITE = (255, 255, 255) # use for coloring O
RED = (255, 51, 51) # use for coloring X
PURPLE = (76, 0, 153) # use for message

LINE_SIZE = 5
BG_COLOR = (0,250,154) #green
#limit time
LIMIT_TIME = 5



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

    
def draw_figures(tic, n_lines):
    
    square_size = SIZE/n_lines
    x_ratio = SPACE/ n_lines * 3
    circle_ratio = square_size // 2
    
    n = tic.sqrt_size
    for i in range(tic.size):
        row, col = tic.get_board_position(i)
        if tic.map[i] == "O":
            pygame.draw.circle( screen, WHITE, (int( col * square_size + circle_ratio ), int( row * square_size + circle_ratio )), 180/n_lines, LINE_SIZE )
        elif tic.map[i] == "X":
            pygame.draw.line( screen, RED, (col * square_size + x_ratio, (row + 1) * square_size  - x_ratio), ((col + 1)* square_size - x_ratio, row * square_size + x_ratio), LINE_SIZE )	
            pygame.draw.line( screen, RED, (col * square_size + x_ratio, row * square_size + x_ratio), ((col + 1) * square_size - x_ratio, (row + 1) * square_size  - x_ratio), LINE_SIZE )

def catch_mouse(event, size_tic):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouseX = event.pos[0] # x
        mouseY = event.pos[1] # y

        clicked_row = int(mouseY // (SIZE/size_tic))
        clicked_col = int(mouseX // (SIZE/size_tic))
        return clicked_row*size_tic + clicked_col
    return None

 

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
def choose_size():
    size_ttt = int(input("Enter size of Tic Tac Toe (3/5/7): "))
    while size_ttt != 5 and size_ttt != 3 and size_ttt !=7:
        print("invalid size !!! please re-enter!")
        size_ttt = int(input("Enter size of Tic Tac Toe (3/5/7): "))
    return size_ttt



def main():

    #size = choose_size()
    size = 5
    tic = hb.TicTacToe(size)
    abp = hb.AlphaBeta(tic)     
    make_lines(size)
    game = True
    while game:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                game = False
            
        
            win = tic.is_end()
            if win != None:
                game_end_message(win)
                #game = False
            else:
                pos = catch_mouse(event, size)
                if pos != None:
                    if tic.is_valid(pos):
                        print(pos)
                        tic.set(pos, "X")
                        draw_figures(tic, size)
                        pygame.display.update()
                        print("bot is thinking.... ")
                        bot = abp.limit_alpha_beta(tic, LIMIT_TIME)
                        if bot != None:
                            tic = bot
                        draw_figures(tic, size)

        
        pygame.display.update()
        
main()

#main1()