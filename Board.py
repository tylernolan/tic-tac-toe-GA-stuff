import random
import sys
import copy
from collections import Counter
import timeit
import time
import re


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap
		
class Board():
	ILLEGAL_MOVE = "ILLEGAL MOVE"
	X_VICTORY = "X WIN"
	O_VICTORY = "O WIN"
	DRAW = "DRAW"
	def __init__(self):
		self.board = [["e" for i in range(3)] for j in range(3)]
		
	def isCenterOpen(self):
		if self.board[1][1] == "e":
			return [(1, 1)]
		else:
			return []
	def getEmptySides(self):
		#sides are (0, 1), (1, 0), (2, 1), (1, 2)
		emptySides = []
		if self.board[0][1] == "e":
			emptySides.append((0, 1))
		if self.board[1][0] == "e":
			emptySides.append((1, 0))
		if self.board[2][1] == "e":
			emptySides.append((2, 1))
		if self.board[1][2] == "e":
			emptySides.append((1, 2))
		return emptySides
	def getEmptyCorners(self):
		emptyCorners = []
		if self.board[0][0] == "e": 
			emptyCorners.append((0, 0))
		if self.board[2][0] == "e": 
			emptyCorners.append((2, 0))
		if self.board[2][2] == "e":
			emptyCorners.append((2, 2))
		if self.board[0][2] == "e": 
			emptyCorners.append((0, 2))
		return emptyCorners
	
	def optimalCounterforking(self, opposingForks):
		if len(opposingForks) == 0:
			return []
		elif len(opposingForks) == 2 and self.getEmptySides() != []:
			emptySides = self.getEmptySides()
			random.shuffle(emptySides)
			return [emptySides[0]]
		elif len(opposingForks) == 4 and self.getEmptyCorners() != []:
			emptyCorners = self.getEmptyCorners()
			random.shuffle(emptyCorners)
			return [emptyCorners[0]]
		else:
			random.shuffle(opposingForks)
			return [opposingForks[0]]
		
	def opposingCorners(self, opponent):
		#corners are: (0, 0), (2, 0), (2, 2), (0, 2)
		#opposing corners are: [(0, 0), (2, 2)] and [(2, 0), (0, 2)]
		oppCorners = []
		if self.board[0][0] == opponent and self.board[2][2] == "e":
			oppCorners.append((2, 2))
		if self.board[2][2] == opponent and self.board[0][0] == "e":
			oppCorners.append((0, 0))
		if self.board[2][0] == opponent and self.board[0][2] == "e":
			oppCorners.append((0, 2))
		if self.board[0][2] == opponent and self.board[2][0] == "e":
			oppCorners.append((2, 0))
		return oppCorners
		
	#returns 4 if player X won
	#returns 2 if player O won
	#returns 3 if the game is drawn
	#returns False if move was illegal
	#returns True if the game continues
	def placeMove(self, x ,y, player):
		if self.board[x][y] == "e":
			self.board[x][y] = player
			result = self.checkForWin()
			if result == "x":
				return self.X_VICTORY
			elif result == "o":
				return self.O_VICTORY
			elif result == "d":
				return self.DRAW
			else:
				return True
		else:
			raise NameError('tried to play a move in an occupied square!')
		
	def getWinningMoves(self, player):
		winningMoves = []
		for move in self.getLegalMoves():
			copiedBoard = copy.deepcopy(self)
			copiedBoard.placeMove(move[0], move[1], player)
			resultOfMove = copiedBoard.checkForWin()
			if resultOfMove == player:
				winningMoves.append(move)
				
		return winningMoves
	
	def findForks(self, player):
		#given a free move, can the player setup 2 wins?
		forkingMoves = []
		for move in self.getLegalMoves():
			copiedBoard = copy.deepcopy(self)
			copiedBoard.placeMove(move[0], move[1], player)
			possibleWins = copiedBoard.getWinningMoves(player)
			if len(possibleWins) > 1:
				forkingMoves.append(move)
		return forkingMoves
		
	#returns x if player X has won, o if player O has won, d if the game is drawn, and e if the game isn't over.
	def checkForWin(self):
		#check all rows
		for x in range(0,3):
			if self.board[x][0] == self.board[x][1] and self.board[x][1] == self.board[x][2] and self.board[x][0] != "e":
				return self.board[x][0]
		#check all columns
		for y in range(0,3):
			if self.board[0][y] == self.board[1][y] and self.board[1][y] == self.board[2][y] and self.board[0][y] != "e":
				return self.board[0][y]
		#check both diagonals
		if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and self.board[0][0] != "e":
			return self.board[0][0]
		elif self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0] and self.board[0][2] != "e":
			return self.board[0][2]
		else:
			if self.getLegalMoves() == []:
				return "d"
			return "e"

	def getLegalMoves(self):
		legalMoves = []
		for x in range(0,3):
			for y in range(0,3):
				if self.board[x][y] == "e":
					legalMoves.append((x,y))
		return legalMoves
	
	def displayBoard(self):
		retString = self.board[0][0] +" "+ self.board[1][0] +" " +self.board[2][0] + "\n"
		retString += self.board[0][1] +" "+ self.board[1][1] +" " +self.board[2][1] + "\n"
		retString += self.board[0][2] +" "+ self.board[1][2] +" " +self.board[2][2] + "\n"
		return retString

		
