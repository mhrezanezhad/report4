import time

import pygame as pg

pg.init()
screen_size = 500, 550
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Kakuro")
font1 = pg.font.SysFont("comicsans", 20)
delay = False


def draw_background(Grid_of_the_game, delay_number=None):
    if delay_number:
        global delay
        delay = delay_number
    screen.fill(pg.Color("white"))
    height = len(Grid_of_the_game)
    width = len(Grid_of_the_game[0])
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(0, 0, 500, 500), 1)
    cells_height = 500 / height
    cells_width = 500 / width

    for i in range(1, height):
        pg.draw.line(screen, pg.Color("black"), (0, i * cells_height), (500, i * cells_height), 3)
    for i in range(1, width):
        pg.draw.line(screen, pg.Color("black"), (i * cells_width, 0), (i * cells_width, 499), 3)

    for i in range(height):
        for j in range(width):
            cell_value = str(Grid_of_the_game[i][j])
            if cell_value == 'X':
                pg.draw.rect(screen, (40, 30, 20),
                             pg.Rect(j * cells_width + 2, i * cells_height + 2, cells_width - 2, cells_height - 2))
            elif cell_value.find('\\') != -1:
                pg.draw.rect(screen, (40, 30, 20),
                             pg.Rect(j * cells_width + 2, i * cells_height + 2, cells_width - 2, cells_height - 2))
                pg.draw.line(screen, pg.Color('white'), (j * cells_width, i * cells_height),
                             ((j + 1) * cells_width, (i + 1) * cells_height), 1)
                if cell_value.find('\\') > 0:
                    under = cell_value[:cell_value.find('\\')]
                    text = font1.render(under, 1, (255, 255, 255))
                    screen.blit(text, ((j + 0.15) * cells_width, (i + 0.5) * cells_height))
                if cell_value.find('\\') != len(cell_value) - 1:
                    above = cell_value[cell_value.find('\\') + 1:]
                    text = font1.render(above, 1, (255, 255, 255))
                    screen.blit(text, ((j + 0.5) * cells_width, (i) * cells_height))


def write_number_on_screen(var, value, Grid, color):
    if delay:
        time.sleep(delay)
    text = font1.render(str(value), 1, color)
    height = len(Grid)
    width = len(Grid[0])
    cells_height = 500 / height
    cells_width = 500 / width
    screen.blit(text, ((var[1] + 0.4) * cells_width, (var[0] + 0.25) * cells_height))
    screen.blit(text, ((var[1] + 0.4) * cells_width, (var[0] + 0.25) * cells_height))
    pg.display.flip()


def write_steps_and_time(time, steps):
    text = font1.render('time : ' + str(time) + '  second', 1, (0, 0, 0))
    screen.blit(text, (15, 510))

    text = font1.render('steps : ' + str(steps), 1, (0, 0, 0))
    screen.blit(text, (330, 510))

    pg.display.flip()
