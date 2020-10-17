# game options and settings
WIDTH = 500
HEIGHT = 650
TITLE = "HOPPY!"
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "Highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"

# player properties
PLAYER_ACC = 0.8
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

# starting platfroms
PLATFORM_LIST = [(0, HEIGHT-40), (WIDTH/2-50, HEIGHT*3/4-50),
                 (125, HEIGHT-350), (350, 200), (175, 100)]  # removed w and h

# defined colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
