from Line_em_up import Game
import numpy as np

def group_by_sum(list):
    u, idx = np.unique(list[:, 0], return_inverse=True)
    s = np.bincount(idx, weights=list[:, 1])
    return np.c_[u, s]

f = open("scoreboard.txt", "a")

e1_wins=0
e2_wins=0

# Set number of iterations (#games = 2*nb_iterations)
nb_iterations=5

# Set game parameters here
blocs=[(0,0),(0,3),(3,0),(3,3)]
n=5
b=4
s=4
t=5
d1=6
d2=6

a='True'

f.write('-----------------------------------------------\n\n')

f.write(F'n={n} b={b} s={s} t={t}\n\n')

f.write(F'Player 1: d={d1} a={a} e1(regular)\n')
f.write(F'Player 2: d={d2} a={a} e2(adjacent)\n')

eval_times = []
total_heuristic_evaluations = 0
total_depth_list = []
average_recursion_depth_list = []
average_evaluation_depth_list = []
moves_list = []

for i in range(nb_iterations):
    g1 = Game(user_input=False, gameTrace=False, n=n, b=b, s=s, t=t, d1=d1, d2=d2, a=a, strat1='e1')
    g1.play(algo=g1.algo, player_x=g1.player_1, player_o=g1.player_2)
    eval_times.append(g1.stats["average_eval_time"])
    total_heuristic_evaluations += g1.stats["total_heuristic_count"]
    total_depth_list = total_depth_list + g1.stats["total_depth_list"]
    average_recursion_depth_list.append(g1.stats["average_recursion_depth"])
    average_evaluation_depth_list.append(g1.stats["average_evaluation_depth"])
    moves_list.append(g1.move)

    g2 = Game(user_input=False, gameTrace=True, n=n, b=b, s=s, t=t, d1=d1, d2=d2, a=a, strat1='e2')
    g2.play(algo=g2.algo, player_x=g2.player_1, player_o=g2.player_2)
    eval_times.append(g2.stats["average_eval_time"])
    total_heuristic_evaluations += g2.stats["total_heuristic_count"]
    total_depth_list = total_depth_list + g2.stats["total_depth_list"]
    average_recursion_depth_list.append(g2.stats["average_recursion_depth"])
    average_evaluation_depth_list.append(g2.stats["average_evaluation_depth"])
    moves_list.append(g2.move)

    if g1.winner == 'X':
        e1_wins += 1
    elif g1.winner == 'O':
        e2_wins += 1

    if g2.winner == 'X':
        e2_wins += 1
    elif g2.winner == 'O':
         e1_wins += 1

f.write(F'\n{nb_iterations*2} games\n')

f.write(F'\nTotal wins for heuristic e1: {e1_wins} ({round(100*e1_wins/(nb_iterations*2),1)}%)\n')
f.write(F'Total wins for heuristic e2: {e2_wins} ({round(100*e2_wins/(nb_iterations*2),1)}%)\n')

average_eval_time = round(np.average(np.array(eval_times)),2)
f.write(F'\ni   Average evaluation time: {average_eval_time}s\n')

f.write(F'ii  Total heuristic evaluations: {total_heuristic_evaluations}')

total_depth_array = group_by_sum(np.array(total_depth_list))
f.write("\niii Total evaluations by depth: {")
for index,info in enumerate(total_depth_array):
    f.write(str(round(info[0])) +": " + str(round(info[1])))
    if index < len(total_depth_array) -1:
        f.write(', ')
f.write("}")

f.write(F'\niv  Average evaluation depth: {round(np.average(np.array(average_evaluation_depth_list)),2)}')

f.write(F'\nv   Average recursion depth: {round(np.average(np.array(average_recursion_depth_list)),2)}')

f.write(F'\nvi  Average moves per game: {round(np.average(np.array(moves_list)),2)}\n\n')

f.close()
