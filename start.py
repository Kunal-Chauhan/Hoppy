import pygame
import random
from settings import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(title)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

# game loop
running = True
while running:

    # keep loop running at right speed
    clock.tick(FPS)

    # processing input
    for event in pygame.event.get():
        # checking to close window
        if event.type == pygame.QUIT:
            running = False

    # update screen
    all_sprites.update()

    # draw
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    # post drawing
    pygame.display.flip()

pygame.quit()
