# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import sys
import numpy as np
import time


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3

    def __init__(self, recommend=True):
        self.initialize_game()
        self.recommend = recommend

    def initialize_game(self):
        self.move = 0

        # Get inputs from human
        print('Select the size of the board:')
        self.n = int(input('Enter a value from 3-10: '))
        print('Select the winning line-up size: ')
        self.s = int(input('Enter a value from 3-' + str(self.n) + ': '))
        print(F'Select the max depth of the adversarial search for player 1: ')
        d1 = int(input('Enter a value : '))
        self.player_1_strat = tuple([d1, self.e1])
        print(F'Select the max depth of the adversarial search for player 2: ')
        d2 = int(input('Enter a value : '))
        self.player_2_strat = tuple([d2, self.e2])

        print(F'Select the max allowed time for the program to return a move: ')
        self.t = int(input('Enter an amount of seconds : '))
        print(F'Select whether minimax or alphabeta will be used: ')
        self.a = input('Enter False for minimax and True for alphabeta : ')
        if self.a == "True":
            self.algo = Game.ALPHABETA
        elif self.a == "False":
            self.algo = Game.MINIMAX
        print(F'Select the play mode: ')
        mode_select = str(input(
            'Enter h-h if both player 1 and 2 are human, h-ai if player 1 is human and player 2 is AI, ai-h if player 1 is AI and player 2 is human and ai-ai if both players are ai : '))
        if mode_select == "h-h":
            self.player_1 = "HUMAN"
            self.player_2 = "HUMAN"
        elif mode_select == "h-ai":
            self.player_1 = "HUMAN"
            self.player_2 = "AI"
        elif mode_select == "ai-h":
            self.player_1 = "AI"
            self.player_2 = "HUMAN"
        elif mode_select == "ai-ai":
            self.player_1 = "AI"
            self.player_2 = "AI"
        print(F'Select the number of blocks on the board:')
        # Get Coordinate and Number of blocks for board
        self.b = int(input('Enter a value : '))
        self.b_array = []
        for i in range(self.b):
            x = ord(
                str(input('enter the x coordinate for block ' + str(i) + ' : '))) - 65
            y = (int(input('enter the y coordinate for block ' + str(i) + ' : ')))
            self.b_array.append(tuple([x, y]))
        self.current_state = []
        # Build game board with blocks
        for i in range(self.n):
            row = []
            for j in range(self.n):
                row.append('.')
            self.current_state.append(row)
        for i in range(self.b):
            x = self.b_array[i][0]
            y = self.b_array[i][1]
            self.current_state[x][y] = '*'
        # X always starts
        self.current_player = self.player_1
        self.player_turn = 'X'
        self.other_player_turn = 'O'
        self.stats = {
            "total_heuristic_count": 0,
            "ard_list": [],
            "depth_list": [],
            "total_depth_list": [],
            "eval_time_list": []
        }
        # Display Initial Game info
        # sys.stdout = open("output.txt", "w")
        print(F'\nn={self.n} b={self.b} s={self.s} t={self.t}')
        print(F'blocs={self.b_array}')
        print(
            F'\nPlayer 1: {self.player_1} d={self.player_1_strat[0]} a={self.current_player} e1(regular)')
        print(
            F'Player 2: {self.player_2} d={self.player_2_strat[0]} a={self.current_player} e2(defensive)')

        # Display Board
        self.draw_board()

    def draw_end_game_stats(self):
        print(
            F'\n6(b)i   Average evaluation time: {round(np.average(np.array(self.stats["eval_time_list"])),2)}s')
        print(
            F'6(b)ii  Total heuristic evaluations: {self.stats["total_heuristic_count"]}')
        print("6(b)iii Total evaluations by depth: {", end='')
        total_depth_list = self.group_by_sum(
            np.array(self.stats["total_depth_list"]))
        for info in total_depth_list:
            print(str(round(info[0])) +
                  ": " + str(round(info[1]))+", ", end="")
        print("}")
        print(
            F'6(b)iv  Average evaluation depth: {round(np.average(np.array(self.stats["total_depth_list"])[:,0]),2)}')

        # self.calculate_ARD(np.array(self.stats["total_depth_list"])[:, 0])

        print(
            F'6(b)v   Average recursion depth evaluations: {round(np.average(np.array(self.stats["ard_list"])),2)}')
        print(
            F'6(b)vi  Total moves: {self.move}')

    def draw_turn_stats(self, x, y):
        print(
            F'Player {self.player_turn} under {self.current_player} control plays: {chr(x+65)}{y}')
        print(
            F'\ni   Evaluation time: {self.stats["eval_time_list"][self.move - 1]}s')

        heuristic_turn_count = np.sum(np.array(self.stats["depth_list"])[:, 1])
        self.stats["total_heuristic_count"] += heuristic_turn_count
        print(
            F'ii  Heuristic evaluations: {heuristic_turn_count}')
        print("iii Evaluations by depth: {", end='')
        depth_list = self.group_by_sum(np.array(self.stats["depth_list"]))

        for info in depth_list:
            self.stats["total_depth_list"].append(tuple([info[0], info[1]]))
            print(str(round(info[0])) +
                  ": " + str(round(info[1]))+", ", end="")
        print("}")
        print(
            F'iv  Average evaluation depth: {round(np.average(np.array(self.stats["depth_list"])[:,0]),2)}')
        print(
            F'v   Average recursion depth evaluations: {self.stats["ard_list"][self.move - 1]}')

    def group_by_sum(self, list):
        u, idx = np.unique(list[:, 0], return_inverse=True)
        s = np.bincount(idx, weights=list[:, 1])
        return np.c_[u, s]

    def calculate_ARD(self, list):
        print()

    def draw_board(self):
        print("\n    ", end='')
        for i in range(self.n):
            print(chr(i+65), end='')
        if self.move != 0:
            print(F'    (move #{self.move})', end="")
        print('\n  + ', end='')
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
        a = np.array(self.current_state)

        for i in range(self.n):
            for c in list(self.count_consecutive_items(a[i, :], self.player_turn)):
                if c == self.s:
                    return self.player_turn

        for i in range(self.n):
            for c in list(self.count_consecutive_items(a[:, i], self.player_turn)):
                if c == self.s:
                    return self.player_turn

        # Getting diagonals from left to right
        diags = [a[::-1, :].diagonal(i)
                 for i in range(-a.shape[0]+1, a.shape[1])]
        # Getting other diagonals
        diags.extend(a.diagonal(i)
                     for i in range(a.shape[1]-1, -a.shape[0], -1))

        # Diagonal win
        for d in diags:
            if len(d) < self.s:
                continue
            for c in list(self.count_consecutive_items(d, self.player_turn)):
                if c == self.s:
                    return self.player_turn

        # Is whole board full?
        for i in range(self.n):
            for j in range(self.n):
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
            self.current_player = self.player_2
            self.player_turn = 'O'
            self.other_player_turn = 'X'
        elif self.player_turn == 'O':
            self.current_player = self.player_1
            self.other_player_turn = 'O'
            self.player_turn = 'X'
        return self.player_turn

    def minimax(self, depth=0, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = sys.maxsize
        if max:
            value = -sys.maxsize - 1
        x = None
        y = None
        result = self.is_end()

        strat = self.player_1_strat if self.player_turn == 'X' else self.player_2_strat

        if result == 'X':
            self.stats["depth_list"].append(
                tuple([depth, 1]))
            return (-sys.maxsize - 1, x, y, depth)
        elif result == 'O':
            self.stats["depth_list"].append(
                tuple([depth, 1]))
            return (sys.maxsize, x, y, depth)
        elif result == '.':
            self.stats["depth_list"].append(
                tuple([depth, 1]))
            return (0, x, y, depth)
        elif strat[0] == depth:
            self.stats["depth_list"].append(
                tuple([depth, 1]))
            score = strat[1](self.player_turn, self.other_player_turn)
            return (score, x, y, depth)

        ard_list = []

        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _, ard) = self.minimax(depth + 1, max=False)

                        ard_list.append(ard)

                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _, ard) = self.minimax(depth + 1, max=True)

                        ard_list.append(ard)

                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
        return (value, x, y, np.average(np.array(ard_list)))

    def alphabeta(self, depth=0, alpha=-sys.maxsize-1, beta=sys.maxsize, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -infinite - win for 'X'
        # 0  - a tie
        # infinite  - loss for 'X'

        value = sys.maxsize
        if max:
            value = -sys.maxsize-1
        x = None
        y = None
        result = self.is_end()

        strat = self.player_1_strat if self.player_turn == 'X' else self.player_2_strat

        if result == 'X':
            self.stats["depth_list"].append(
                tuple([depth, 1]))
            return (-sys.maxsize-1, x, y, depth)
        elif result == 'O':
            self.stats["depth_list"].append(
                tuple([depth, 1]))
            return (sys.maxsize, x, y, depth)
        elif result == '.':
            self.stats["depth_list"].append(
                tuple([depth, 1]))
            return (0, x, y, depth)
        elif strat[0] == depth:
            self.stats["depth_list"].append(
                tuple([depth, 1]))
            score = strat[1](self.player_turn, self.other_player_turn)
            return (score, x, y, depth)

        ard_list = []

        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _, ard) = self.alphabeta(depth + 1,
                                                        alpha, beta, max=False)
                        ard_list.append(ard)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _, ard) = self.alphabeta(depth + 1,
                                                        alpha, beta, max=True)
                        ard_list.append(ard)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
                    if max:
                        if value >= beta:
                            return (value, x, y, depth)
                        if value > alpha:
                            alpha = value
                    else:
                        if value <= alpha:
                            return (value, x, y, depth)
                        if value < beta:
                            beta = value
        return (value, x, y, np.average(np.array(ard_list)))

    def e1(self, player, other_player):
        """
        Simple heuristic function that sums up the difference in the number of pieces 
        between the other player and the current player for each row, column and the 2 main diagonals
        """

        score = 0

        board_range = range(self.n)

        # Computing row scores
        for i in board_range:
            player_score = sum(
                self.current_state[i][j] == player for j in board_range)
            opponent_score = sum(
                self.current_state[i][j] == other_player for j in board_range)
            score += opponent_score - player_score

        # Computing column scores
        for j in board_range:
            player_score = sum(
                self.current_state[i][j] == player for i in board_range)
            opponent_score = sum(
                self.current_state[i][j] == other_player for i in board_range)
            score += opponent_score - player_score

        # Computing first diagonal score
        player_score = sum(
            self.current_state[i][i] == player for i in board_range)
        opponent_score = sum(
            self.current_state[i][i] == other_player for i in board_range)
        score += opponent_score - player_score

        # Computing second diagonal score
        player_score = sum(
            self.current_state[i][self.n - 1 - i] == player for i in board_range)
        opponent_score = sum(
            self.current_state[i][self.n - 1 - i] == other_player for i in board_range)
        score += opponent_score - player_score

        return score

    def appraise_count(self, count):
        return count*count if count < self.s else pow(count, 3)

    def count_consecutive_items(self, lst, player):
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

    def consecutive_score(self, lst, player):
        return np.sum([self.appraise_count(c) for c in list(self.count_consecutive_items(lst, player))])

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
            player_score = self.consecutive_score(a[:, i], player)
            opponent_score = self.consecutive_score(a[:, i], other_player)
            score += opponent_score - player_score

            # Computing column scores
            player_score = self.consecutive_score(a[i, :], player)
            opponent_score = self.consecutive_score(a[i, :], other_player)
            score += opponent_score - player_score

        # Getting diagonals from left to right
        diags = [a[::-1, :].diagonal(i)
                 for i in range(-a.shape[0]+1, a.shape[1])]
        # Getting other diagonals
        diags.extend(a.diagonal(i)
                     for i in range(a.shape[1]-1, -a.shape[0], -1))

        # Computing diagonal scores
        for d in diags:
            if len(d) < self.s:
                continue
            player_score = self.consecutive_score(d, player)
            opponent_score = self.consecutive_score(d, other_player)
            score += opponent_score - player_score

        return score

    def play(self, algo=None, player_x=None, player_o=None):
        if algo == None:
            algo = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN
        while True:
            self.stats["depth_list"] = []
            start = time.time()
            if algo == self.MINIMAX:
                if self.player_turn == 'X':
                    (_, x, y, ard) = self.minimax(max=False)
                else:
                    (_, x, y, ard) = self.minimax(max=True)
            else:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y, ard) = self.alphabeta(max=False)
                else:
                    (m, x, y, ard) = self.alphabeta(max=True)
            self.stats["ard_list"].append(ard)
            end = time.time()
            self.stats["eval_time_list"].append(round(end - start, 2))
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Recommended move: x = {x}, y = {y}')
                (x, y) = self.input_move()
            self.move += 1
            self.draw_turn_stats(x, y)
            self.current_state[x][y] = self.player_turn
            self.draw_board()
            if self.check_end():
                self.draw_end_game_stats()
                return
            self.switch_player()


def main():
    g = Game(recommend=True)
    g.play(algo=g.algo, player_x=g.player_1, player_o=g.player_2)
    # sys.stdout.close()
    # g.play(algo=Game.MINIMAX,player_x=g.player_1,player_o=g.player_2)


if __name__ == "__main__":
    main()
