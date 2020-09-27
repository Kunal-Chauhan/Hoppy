from settings import*
import pygame as pg
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    # initializing the sprite
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        # surface to draw sprite on
        self.image = pg.Surface((30, 40))
        # filling suface with colour
        self.image.fill(YELLOW)
        # declaring reactangle for sprite object
        self.rect = self.image.get_rect()
        # centering our rect sprite
        self.rect.center = (width/2, height/2)
        # starting position for object player
        self.pos = vec(width/2, height/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    # updating the sprite
    def update(self):
        self.acc = vec(0, 0)

        # inputing and processing key presses
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

    # moving our sprite's rectangle(accelerating)
        # applying friction
        self.acc += self.vel*PLAYER_FRICTION
        # equation of motion
        self.vel += self.acc
        self.pos += self.vel+(0.5*self.acc)
        # wrapping the sprite rectangle
        if self.pos.x > width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = width

        self.rect.center = self.pos
