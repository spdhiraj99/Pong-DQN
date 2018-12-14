from pong import Game
from agent import Agent
import os
import sys
import numpy as np
from collections import deque
from time import sleep
game = Game()
agent = Agent(game)

print('training...')
epochs = 6500
batch_size = 256
fname = 'game_weights.h5'

# keep track of past record_len results
record_len = 100
record = deque([], record_len)

for i in range(epochs):
    game.reset()
    reward = 0
    loss = 0
    # rewards only given at end of game
    while reward == 0:
        prev_state = game.state
        action = agent.choose_action()
        game.move(action)
        reward = game.update()
        new_state = game.state
        
        # debug, "this should never happen"
        assert not np.array_equal(new_state, prev_state)

        agent.remember(prev_state, action, new_state, reward)
        loss += agent.replay(batch_size)

    if i % 100 == 0:
        sys.stdout.flush()
        sys.stdout.write('epoch: {:04d}/{} | loss: {:.3f} | win rate: {:.3f}\r'.format(i+1, epochs, loss, sum(record)/len(record) if record else 0))    
    record.append(reward if reward == 1 else 0)

agent.save(fname)