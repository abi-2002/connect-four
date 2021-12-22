import settings
import AI
import time
import pygame
from pygame import mixer
from constants import *
import math


mixer.init()						# for sound effects
pygame.init()						# for sound effects
settings.init()						# loading globals
mixer.music.load("assets/beep.mp3")	# loading sounds
mixer.music.set_volume(0.08)		# set sound volume


# default values
CurrentPlayer = settings.yellow
Mortal = settings.yellow
Machine = settings.green

Win_Ind = settings.win_ind

GameOver = False

def IndexToCoordinates(index):										# Convert piece index to corresponding coordinates on surface
	return (index%7*100+295, index//7*100+63)

def Distance(x1, y1, x2, y2):										# Calculate distance from centre
	return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def Blit(piece, loc):												# Blit piece on surface
	settings.WINDOW.blit(piece, (loc))


def Animate(currentPiece, x_position, y_end, y_start = DROP_POINT):	# Animate inserting piece
    global VELOCITY
    while(y_start <= y_end):	
        if(y_start + VELOCITY > y_end):
            y_start = y_end
        settings.WINDOW.fill(BACKGROUND)
        Blit(currentPiece, (x_position, y_start))
        UpdateBoard()
        pygame.display.update()

        y_start += VELOCITY	
        VELOCITY += ACCELERATION
    mixer.music.play()
    VELOCITY = 2
   

def UpdateBoard():												# Display board with new pieces
	for i in range(len(settings.GameBoard)):
		if(settings.GameBoard[i] != None):
			settings.WINDOW.blit(settings.GameBoard[i], (IndexToCoordinates(i)))
	Blit(settings.board, settings.board_rect)

def Game():														# Mortal player's turn
    global CurrentPlayer
    clicked_x_coordinate, y = pygame.mouse.get_pos()			# getting clicked coordinates
    clicked_x_coordinate -=  295								# scaling
    if(clicked_x_coordinate % CELL_WIDTH > 80 or clicked_x_coordinate < BOARD_START or clicked_x_coordinate >= BOARD_END):
        return  								#return if x coordinate of clicked position is outside board or not on columns
    column_index = (clicked_x_coordinate // CELL_WIDTH)	
    LegalMoves = AI.FindLegalMoves()
    if(LegalMoves[column_index] == None):						# If there is no legal move on clicked column
        return 
    LegalMove = LegalMoves[column_index] 						# Corresponding legal move along the clicked column
    x_coordinate, y_coordinate = IndexToCoordinates(LegalMove)	# Get coordinates of the legal move
    Animate(CurrentPlayer, x_coordinate, y_coordinate)			# Animate making the move
    settings.GameBoard[LegalMove] = CurrentPlayer				# Update the board
    CurrentPlayer = Machine										# Toggle player

def DisplayText(Text):											# Display any text
    font = pygame.font.Font('assets/AdobeCleanRegular.otf', 40)	# Select font
    text = font.render(Text, True, (255, 255, 255))				# Text colour
    global textRect
    textRect = text.get_rect()
    textRect.center = (WIDTH//2, HEIGHT//3)
    Blit(text, textRect)


def OnClick():										# Choosing piece to play 
	global Mortal, Machine
	x,y = pygame.mouse.get_pos()					# Get clicked position
	dist_yellow = Distance(x, y, YELLOW_CENTRE_X, YELLOW_CENTRE_Y)	# Calculate distance from yellow piece centre
	dist_green = Distance(x, y, GREEN_CENTRE_X, GREEN_CENTRE_Y)	# Calculate distance from green piece centre
	if dist_yellow < PIECE_RADIUS:					# if distance from yellow centre is less than radius then the piece has been clicked
		Mortal = settings.yellow					# set mortal as yellow and machine as green
		Machine = settings.green	
		return True
	if dist_green < PIECE_RADIUS:					# if distance fron green centre is less than radius then the green piece has been clicked
		Mortal = settings.green						# set mortal as green and machine as yellow
		Machine = settings.yellow
		return True
	return False

def Hover():										#Arrow to show hoveWin_Ind column
	settings.WINDOW.fill(BACKGROUND)
	UpdateBoard()
	x, y = pygame.mouse.get_pos()
	x -= 295
	if y <= BOARD_TOP or y >= BOARD_BOTTOM or x <= BOARD_START or x >= BOARD_END or x % CELL_WIDTH > 80:
		return 										# if mouse is hoveWin_Ind outside board or not on columns 
	index = x // CELL_WIDTH							# get hoveWin_Ind index
	if AI.FindLegalMoves()[index] == None:			# if there is no legal move along hoveWin_Ind column, no hovering effect is given
		return
	x_pos = IndexToCoordinates(index)[0]			# get coordinate for hovering arrow
	x_pos += 25										# positioning hovering arrow
	Blit(settings.arrow, [x_pos, 25])				# blit arrow


def IntroHover():													#Hover effects at intro
	x, y = pygame.mouse.get_pos()									# Get mouse position
	dist_yellow = Distance(x, y, YELLOW_CENTRE_X, YELLOW_CENTRE_Y)  # Calculate distance from yellow centre
	dist_green = Distance(x, y, GREEN_CENTRE_X, GREEN_CENTRE_Y)		# Calculate distance from green centre

	if dist_yellow < PIECE_RADIUS:											# if distance from yellow centre less than radius show hover effects
		Blit(settings.yellow_bright, settings.yellow_rect)			# yellow bright is blitted at yellow rect for hovering effect
		Blit(settings.green, settings.green_rect)					# regular green is blitted at green rect
		return
	
	Blit(settings.yellow, settings.yellow_rect)						# if distance greater than radius, no hovering effect and regular yellow is blitted
	
	if dist_green < PIECE_RADIUS:												# if distance from green centre less than radius show hover effects
		Blit(settings.green_bright, settings.green_rect)			# green bright is blitted
		return
	
	Blit(settings.green, settings.green_rect)						# regular green blited if distance greater than radius


def Intro():											# When game starts
	intro = True
	
	while(intro):
		settings.clock.tick(FPS)						# set fps
		settings.WINDOW.fill(BACKGROUND)				# filling background colour
		DisplayText('Choose your fighter')				# display text
		for event in pygame.event.get():
			if event.type == pygame.QUIT:			
				intro = False
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:	# if mouse button is pressed
				mouse = pygame.mouse.get_pressed()
				if mouse[0]:							# and it is left-click
					if(OnClick()):						# call the on click listener
						intro = False			
		IntroHover()									# hover effects

		pygame.display.update()
        
def GameOverAnimate():
        time.sleep(1)
        Blit(Win_Ind, (IndexToCoordinates(settings.winning_position_pieces[0])[0], IndexToCoordinates(settings.winning_position_pieces[0])[1] ))

        Blit(Win_Ind, (IndexToCoordinates(settings.winning_position_pieces[1])[0], IndexToCoordinates(settings.winning_position_pieces[1])[1] ))
        Blit(Win_Ind, (IndexToCoordinates(settings.winning_position_pieces[2])[0] , IndexToCoordinates(settings.winning_position_pieces[2])[1]))
        Blit(Win_Ind, (IndexToCoordinates(settings.winning_position_pieces[3])[0] , IndexToCoordinates(settings.winning_position_pieces[3])[1]))
        Blit(settings.board, settings.board_rect)
        pygame.display.update()
        time.sleep(2)

def End(GameStat):										# Message after game ends
	time.sleep(0.5)
	pygame.draw.rect(settings.WINDOW, (10, 10, 10), (WIDTH//2 - 150, HEIGHT//2 - 200, 300, 200))	# Message box (surface, (colour), (x, y, width, height))
	
	if (GameStat == WIN):	
		DisplayText("You lost")											# the text 
		pygame.display.update()
		return

	if(GameStat == LOSE):
		DisplayText("You won")
		pygame.display.update()
		return
	
	if (GameStat == TIE):
		DisplayText("Tie")
		pygame.display.update()
		return
def Main():
	global GameOver, CurrentPlayer
	run = True
	settings.WINDOW.fill(BACKGROUND)
	UpdateBoard()
	while(not(GameOver) and run):
		settings.clock.tick(FPS)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
			Hover()
			if CurrentPlayer == Mortal:
				if event.type == pygame.MOUSEBUTTONDOWN:
					mouse = pygame.mouse.get_pressed()
					if(mouse[0]):
						Game()
			else:
				time.sleep(0.5)
				move = AI.Minimax(0, True, -100, 100, Mortal, Machine)[1]
				x, y = IndexToCoordinates(move)
				Animate(Machine, x, y)
				settings.GameBoard[move] = CurrentPlayer
				CurrentPlayer = Mortal
			
			GameStat = AI.CheckGameStatus(Mortal)
			
			if GameStat != 1:	# If game has ended
				GameOver = True
				if(GameStat != TIE):
					GameOverAnimate()
				End(GameStat)
				time.sleep(2)
				break

		pygame.display.update()
	
if __name__ == "__main__":
	Intro()
	Main()

	
