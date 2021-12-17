import pygame
from constants import *


def init():
    global GameBoard, clock, WINDOW, yellow, green, yellow_bright, green_bright, board_rect, board, arrow, arrow_rect
    global yellow_rect, green_rect, winning_position_pieces, win_ind
    GameBoard = [None for _ in range(42)]
    winning_position_pieces = []
    clock = pygame.time.Clock()                         # To set tick speed
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))   # Define pygame window
    pygame.display.set_caption('Connect Four')          # Window title
    WINDOW.fill(BACKGROUND)                             # Fill window colour


    #Load assets
    yellow = pygame.image.load('assets/yellow.png')
    green = pygame.image.load('assets/green.png')    
    yellow_bright = pygame.image.load('assets/yellow_bright.png')
    green_bright = pygame.image.load('assets/green_bright.png')
    board = pygame.image.load('assets/board.png')
    arrow = pygame.image.load('assets/arrow.png')
    win_ind = pygame.image.load('assets/win_in.png')


    # convert assets
    win_ind.convert()
    arrow.convert()
    yellow_bright.convert()
    green_bright.convert()
    yellow.convert()
    green.convert()
    board.convert()
   


    # get_rect and position the assets
    yellow_rect = yellow.get_rect()
    yellow_rect.center = YELLOW_CENTRE_X, YELLOW_CENTRE_Y
    green_rect = green.get_rect()
    green_rect.center = GREEN_CENTRE_X, GREEN_CENTRE_Y
    board_rect = board.get_rect()
    board_rect.center = WIDTH//2, HEIGHT//2

  
