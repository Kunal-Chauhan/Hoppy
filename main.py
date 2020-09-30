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

    # start new game
    def new(self):
        # making a new sprite group
        self.all_sprites = pg.sprite.Group()
        # making platform group to hold all the platforms
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        # spawning a platform
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
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

    # game loop update
    def update(self):
        # updating properties
        self.all_sprites.update()
        # check if playeer hits a platfrom only if falling
        # if velocity is downward
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                # setting player y position to platform top
                self.player.pos.y = hits[0].rect.top+1
                self.player.vel.y = 0

    def events(self):
        # game loops events

        # processing input
        for event in pg.event.get():

            # checking to close window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # checking jump event
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    # game loop draw
    def draw(self):

        # draw
        self.screen.fill((0, 0, 0))
        # drawing sprite on screen
        self.all_sprites.draw(self.screen)
        # post drawing
        pg.display.flip()

    def show_start_screen(self):
        # start screen
        pass

    def show_go_screen(self):
        # game over or continue
        pass


G = Game()
# showing start screen
G.show_start_screen()
while G.running:
    # creating new game
    G.new()
    G.show_go_screen()

pg.quit()
