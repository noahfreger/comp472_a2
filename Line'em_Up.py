# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time

class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3

    def __init__(self, recommend=True):
        self.initialize_game()

        self.recommend = recommend
        self.n = 5
        self.s = 3

    def initialize_game(self):
        self.current_state = [['.', '.', '.'],
                              ['.', '.', '.'],
                              ['.', '.', '.']]
        # Player X always plays first
		# print() TODO: print initial game params

        self.player_turn = 'X'

    def draw_turn_info(self, x, y, time, eval_depth, avg_eval_depth, avg_recursion_depth):
        print(F'Evaluation time: {round(time, 7)}s')
        print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')

    def draw_board(self):
        print()
        for y in range(0, self.n):
            for x in range(0, self.n):
                print(F'{self.current_state[x][y]}', end="")
            print()
        print()

    def test1(self):
        self.current_state = [['X', '.', '.','.','.'],
                              ['.', 'X', '.','.','.'],
                              ['.', '.', '.','.','.'],
                              ['.', '.', '.','.','.'],
                              ['.', '.', '.','.','.']]

        self.s = 3
        self.draw_board()                      
        self.check_end()

    def is_valid(self, px, py):
        if px < 0 or px > 2 or py < 0 or py > 2:
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True

    def is_end(self):
        # Vertical win
        for i in range(0, self.n):
            count = 1
            for j in range(0, self.n - 1):
                item = self.current_state[i][j]
                nextItem = self.current_state[i][j+1]
                if(item == '.' or item == '*' or item != nextItem):
                    count = 1
                else:
                    count += 1
                if(count == self.s ):
                    return self.current_state[i][j - count + 2]
        # Horizontal win
        for j in range(0, self.n):
            count = 1
            for i in range(0, self.n - 1):
                item = self.current_state[i][j]
                nextItem = self.current_state[i+1][j]
                if(item == '.' or item == '*' or item != nextItem):
                    count = 1
                else:
                    count += 1
                if(count == self.s ):
                    return self.current_state[i - count + 2][j]

        # Main diagonal win (from left to right)
        # we start at n-3 and end at -n+2 because minimum possible win condition is 3 in a row
        for i in range(self.n - 3, - self.n + 2, -1):
            count = 1
            # Different end condition for left of main diagnol
            end = self.n - i - 1 if i > 0 else self.n - 2 - (abs(i) - 1)
            for j in range(0, end):
                if(i>=0):
                    item = self.current_state[i + j][j]
                    nextItem = self.current_state[i + j + 1][j + 1]
                    nextX = i + j + 1
                    nextY = j + 1
                else:
                    item = self.current_state[j][abs(i) + j]
                    nextItem = self.current_state[j + 1][abs(i) + j + 1]
                    nextX = j + 1
                    nextY = abs(i) + j + 1

                if(item == '.' or item == '*' or item != nextItem):
                    count = 1
                    continue
                else:
                    count += 1
                if(count == self.s):
                    return self.current_state[nextX][nextY]
                    
        # Second diagonal win (from right to left)
        for i in range(self.n - 3, self.n + 2):
            count = 1
            # Different end condition for left of main diagnol
            end = i if i <= self.n - 1 else self.n - 2 - (i - self.n)
            for j in range(0, end):
                if(i <= self.n - 1):
                    item = self.current_state[i - j][j]
                    nextItem = self.current_state[i - j - 1][j + 1]
                    nextX = i - j - 1
                    nextY = j + 1
                else:
                    item = self.current_state[ self.n - j - 1][j + i - self.n + 1]
                    nextItem = self.current_state[self.n - j -  2][j + i - self.n + 2]
                    nextX = self.n - j -  2
                    nextY = j + i - self.n + 2

                if(item == '.' or item == '*' or item != nextItem):
                    count = 1
                    continue
                else:
                    count += 1
                # Checks the win condition and returns the first instanc
                if(count == self.s):
                    return self.current_state[nextX][nextY]

        # Is whole board full?
        for i in range(0, self.n):
            for j in range(0, self.n):
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
                return (px, py)
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
        count = 0
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = self.is_end()
        if result == 'X':
            return (-1, x, y,count)
        elif result == 'O':
            return (1, x, y,count)
        elif result == '.':
            return (0, x, y,count)
        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _, _) = self.minimax(max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _, _) = self.minimax(max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
                    count + 1
        return (value, x, y, count)

    def alphabeta(self, alpha=-2, beta=2, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        count = 0
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
                    count + 1        
        return (value, x, y)

    def play(self, algo=None, player_x=None, player_o=None):
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
                    (_, x, y, _) = self.minimax(max=False)
                else:
                    (_, x, y, _) = self.minimax(max=True)
            else:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(max=False)
                else:
                    (m, x, y) = self.alphabeta(max=True)
            end = time.time()
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Recommended move: x = {x}, y = {y}')
                (x, y) = self.input_move()
            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
               self.draw_turn_info(self, x, y, end - start, 1, 1)
            self.current_state[x][y] = self.player_turn
            self.switch_player()


def main():
    g = Game(recommend=True)
    g.test1()
    # g.play(algo=Game.ALPHABETA, player_x=Game.AI, player_o=Game.AI)
    #g.play(algo=Game.ALPHABETA, player_x=Game.AI, player_o=Game.HUMAN)


if __name__ == "__main__":
    main()
