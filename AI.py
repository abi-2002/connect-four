from constants import *
import random
import settings

	
def Minimax(depth, isMax, alpha, beta, Mortal, Machine):
	Evaluation = CheckGameStatus(Mortal)
	if(depth == MAX_DEPTH or Evaluation != 1):
		return [Evaluation, None]

	LegalMoves = FindLegalMoves()
	random.shuffle(LegalMoves)
	if(isMax):
		bestScore = -100
		bestMove = 100
		for move in LegalMoves:
			if(move == None):
				continue		
			settings.GameBoard[move] = Machine
			score = Minimax(depth + 1, False,  alpha, beta, Mortal, Machine)[0]
			settings.GameBoard[move] = None
			if(score > bestScore):
				bestScore = score - depth
				bestMove = move
				alpha = max(bestScore, alpha)
				if(beta <= alpha):
					break
		return [bestScore, bestMove]
	else:
		bestScore = 100
		bestMove = 100
		for move in LegalMoves:
			if (move == None): 
				continue
			settings.GameBoard[move] = Mortal
			score = Minimax(depth + 1, True, alpha, beta, Mortal, Machine)[0]
			settings.GameBoard[move] = None
			if(score < bestScore):
				bestScore = score + depth
				bestMove = move
				beta = min(beta, bestScore)
				if(beta <= alpha):
					break
		return [bestScore, bestMove]

def FindLegalMoves():
	LegalMoves = []
	i = 0
	while(i < 42):
		if(settings.GameBoard[i] != None and i // 7 == 0):
			LegalMoves.append(None)
			if(i == 6):
				break
			i +=1 
			continue
		if(settings.GameBoard[i] != None):
			LegalMoves.append(i - 7)
			if(i % 7 == 6):
				break
			i = (i % 7) + 1
			continue
		if(i // 7 == 5):
			LegalMoves.append(i)
			if(i % 7 == 6):
				break
			i = (i % 7) + 1
		else:
			i += 7	

	return LegalMoves

def CheckGameStatus(Mortal):
	for position in WINNING_POSITIONS:
		
		if(settings.GameBoard[position[0]] == None or settings.GameBoard[position[1]] == None or settings.GameBoard[position[2]] == None or settings.GameBoard[position[3]] == None):
			continue

		if(settings.GameBoard[position[0]] == settings.GameBoard[position[1]] == settings.GameBoard[position[2]] == settings.GameBoard[position[3]]):
			settings.winning_position_pieces = [position[0], position[1],position[2],position[3]]
			if(settings.GameBoard[position[0]] == Mortal):
				return LOSE
			return WIN
			
	LegalMoves = FindLegalMoves()
	NumberOfLegalMoves = 0
	for move in LegalMoves:
		if(move != None):
			NumberOfLegalMoves += 1

	if(NumberOfLegalMoves == 0):
		return TIE

	return 1

