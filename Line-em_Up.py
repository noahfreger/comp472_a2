# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time

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
		print(F'Select the max allowed time for the program to return a move: ')
		self.t = int(input('Enter an amount of seconds : '))
		print(F'Select whether minimax or alphabeta will be used: ')
		self.a = bool(input('Enter False for minimax and True for alphabeta : '))
		if self.a == True:
			self.algo = Game.ALPHABETA
		elif self.a == False:
			self.algo = Game.MINIMAX
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
		print(F'Select the number of blocks on the board:')
		self.b = int(input('Enter a value : '))
		self.b_array = []
		for i in range(self.b):
			x = ord(str(input('enter the x coordinate for block ' + str(i) + ' : ' ))) - 97
			y = (int(input('enter the y coordinate for block ' + str(i) + ' : ' )))
			self.b_array.append(tuple([x,y]))
		self.current_state = []
		for i in range(self.n):
			row = []
			for j in range(self.n):
				row.append('.')
			self.current_state.append(row)
		
		for i in range(self.b):
			x = self.b_array[i][0]
			y = self.b_array[i][1]
			self.current_state[x][y] = '*'

		# Player X always plays first

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
		if px < 0 or px > self.n or py < 0 or py > self.n:
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
			px = int(input('enter the x coordinate: '))
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
	# g.play(algo=g.algo,player_x=g.player_1,player_o=g.player_2)
	# g.play(algo=Game.MINIMAX,player_x=g.player_1,player_o=g.player_2)

if __name__ == "__main__":
	main()

