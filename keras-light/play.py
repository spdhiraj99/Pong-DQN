from agent import Agent
from pong import Game
# play a round
import os
import sys
import argparse
import re
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument('checkpoint',nargs='?')
args = parser.parse_args()

game = Game()
agent = Agent(game)
if args.checkpoint:
    agent.load('game_weights.h5')

while 1:
    game.reset()
    game.render() # rendering won't work inside a notebook, only from terminal. uncomment
    reward = 0
    while reward == 0 or reward == 1:
        action = agent.choose_action()
        game.move(action)
        reward = game.update()
        game.render()
        sleep(0.1)
    print('winner!' if reward == 1 else 'loser!')