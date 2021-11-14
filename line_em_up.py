# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import numpy as np
import time
import sys

class Game:
	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3
	
	def __init__(self, recommend = True):
		self.initialize_game()
		self.recommend = recommend
		
	def initialize_game(self):
        
		print('Select the size of the board:')
		self.n = int(input('Enter a value from 3-10: '))
		print('Select the winning line-up size: ')
		self.s = int(input('Enter a value from 3-' + str(self.n) +': '))
		print(F'Select the max depth of the adversarial search for player 1: ')
		self.d1 = int(input('Enter a value : '))
		print(F'Select the max depth of the adversarial search for player 2: ')
		self.d2 = int(input('Enter a value : '))
		print(F'Select the play mode: ')
		mode_select = str(input('Enter h-h if both player 1 and 2 are human, h-ai if player 1 is human and player 2 is AI, ai-h if player 1 is AI and player 2 is human and ai-ai if both players are ai : '))
		if mode_select == "h-h":
			self.player_1 = Game.HUMAN
			self.player_2 = Game.HUMAN
		elif mode_select == "h-ai":
			self.player_1 = Game.HUMAN
			self.player_2 = Game.AI
		elif mode_select == "ai-h":
			self.player_1 = Game.AI
			self.player_2 = Game.HUMAN
		elif mode_select == "ai-ai":
			self.player_1 = Game.AI
			self.player_2 = Game.AI
		if self.player_1 == Game.AI or self.player_2 == Game.AI:
			print(F'Select whether minimax or alphabeta will be used: ')
			self.a = str(input('Enter False for minimax and True for alphabeta : '))
			if self.a == "True":
				self.algo = Game.ALPHABETA
			elif self.a == "False":
				self.algo = Game.MINIMAX
			print(F'Select the max allowed time for the program to return a move: ')
			self.t = float(input('Enter an amount of seconds : '))
		self.current_state = []
		for i in range(self.n):
			row = []
			for j in range(self.n):
				row.append('.')
			self.current_state.append(row)
		print(F'Select the number of blocks on the board:')
		self.b = int(input('Enter a value : '))
		if self.b != 0:
			self.draw_board()
		self.b_array = []
		for i in range(self.b):
			x = ord(str(input('Select the x coordinate for block ' + str(i) + '. Select a value between A and ' + str(chr(self.n+64)) + ': ' ))) - 65
			y = (int(input('enter the y coordinate for block ' + str(i) + ' : ' )))
			self.b_array.append(tuple([x,y]))
		
		for i in range(self.b):
			x = self.b_array[i][0]
			y = self.b_array[i][1]
			self.current_state[x][y] = '*'

		#  Player X always plays first

		self.draw_board()
		self.player_turn = 'X'

	def draw_board(self):
		print()
		print("    ", end='')
		for i in range(self.n):
			print(chr(i+65), end='')
		print()
		print('  + ', end='')
		for i in range(self.n):
			print('-', end='')
		print()
		for y in range(0, self.n):
			print(str(y) + ' | ', end='')
			for x in range(0, self.n):
				print(F'{self.current_state[x][y]}', end="")
			print()
		print()
		
	def is_valid(self, px, py):
		if px < 0 or px >= self.n or py < 0 or py >= self.n:
			return False
		elif self.current_state[px][py] != '.' and self.current_state[px][py] != '*':
			return False
		else:
			return True

	def is_end(self):
		# Vertical win
		for i in range(0, 3):
			if (self.current_state[0][i] != '.' and
				self.current_state[0][i] == self.current_state[1][i] and
				self.current_state[1][i] == self.current_state[2][i]):
				return self.current_state[0][i]
		# Horizontal win
		for i in range(0, 3):
			if (self.current_state[i] == ['X', 'X', 'X']):
				return 'X'
			elif (self.current_state[i] == ['O', 'O', 'O']):
				return 'O'
		# Main diagonal win
		if (self.current_state[0][0] != '.' and
			self.current_state[0][0] == self.current_state[1][1] and
			self.current_state[0][0] == self.current_state[2][2]):
			return self.current_state[0][0]
		# Second diagonal win
		if (self.current_state[0][2] != '.' and
			self.current_state[0][2] == self.current_state[1][1] and
			self.current_state[0][2] == self.current_state[2][0]):
			return self.current_state[0][2]
		# Is whole board full?
		for i in range(0, 3):
			for j in range(0, 3):
				# There's an empty field, we continue the game
				if (self.current_state[i][j] == '.'):
					return None
		# It's a tie!
		return '.'

	def check_end(self):
		self.result = self.is_end()
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':
				print('The winner is X!')
			elif self.result == 'O':
				print('The winner is O!')
			elif self.result == '.':
				print("It's a tie!")
			self.initialize_game()
		return self.result

	def input_move(self):
		while True:
			print(F'Player {self.player_turn}, enter your move:')
			px = ord(str(input('enter the x coordinate: '))) - 65
			py = int(input('enter the y coordinate: '))
			if self.is_valid(px, py):
				return (px,py)
			else:
				print('The move is not valid! Try again.')

	def switch_player(self):
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn

	def minimax(self, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		if time.time() >= self.time_start + self.t:
			sys.exit("The AI took too longer than " + str(self.t) + " seconds so it automatically loses")
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, 3):
			for j in range(0, 3):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.minimax(max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.minimax(max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y)

	def alphabeta(self, alpha=-2, beta=2, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		if time.time() >= self.time_start + self.t:
			sys.exit("The AI took too longer than " + str(self.t) + " seconds so it automatically loses")
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, 3):
			for j in range(0, 3):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.alphabeta(alpha, beta, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(alpha, beta, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
					if max: 
						if value >= beta:
							return (value, x, y)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y)
						if value < beta:
							beta = value
		return (value, x, y)

	def e1(self, player, other_player):
		"""
		Simple heuristic function that sums up the difference in the number of pieces 
		between the other player and the current player for each row, column and the 2 main diagonals
		"""
		
		score = 0

		board_range = range(self.n)

		# Computing row scores
		for i in board_range:
			player_score = sum(self.current_state[i][j] == player for j in board_range)
			opponent_score = sum(self.current_state[i][j] == other_player for j in board_range)
			score += opponent_score - player_score

		# Computing column scores
		for j in board_range:
			player_score = sum(self.current_state[i][j] == player for i in board_range)
			opponent_score = sum(self.current_state[i][j] == other_player for i in board_range)
			score += opponent_score - player_score

		# Computing first diagonal score
		player_score = sum(self.current_state[i][i] == player for i in board_range)
		opponent_score = sum(self.current_state[i][i] == other_player for i in board_range)
		score += opponent_score - player_score

		# Computing second diagonal score
		player_score = sum(self.current_state[i][self.n - 1 - i] == player for i in board_range)
		opponent_score = sum(self.current_state[i][self.n - 1 - i] == other_player for i in board_range)
		score += opponent_score - player_score

		return score

	def appraise_count(self,count):
		return count*count if count < self.s else pow(count,3)

	def count_consecutive_items(self,lst,player):
		prev = None
		count = 0
		for item in lst:
			if item != player:
				if prev and count:
					yield count
					prev = None
				count = 0
				continue
			if item != prev and count:
				yield count
				count = 0
			count += 1
			prev = item
		if prev and count:
			yield count

	def consecutive_score(self,lst,player):
		return np.sum([self.appraise_count(c) for c in list(self.count_consecutive_items(lst,player))])

	def e2(self, player, other_player):
		"""
		Stronger heuristic function that sums up the difference in the number of adjacent pieces,
		giving more weight to longest adjacencies.
		"""
		
		score = 0

		board_range = range(self.n)

		a = np.array(self.current_state)

		for i in board_range:
			# Computing row scores
			player_score = self.consecutive_score(a[:,i],player)
			opponent_score = self.consecutive_score(a[:,i],other_player)
			score += opponent_score - player_score

			# Computing column scores
			player_score = self.consecutive_score(a[i,:],player)
			opponent_score = self.consecutive_score(a[i,:],other_player)
			score += opponent_score - player_score

		# Getting diagonals from left to right
		diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
		# Getting other diagonals
		diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))

		# Computing diagonal scores
		for d in diags:
			if len(d) < self.s:
				continue
			player_score = self.consecutive_score(d,player)
			opponent_score = self.consecutive_score(d,other_player)
			score += opponent_score - player_score
		
		return score

	def play(self,algo=None,player_x=None,player_o=None):
		if algo == None:
			algo = self.ALPHABETA
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		while True:
			self.draw_board()
			if self.check_end():
				return
			start = time.time()
			self.time_start = time.time()
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(max=False)
				else:
					(_, x, y) = self.minimax(max=True)
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(max=False)
				else:
					(m, x, y) = self.alphabeta(max=True)
			end = time.time()
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
					if self.recommend:
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Recommended move: x = {x}, y = {y}')
					(x,y) = self.input_move()
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
			self.current_state[x][y] = self.player_turn
			self.switch_player()

def main():
	g = Game(recommend=True)
	g.play(algo=g.algo,player_x=g.player_1,player_o=g.player_2)
	g.play(algo=Game.MINIMAX,player_x=g.player_1,player_o=g.player_2)
	# g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI)
	# g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN)
	print('e1: ')
	print(g.e1('X','O'))
	print('e2: ')
	print(g.e2('X','O'))

if __name__ == "__main__":
	main()

