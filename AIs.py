import random
import sys
import copy
from collections import Counter
import timeit
import time
import re

from Board import *

class Trait():
	def __init__(self):
		listOfBoardMethods = [[board.getWinningMoves, self.player, 0], [board.getWinningMoves, self.opponent, 1], [board.findForks, self.player, 2], [board.optimalCounterforking, opposingForks, 3], [board.opposingCorners,self.opponent, 4], [board.getEmptyCorners, 5], [board.getEmptySides, 6], [board.isCenterOpen, 7] ]
		random.shuffle(listOfBoardMethods)
		
		self.sequence = [listOfBoardMethods]
	def reproduce(self, otherSequence):
		newSequence = {}
		for trait in range(len(self.sequence)): 
			traits = [self.sequence[trait], otherSequence[trait]]
			random.shuffle(traits)
			if traits[0] not in newSequence.values():
				newSequence[trait] = traits[0]
			elif traits[1] not in newSequence.values():
				newSequence[trait] = traits[1]
				
		return newSequence
		
class AI():
	def __init__(self, xOrO):
		self.name = "randomAI"
		self.player = xOrO
		self.prevGamesMoves = []
		self.moveHistory = []
		self.weightedMoves = []
		self.prevGamesCalls = []
		self.callHistory = []
		self.moveCounter = 1
		if self.player == "x":
			self.opponent = "o"
		else:
			self.opponent = "x"
		
	def makeMove(self, board):
		#base class picks a random move
		legalMoves = board.getLegalMoves()
		random.shuffle(legalMoves)
		move = legalMoves[0]
		return self._move(board, move)
	
	def _move(self, board, move):
		self.moveHistory.append(move)
		self.moveCounter += 1
		return board.placeMove(move[0], move[1], self.player)

	def endGame(self, winOrLoss):
		self.prevGamesMoves.append([self.moveHistory, winOrLoss])
		textFile = open(self.player + ".txt", "a")
		for move in self.moveHistory:
			textFile.write(str(move))
		textFile.close()
		self.moveHistory = []
		self.moveCounter = 1
		
	def nextGeneration(self):
		self.prevGamesMoves = []
	
class notAI(AI):
	def makeMove(self, board):
		print board.displayBoard()
		input = raw_input("enter coord pair: ")
		input = input.split(" ")
		print input
		return self._move(board, (int(input[0]), int(input[1])))
		
class Perfect_AI(AI):
	def makeMove(self, board):
		#import pdb; pdb.set_trace()
		#find winning moves for the turn player
		lethalMoves = board.getWinningMoves(self.player)
		if lethalMoves != []:
			# print "lm"
			return self._move(board, lethalMoves[0])
		
		opposingLethalMoves = board.getWinningMoves(self.opponent)
		if opposingLethalMoves != []:
			# print "olm"
			return self._move(board, opposingLethalMoves[0])
		
		forks = board.findForks(self.player)
		if forks != []:
			# print "f"
			random.shuffle(forks)
			return self._move(board, forks[0])
		
		opposingForks = board.findForks(self.opponent)
		if opposingForks != []:
			# print "of"
			# print opposingForks
			return self._move(board, board.optimalCounterforking(opposingForks))
		if board.isCenterOpen() != []:
			# print "c"
			return self._move(board, (1, 1))
		
		opposingCorners = board.opposingCorners(self.opponent)
		if board.opposingCorners(self.opponent) != []:
			# print "oc"
			random.shuffle(opposingCorners)
			return self._move(board, opposingCorners[0])
		
		emptyCorners = board.getEmptyCorners()
		if emptyCorners != []:
			# print "ec"
			random.shuffle(emptyCorners)
			return self._move(board, emptyCorners[0])
		
		emptySides = board.getEmptySides()
		random.shuffle(emptySides)
		# print "es"
		return self._move(board, emptySides[0])
		
			
class AI2(AI):
	def makeMove(self, board):
		opposingForks = board.findForks(self.opponent)
		listOfBoardMethods = [[board.getWinningMoves, self.player, 0], [board.getWinningMoves, self.opponent, 1], [board.findForks, self.player, 2], [board.optimalCounterforking, opposingForks, 3], [board.opposingCorners,self.opponent, 4], [board.getEmptyCorners, 5], [board.getEmptySides, 6], [board.isCenterOpen, 7] ]
		random.shuffle(listOfBoardMethods)
		return self.validateAndExecute(board, listOfBoardMethods)
				
	def validateAndExecute(self, board, listOfBoardMethods):
		for method in listOfBoardMethods:
			moveSet = []
			call = ""
			if len(method) == 3:
				moveSet = method[0](method[1])
				call = method[2]
			else:
				moveSet = method[0]()
				call = method[1]
			if moveSet != []:
				if len(moveSet) > 1:
					random.shuffle(moveSet)
				return self._move(board, moveSet[0], call)
				
	def _move(self, board, move, call):
		self.callHistory.append([call, self.moveCounter])
		return AI._move(self, board, move)
		
	def endGame(self, winOrLoss):
		AI.endGame(self, winOrLoss)
		self.prevGamesCalls.append((self.callHistory, winOrLoss))
		textFile = open(self.player+"calls.txt", "a")
		for call in self.callHistory:
			textFile.write(str(call) + "\n")
		textFile.close()
		self.callHistory = []
		
class Genetic_AI2(AI2):
	def __init__(self, xOrO):
		listOfBoardMethods = [[board.getWinningMoves, self.player, 0], [board.getWinningMoves, self.opponent, 1], [board.findForks, self.player, 2], [board.optimalCounterforking, opposingForks, 3], [board.opposingCorners,self.opponent, 4], [board.getEmptyCorners, 5], [board.getEmptySides, 6], [board.isCenterOpen, 7] ]
		
		random.shuffle(listOfBoardMethods)
		self.sequence = [listOfBoardMethods]
		
		AI.__init__(self, xOrO)
		
	def MakeMove(self):
		return self.validateAndExecute(board, self.sequence)
		
	def nextGeneration(self):
		pass
				
class Genetic_AI(AI):	

	def nextGeneration(self):
		#fill a dictionary with all legal moves
		allMoves = {}
		totalMoves = Board().getLegalMoves()
		totalGames = len(self.prevGamesMoves)
		moveWinPairs = {}
		for move in totalMoves:
			allMoves[move] = 0
			moveWinPairs[move] = 0
		#for each game in the last generation
		for game in self.prevGamesMoves:
			if game[1] == "draw":
				for move in game[0]:
					moveWinPairs[move] += 1
				#totalGames -= 1
			if game[1] == "loss":
				for move in game[0]:
					allMoves[move] += 1
			if game[1] == "win":
				for move in game[0]:
					moveWinPairs[move] += 1
				
		#express strength as a percentage of total moves
		maxStrength = 0.01
		for move in allMoves:
			allMoves[move] = allMoves[move] / float(totalGames)
			if allMoves[move] > maxStrength:
				maxStrength = allMoves[move]
		
		#assign relative fitness values
		for move in allMoves:
			allMoves[move] = allMoves[move] / maxStrength
		
		#add a number of copies of the move to a new list, relative to the move's relative fitness
		retMoves = []
		for move in allMoves:
			for i in range (0, int(allMoves[move]*moveWinPairs[move]*100)):
				retMoves.append(move)
		self.weightedMoves = retMoves
		self.prevGamesMoves = []
		
	def makeMove(self, board):
		if self.weightedMoves == []:
			return AI.makeMove(self, board)
		else:
			legalMoves = board.getLegalMoves()
			random.shuffle(self.weightedMoves)
			for move in self.weightedMoves:
				if move in legalMoves:
					return self._move(board, move)
			return AI.makeMove(self, board)