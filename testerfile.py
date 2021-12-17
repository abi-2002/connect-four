
from constants import WINNING_POSITIONS, WIDTH, HEIGHT, BACKGROUND
import pygame
import time

gameBoard = [None for _ in range(42)]
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

WINDOW.fill(BACKGROUND)

piece = pygame.image.load('assets/yellow.png')
piece.convert()
board = pygame.image.load('assets/board.png')
board.convert()

boardRect = board.get_rect()
boardRect.center = WIDTH//2, HEIGHT//2

def IndexToCoordinates(index):
	x = index%7*100+295
	y = index//7*100+64
	return (x, y)



def BoardPrint(position):
    global gameBoard
    for pos in position:
        gameBoard[pos] = piece
    for i in range(len(gameBoard)):
        if gameBoard[i] != None:
            WINDOW.blit(piece, IndexToCoordinates(i))
    WINDOW.blit(board, boardRect)
    pygame.display.update()
    for pos in position:
        gameBoard[pos] = None

clock = pygame.time.Clock()

run = True
while(run):
    
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        
    for position in WINNING_POSITIONS:
        WINDOW.fill(BACKGROUND)
        BoardPrint(position)
        time.sleep(0.75)
    pygame.display.update()

