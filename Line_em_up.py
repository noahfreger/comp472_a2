import sys
import numpy as np
import time
from random import randint
from threading import Event, Timer
import copy


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3

    def __init__(self, user_input=True, gameTrace=False, n=0, b=0, s=0, t=0, d1=0, d2=0, a='True', blocs=None, strat1='e1'):
        self.gameTrace = gameTrace
        self.user_input = user_input
        self.initialize_game(n, b, s, t, d1, d2, a, blocs, strat1)
        self.stop_timer_event = Event()

    def initialize_game(self, n, b, s, t, d1, d2, a, blocs, strat1):
        # Initialize variables
        self.move = 0
        self.ai_move = 0
        self.current_depth = 0
        # X always starts
        self.player_turn = 'X'
        self.other_player_turn = 'O'
        self.stats = {
            "total_heuristic_count": 0,
            "ard_list": [],
            "depth_list": [],
            "total_depth_list": [],
            "eval_time_list": [],
            "average_eval_time": 0,
            "average_recursion_depth": 0
        }
        if self.user_input:
            self.display_inputs()
        else:
            self.init_from_params(n, b, s, t, d1, d2, a, blocs, strat1)

        if self.a == "True":
            self.algo = Game.ALPHABETA
        elif self.a == "False":
            self.algo = Game.MINIMAX

        self.current_player = self.player_1

        if self.gameTrace:
            sys.stdout = open(
                F"gameTrace-{self.n}{self.b}{self.s}{self.t}.txt", "w")

        # Display Initial Game info
        print(F'\nn={self.n} b={self.b} s={self.s} t={self.t}')
        print(F'blocs={self.b_array}')
        player1_heuristic_string = 'e1(regular)' if strat1 == 'e1' else 'e2(adjacent)'
        player2_heuristic_string = 'e2(adjacent)' if strat1 == 'e1' else 'e1(regular)'

        print(
            F'\nPlayer 1: {self.player_1} d={self.player_1_strat[0]} a={self.a} {player1_heuristic_string}')
        print(
            F'Player 2: {self.player_2} d={self.player_2_strat[0]} a={self.a} {player2_heuristic_string}')

        # Display Board
        self.draw_board()

    def init_from_params(self, n, b, s, t, d1, d2, a, blocs, strat1):
        self.n = n
        self.b = b
        self.s = s
        self.t = t
        self.a = a

        self.player_1 = "AI"
        self.player_2 = "AI"

        if (strat1 == 'e1'):
            self.player_1_strat = tuple([d1, self.e1])
            self.player_2_strat = tuple([d2, self.e2])
        else:
            self.player_1_strat = tuple([d2, self.e2])
            self.player_2_strat = tuple([d1, self.e1])

        self.current_state = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                row.append('.')
            self.current_state.append(row)

        self.b_array = []

        if blocs != None:
            for bloc in blocs:
                self.b_array.append(tuple([bloc[0], bloc[1]]))
        else:
            valid_positions = self.find_all_valid_positions()
            for _ in range(self.b):
                bloc_position = self.find_random_valid_position(
                    valid_positions)
                self.b_array.append(
                    tuple([bloc_position[0], bloc_position[1]]))
                del valid_positions[bloc_position[2]]

        for bloc in self.b_array:
            self.current_state[bloc[0]][bloc[1]] = '*'

    def find_all_valid_positions(self):
        valid_spots = []
        for i in range(self.n):
            for j in range(self.n):
                if self.current_state[i][j] == '.':
                    valid_spots.append(([i, j]))

        return valid_spots

    def find_random_valid_position(self, lst=None):
        if lst != None:
            valid_spots = lst
        else:
            valid_spots = []
            for i in range(self.n):
                for j in range(self.n):
                    if self.current_state[i][j] == '.':
                        valid_spots.append((i, j))

        random_int = randint(0, len(valid_spots)-1)
        random_position = valid_spots[random_int]
        return (random_position[0], random_position[1], random_int)

    def draw_end_game_stats(self):
        self.stats["average_eval_time"] = round(
            np.average(np.array(self.stats["eval_time_list"])), 2)
        print(
            F'\n6(b)i   Average evaluation time: {self.stats["average_eval_time"]}s')
        print(
            F'6(b)ii  Total heuristic evaluations: {self.stats["total_heuristic_count"]}')
        print("6(b)iii Total evaluations by depth: {", end='')
        total_depth_list = self.group_by_sum(
            np.array(self.stats["total_depth_list"]))
        for index, info in enumerate(total_depth_list):
            print(str(round(info[0])) + ": " + str(round(info[1])) +
                  (", " if index < len(total_depth_list) - 1 else ""), end="")
        print("}")

        self.stats["average_evaluation_depth"] = round(np.average(
            total_depth_list[:, 0], weights=total_depth_list[:, 1]), 2)
        print(
            F'6(b)iv  Average evaluation depth: {self.stats["average_evaluation_depth"]}')

        self.stats["average_recursion_depth"] = round(
            np.average(np.array(self.stats["ard_list"])), 2)
        print(
            F'6(b)v   Average recursion depth evaluations: {self.stats["average_recursion_depth"]}')
        print(
            F'6(b)vi  Total moves: {self.move}')

    def draw_turn_stats(self, x, y):
        print(
            F'Player {self.player_turn} under {self.current_player} control plays: {chr(x+65)}{y}')
        print(
            F'\ni   Evaluation time: {self.stats["eval_time_list"][self.ai_move - 1]}s')

        heuristic_turn_count = np.sum(np.array(self.stats["depth_list"])[:, 1])
        self.stats["total_heuristic_count"] += heuristic_turn_count
        print(
            F'ii  Heuristic evaluations: {heuristic_turn_count}')
        print("iii Evaluations by depth: {", end='')
        depth_list = self.group_by_sum(np.array(self.stats["depth_list"]))

        for index, info in enumerate(depth_list):
            self.stats["total_depth_list"].append(tuple([info[0], info[1]]))
            print(str(round(info[0])) + ": " + str(round(info[1])) +
                  (", " if index < len(depth_list) - 1 else ""), end="")

        print("}")
        print(
            F'iv  Average evaluation depth: {round(np.average(np.array(self.stats["depth_list"])[:,0]),2)}')
        print(
            F'v   Average recursion depth evaluations: {round(self.stats["ard_list"][self.ai_move-1],2)}')

    def group_by_sum(self, list):
        u, idx = np.unique(list[:, 0], return_inverse=True)
        s = np.bincount(idx, weights=list[:, 1])
        return np.c_[u, s]

    def no_time_left(self):
        self.stop_timer_event.set()

    def display_inputs(self):
        print('Step 1) Select the size of the board.')
        self.n = int(input(' \tEnter a value from (3-10): '))
        print('Step 2) Select the winning line-up size.')
        self.s = int(input(' \tEnter a value from (3-' + str(self.n) + '): '))
        print(F'Step 3) Select the max depth of the adversarial search for player 1.')
        d1 = int(input(' \tEnter a value : '))
        self.player_1_strat = tuple([d1, self.e1])
        print(F'Step 4) Select the max depth of the adversarial search for player 2.')
        d2 = int(input(' \tEnter a value : '))
        self.player_2_strat = tuple([d2, self.e2])
        print(F'Step 5) Select the play mode.')
        mode_select = str(input(
            ' \tEnter (h-h) if both player 1 and 2 are human, \n \tenter (h-ai) if player 1 is human and player 2 is AI, \n \tenter (ai-h) if player 1 is AI and player 2 is human and \n \tenter (ai-ai) if both players are ai : '))
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
        print(F'Step 6) Select whether minimax or alphabeta will be used.')
        self.a = str(
            input(' \tEnter (False) for minimax and (True) for alphabeta : '))
        print(F'Step 7) Select the max allowed time for the program to return a move.')
        self.t = int(input(' \tEnter an amount of seconds : '))
        self.current_state = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                row.append('.')
            self.current_state.append(row)
        print(F'Step 8) Select the number of blocks on the board.')
        self.b = int(input(' \tEnter a value : '))
        if self.b != 0:
            self.draw_board()
        self.b_array = []
        for i in range(self.b):
            x = ord(str(input('Select the x coordinate for block ' + str(i) +
                    '. Select a value between A and ' + str(chr(self.n+64)) + ': '))) - 65
            y = (int(input('enter the y coordinate for block ' + str(i) + ' : ')))
            self.b_array.append(tuple([x, y]))

        for i in range(self.b):
            x = self.b_array[i][0]
            y = self.b_array[i][1]
            self.current_state[x][y] = '*'

        #  Player X always plays first

        self.draw_board()
        self.player_turn = 'X'

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
                self.winner = 'X'
                print('The winner is X!')
            elif self.result == 'O':
                self.winner = 'O'
                print('The winner is O!')
            elif self.result == '.':
                self.winner = '.'
                print("It's a tie!")
        return self.result

    def input_move(self):
        while True:
            print(F'Player {self.player_turn}, enter your move:')
            px = ord(str(input('enter the x coordinate: '))) - 65
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
        # -maxInt - win for 'X'
        # 0  - a tie
        # maxInt  - loss for 'X'

        if self.stop_timer_event.is_set():
            raise Exception(depth)

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
            return ((-sys.maxsize-1)/2, x, y, depth)
        elif result == 'O':
            self.stats["depth_list"].append(
                tuple([depth, 1]))
            return (sys.maxsize/2, x, y, depth)
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
        # -maxInt - win for 'X'
        # 0  - a tie
        # maxInt  - loss for 'X'

        if self.stop_timer_event.is_set():
            raise Exception(depth)

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
            return ((-sys.maxsize-1)/2, x, y, depth)
        elif result == 'O':
            self.stats["depth_list"].append(
                tuple([depth, 1]))
            return (sys.maxsize/2, x, y, depth)
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
                            return (value, x, y, np.average(np.array(ard_list)))
                        if value > alpha:
                            alpha = value
                    else:
                        if value <= alpha:
                            return (value, x, y, np.average(np.array(ard_list)))
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
            player_x = "HUMAN"
        if player_o == None:
            player_o = "HUMAN"
        while True:
            self.move += 1
            if (self.player_turn == 'X' and player_x == "HUMAN") or (self.player_turn == 'O' and player_o == "HUMAN"):
                (x, y) = self.input_move()
            else:
                self.ai_move += 1
                # make deep copy of board
                self.save_board = copy.deepcopy(self.current_state)
                self.timer = Timer(self.t - 0.03, self.no_time_left)
                self.timer.start()
                self.stats["depth_list"] = []
                start = time.time()
                try:
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
                    end = time.time()
                except Exception as e:
                    (x, y, _) = self.find_random_valid_position()
                    end = time.time()
                    print(F"*** Out of extra time at depth {str(e)} ***")
                    ard = 0
                    # make deep copy of board
                    self.current_state = copy.deepcopy(self.save_board)

                self.stats["ard_list"].append(ard)

                self.stats["eval_time_list"].append(round(end - start, 7))
                self.draw_turn_stats(x, y)
                self.timer.cancel()
                self.stop_timer_event.clear()

            self.current_state[x][y] = self.player_turn
            self.draw_board()
            if self.check_end():
                self.draw_end_game_stats()
                if self.gameTrace:
                    sys.stdout.close()
                return
            self.switch_player()


def main():
    g = Game(user_input=False, gameTrace=True, n=4, b=4, s=3, t=5, d1=6, d2=6, a='False', strat1='e1', blocs=[(0,0),(0,3),(3,0),(3,3)])
    g.play(algo=g.algo, player_x=g.player_1, player_o=g.player_2)


if __name__ == "__main__":
    main()
