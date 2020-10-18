# importing files and options
# file I/O
import pygame as pg
import random
from settings import *
from sprites import *
from os import path


class Game:

    # initialising class attributes
    def __init__(self):
        # initialise game window
        pg.init()
        pg.mixer.init()
        # making game window
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # setting a title
        pg.display.set_caption(TITLE)
        # clock
        self.clock = pg.time.Clock()
        # declaring variable for loop to run
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # loading highscore
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # loading spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

        # loading sounds
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump33.wav'))
        self.boost_sound = pg.mixer.Sound(
            path.join(self.snd_dir, 'Boost1.ogg'))
    # start new game

    def new(self):
        self.score = 0
        # making a new sprite group
        self.all_sprites = pg.sprite.LayeredUpdates()
        # making platform group to hold all the platforms
        self.platforms = pg.sprite.Group()
        # powerup group
        self.powerups = pg.sprite.Group()
        # mob group
        self.mobs = pg.sprite.Group()
        self.player = Player(self)
        # spawning a platform
        for plat in PLATFORM_LIST:
            Platform(self, *plat)

        self.mob_timer = 0
        # loading music
        pg.mixer.music.load(path.join(self.snd_dir, 'GameTheme.ogg'))
        # running new game
        self.run()

    def run(self):
        # game loop
        # playing music as the game starts
        pg.mixer.music.play(loops=-1)
        # keep loop running at right speed
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        # music stops when the game ends
        pg.mixer.music.fadeout(250)

    # game loop update
    def update(self):
        # updating properties
        self.all_sprites.update()

        # spawning enemy mob
        now = pg.time.get_ticks()
        if (now-self.mob_timer) > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)
        # player hit mob
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits:
            self.playing = False

        # check if playeer hits a platfrom only if falling
        # if velocity is downward
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right+10 and self.player.pos.x > lowest.rect.left-10:
                    # setting player y position to platform top
                    if self.player.pos.y < hits[0].rect.centery:
                        self.player.pos.y = hits[0].rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        # if player reaches 1/4 of screen
        if self.player.rect.top <= HEIGHT/4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        # player hit power
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False

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
            Platform(self, random.randrange(0, WIDTH-width),
                     random.randrange(-75, -30))

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

            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    # game loop draw
    def draw(self):

        # draw
        # adding backgroud color
        self.screen.fill(BGCOLOR)
        # drawing sprite on screen
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH/2, 15)
        # post drawing
        pg.display.flip()

    # start screen
    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, 'HappyTune.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Arrows to move and Space to jump",
                       22, WHITE, WIDTH/2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT * 3/4)
        self.draw_text("High Score: " + str(self.highscore),
                       22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    # game over or continue
    def show_go_screen(self):
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text("Game Over!", 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Score: "+str(self.score),
                       22, WHITE, WIDTH/2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22,
                       WHITE, WIDTH/2, HEIGHT * 3/4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE: ", 22,
                           WHITE, WIDTH/2, HEIGHT / 2+40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("Highscore: " + str(self.highscore),
                           22, WHITE, WIDTH / 2, HEIGHT / 2+40)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

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
