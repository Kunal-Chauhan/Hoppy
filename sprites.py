from settings import*
import pygame as pg
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    # initializing the sprite
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        # surface to draw sprite on
        self.game = game
        # setting character image
        self.image = self.game.spritesheet.get_image(614, 1063, 120, 191)
        # removing the black background from the image
        self.image.set_colorkey(BLACK)
        # declaring reactangle for sprite object
        self.rect = self.image.get_rect()
        # centering our rect sprite
        self.rect.center = (WIDTH/2, HEIGHT/2)
        # starting position for object player
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    # defining jump
    def jump(self):
        # jumping only when standing on platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP

    # updating the sprite
    def update(self):
        # adding gravity to our player
        self.acc = vec(0, PLAYER_GRAV)
        # inputing and processing key presses
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # moving our sprite's rectangle(accelerating)
        # applying friction to only x part
        self.acc.x += self.vel.x*PLAYER_FRICTION
        # equation of motion
        self.vel += self.acc
        self.pos += self.vel+(0.5*self.acc)
        # wrapping the sprite rectangle
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        # putting player's midbottom at screen's center
        self.rect.midbottom = self.pos


class Platform(pg.sprite.Sprite):
   # initializing platform class
    def __init__(self, x, y, w, h):
        # initializing sprite
        pg.sprite.Sprite.__init__(self)
        # aming surface for platform
        self.image = pg.Surface((w, h))
        # coloring surface
        self.image.fill(GREEN)
        # making rect for platform and defining x and y coordinate
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grabbing an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # making the character image smaller
        image = pg.transform.scale(image, (width//2, height//2))
        return image
