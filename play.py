from game import State, random_action
from mcts import mcs_action, mcts_action
# from tensorflow.keras.models import load_model
# from pv_mcts import pv_mcts_action
import numpy as np
import pandas as pd
from misc import *

# model = load_model('./model/best.h5')

score_board = np.array([0]*(ROW*COL)).reshape(ROW,COL)

# 반복 횟수
n = 4000

for i in range(n):
    state = State()
    path = [0] * (ROW*COL)
    win_count = 0

    while True:
        if state.is_done():
            break

        if state.is_first_player():
            # action = pv_mcts_action(model, 0.0)(state)
            action = mcts_action(state)
            if action != (ROW*COL):
                path[action] = 1
        else:
            action = mcts_action(state)

        state = state.next(action)    

        # print(state)
        # print()

    if state.is_lose():
        score_board -= np.array(path).reshape(ROW,COL)
    if  state.is_win():
        score_board += np.array(path).reshape(ROW,COL)
        win_count += 1

print(score_board)
print(win_count/n)

df = pd.DataFrame(score_board)
df.to_csv('mcts_4000.csv', index=False)

