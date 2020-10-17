from settings import*
import pygame as pg
from random import choice
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    # initializing the sprite
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        # surface to draw sprite on
        self.game = game
        self.walking = False
        self.jumping = False
        # counting frames
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        # setting character image
        self.image = self.game.spritesheet.get_image(690, 406, 120, 201)

        # declaring reactangle for sprite object
        self.rect = self.image.get_rect()
        # centering our rect sprite
        self.rect.center = (40, HEIGHT-100)
        # starting position for object player
        self.pos = vec(40, HEIGHT-100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
    # loading all the images: frame-wise

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(614, 1063, 120, 191),
                                self.game.spritesheet.get_image(690, 406, 120, 201)]

        for frame in self.standing_frames:
            # removing the black background from the image
            frame.set_colorkey(BLACK)

        self.walk_frames_r = [self.game.spritesheet.get_image(678, 860, 120, 201),
                              self.game.spritesheet.get_image(692, 1458, 120, 207)]

        self.walk_frames_l = []

        # flipping the right walk frames
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))

        self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)
        self.jump_frame.set_colorkey(BLACK)
    # defining jump

    def jump(self):
        # jumping only when standing on platform
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits:
            self.vel.y = -PLAYER_JUMP

    # updating the sprite
    def update(self):
        # adding animations
        self.animate()
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
        # setting a threshold to stop the character
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        self.pos += self.vel+(0.5*self.acc)
        # wrapping the sprite rectangle
        # making the character go off the screen fully and then appear to the other side of the screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2
        # putting player's midbottom at screen's center
        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        # Show walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (
                    self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom

                # if the character is going in right direction
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                # if left
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # Shoe idle animation
        if not self.jumping and not self.walking:
            # checking time since the frames last updated and changing frames automatically after 350 milliseconds
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (
                    self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                # changing the character image according to the frame number
                self.image = self.standing_frames[self.current_frame]
                # new rect for the next frame
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Platform(pg.sprite.Sprite):
   # initializing platform class
    def __init__(self, game,  x, y):
        # initializing sprite
        pg.sprite.Sprite.__init__(self)
        self.game = game
        # getting platform images
        images = [self.game.spritesheet.get_image(0, 288, 380, 94),
                  self.game.spritesheet.get_image(213, 1662, 201, 100)]
        # choosing random image from images list for the platform
        self.image = choice(images)
        self.image.set_colorkey(BLACK)
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
