# importing files and options
import pygame as pg
import random
from settings import *
from sprites import *


class Game:

    # initialising class attributes
    def __init__(self):
        # initialise game window
        pg.init()
        pg.mixer.init()
        # making game window
        self.screen = pg.display.set_mode((width, height))
        # setting a title
        pg.display.set_caption(title)
        # clock
        self.clock = pg.time.Clock()
        # declaring variable for loop to run
        self.running = True

    def new(self):
        # start new game
        self.all_sprites = pg.sprite.Group()
        # running new game
        self.run()

    def run(self):
        # game loop
        # keep loop running at right speed
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # game loop update
        self.all_sprites.update()
        pass

    def events(self):
        # game loops events

        # processing input
        for event in pg.event.get():

            # checking to close window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # game loop draw
        # draw
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        # post drawing
        pg.display.flip()

    def show_start_screen(self):
        # start screen
        pass

    def show_go_screen(self):
        # game over or continue
        pass


# make a new game object
G = Game()
# showing start screen
G.show_start_screen()
while G.running:
    # creating new game
    G.new()
    G.show_go_screen()

pg.quit()
