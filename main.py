import boards
import graphics
import sys
import pygame
from csps import Csps
import time

start_time = time.time()
board = boards.easy1 # you can change the board
graphics.draw_background(board)
pygame.display.flip()

# (board, use forward checking filter, use pruning filter, use MLV ordering)
X = Csps(board, False, True, True)

graphics.write_steps_and_time(round(time.time() - start_time, 2), X.step)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
