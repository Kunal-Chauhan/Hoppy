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
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # setting a title
        pg.display.set_caption(title)
        # clock
        self.clock = pg.time.Clock()
        # declaring variable for loop to run
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

    # start new game
    def new(self):
        self.score = 0
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
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

        # if player reaches 1/4 of screen
        if self.player.rect.top <= HEIGHT/4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        # player die
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # spawning new platform to keep same number of platforms
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            p = Platform(random.randrange(0, WIDTH-width),
                         random.randrange(-75, -30), width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)

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
        self.draw_text(str(self.score), 22, WHITE, WIDTH/2, 15)
        # post drawing
        pg.display.flip()

    def show_start_screen(self):
        # start screen
        pass

    def show_go_screen(self):
        # game over or continue
        pass

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


G = Game()
# showing start screen
G.show_start_screen()
while G.running:
    # creating new game
    G.new()
    G.show_go_screen()

pg.quit()
