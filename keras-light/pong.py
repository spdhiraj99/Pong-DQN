import numpy as np
from blessings import Terminal

class Game():
    def __init__(self, shape=(10,40)):
        self.shape = shape
        self.height, self.width = shape
        self.last_col = self.width
        self.first_col = -2
        self.first_row = -1
        self.last_row = self.height
        self.paddle_padding = 1
        self.xspeed = 2
        self.yspeed = 1
        self.n_actions = 3 # left, stay, right
        self.term = Terminal()
        self.reset()

    def reset(self):
        # reset grid
        self.grid = np.zeros(self.shape)

        # can only move left or right (or stay)
        # so position is only its horizontal position (col)
        self.pos = np.random.randint(self.paddle_padding, self.height - 1 - self.paddle_padding)
        self.set_paddle(1)

        #y direc
        n = np.random.randint(1,2)
        if n == 0:
            self.yspeed = 1
        if n == 1:
            self.yspeed = -1
        self.target = (5 , 20)
        self.set_position(self.target, 1)

    def move(self, action):
        # clear previous paddle position
        self.set_paddle(0)

        # action is either -1, 0, 1,
        # but comes in as 0, 1, 2, so subtract 1
        action -= 1
        self.pos = min(max(self.pos + action, self.paddle_padding), self.height - 1 - self.paddle_padding)

        # set new paddle position
        self.set_paddle(1)

    def set_paddle(self, val):
        for i in range(1 + self.paddle_padding*2):
            pos = self.pos - self.paddle_padding + i
            self.set_position((pos,0), val)
    def paddle_pt(self):
        return [self.pos, self.pos+2]
    @property
    def state(self):
        return self.grid.reshape((1,-1)).copy()

    def set_position(self, pos, val):
        r, c = pos
        self.grid[r,c] = val
    #returns reward
    def update(self):
        #erase previous location
        r, c = self.target
        self.set_position(self.target, 0)
        [paddle_start, paddle_end]= self.paddle_pt()
        # collision
        #right side
        if c + self.xspeed >= self.last_col:
            self.xspeed = -self.xspeed
        #left side
        if c + self.xspeed <= self.first_col:
            if r + self.yspeed >= paddle_start and r + self.yspeed <= paddle_end:
                self.xspeed = -self.xspeed
                return 1
            return -1                
        #top side
        if r + self.yspeed <= self.first_row:
            self.yspeed = -self.yspeed
        #bottom
        if r + self.yspeed >= self.last_row:
            self.yspeed = -self.yspeed
        #set new coordinates    
        self.target = (r + self.yspeed , c + self.xspeed)
        self.set_position(self.target, 1)

        return 0

    def render(self):
        print(self.term.clear())
        for r, row in enumerate(self.grid):
            for c, on in enumerate(row):
                if on:
                    color = 255
                else:
                    color = 20

                print(self.term.move(r, c) + self.term.on_color(color) + ' ' + self.term.normal)

        # move cursor to end
        print(self.term.move(self.height, 0))