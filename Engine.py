from Board import *
from AIs import *
import random
import sys
import copy
from collections import Counter
import timeit
import time
import re
class Engine():
	def __init__(self):
		for runs in range(0,1):
			self.board = Board()
			self.playerO = Perfect_AI("o") #player 2 AI
			self.playerX = Genetic_AI("x") #player 1 AI
			self.startingPlayer = self.playerX
			self.results = {}
			for genCount in range(0, 50):
				for gameCount in range(0, 100):
					self.currentPlayer = self.startingPlayer
					result = True
					while result == True:
						result = self.play()
					try:
						self.results[result]+=1
					except:
						self.results[result]=1
					self.newGame(result)
					gameCount += 1
				self.playerX.nextGeneration()
				self.playerO.nextGeneration()
				self.displayResults()
	def alternatePlayers(self):
		if self.startingPlayer == self.playerX:
			self.startingPlayer = self.playerO
		else:
			self.startingPlayer = self.playerX
	def newGame(self, result):
		#alternates between the two starting players
		#self.alternatePlayers()
		if result == Board.X_VICTORY:
			self.playerX.endGame("win")
			self.playerO.endGame("loss")
		if result == Board.O_VICTORY:
			self.playerX.endGame("loss")
			self.playerO.endGame("win")
		if result == Board.DRAW:
			self.playerX.endGame("draw")
			self.playerO.endGame("draw")
			
		self.board = Board()

	def play(self):
		result = self.currentPlayer.makeMove(self.board)
		if result == None:
			raise NameError("\n"+self.board.displayBoard())
		
		if self.currentPlayer == self.playerX:
			self.currentPlayer = self.playerO
		else:
			self.currentPlayer = self.playerX
		return result

	def displayResults(self):
		for key in self.results:
			print str(key) + " " + str(self.results[key])
		print "\n"
		
class Analyzer():
	def __init__(self, file):
		file = open(file, 'r')
		file = file.read()
		moves = []
		file = file.split("(")
		for thing in file:
			if thing == "":
				continue
			thing = thing.strip(")")
			thing = thing.split(",")
			tup = (int(thing[0]), int(thing[1].strip()))
			moves.append(tup)
		moves = Counter(moves)
		self.printMoveGrid(moves)
		
	def printMoveGrid(self, moves):
		str1 = str(moves[(0, 0)]) + "|" + str(moves[(0, 1)]) + "|" + str(moves[(0, 2)]) + "\n"
		str2 = (str(moves[(1, 0)]) + "|" + str(moves[(1, 1)]) + "|" + str(moves[(1, 2)]) + "\n")
		str3 = (str(moves[(2, 0)]) + "|" + str(moves[(2, 1)]) + "|" + str(moves[(2, 2)]) + "\n")
		print str1 + str2 + str3
		file = open("moves.txt", 'a')
		file.write("\n" + str1+str2+str3)
		file.close
		
		
			
file = open("o.txt", 'w')
file.close()
file = open("ocalls.txt", 'w')
file.close()
file = open("xcalls.txt", 'w')
file.close()
file = open("x.txt", 'w')
file.close()

Engine()
print "o file: \n"
Analyzer("o.txt")
print "x file: \n"
Analyzer("x.txt")		