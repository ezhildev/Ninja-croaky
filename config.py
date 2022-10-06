'''config module have lots of constant variables and module imports.'''
import sys
import os
import math
import random
import pygame
from pygame.locals import *
from util_funcs import *

pygame.init()

GAME_TITLE = 'NINJA CROAKY'
TILE_SIZE = 16
GRID_SIZE = 16
SCALE_RATIO = GRID_SIZE / TILE_SIZE

DISPLAY_WIDTH = GRID_SIZE * 48
DISPLAY_HEIGHT = GRID_SIZE * 27
DISPLAY_SIZE = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
DISPLAY_CENTER = tuple([x//2 for x in DISPLAY_SIZE])

FPS = 60

OXFORD_BLUE = '#0E1C36'
DARK_BLUE = '#211F30'
GHOST_WHITE = '#FFFAFF'
DARK_SCREEN = pygame.Surface(DISPLAY_SIZE)
DARK_SCREEN.fill(DARK_BLUE)
DARK_SCREEN.set_alpha(255)

LARGE_FONT = pygame.font.Font('./scr/font/ThaleahFat.ttf', GRID_SIZE * 5)
MED_FONT = pygame.font.Font('./scr/font/ThaleahFat.ttf', GRID_SIZE * 2)
SMALL_FONT = pygame.font.Font('./scr/font/ThaleahFat.ttf', GRID_SIZE )

ICON = pygame.image.load('./scr/image/FNF.ico')