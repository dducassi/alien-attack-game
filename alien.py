# ALIEN

import pygame
from pygame.sprite import Sprite
from random import randint
import sys

import os
script_dir = os.path.dirname(os.path.abspath(__file__))
if getattr(sys, 'frozen', False):
    # Running as EXE - use temporary bundle directory
    base_dir = sys._MEIPASS
else:
    # Running as script - use normal script directory
    base_dir = script_dir




class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, rc_game):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = rc_game.screen
        self.settings = rc_game.settings

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load(os.path.join(
                                        base_dir,'images/alien.bmp'))
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien at edge of screen"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
    
    def update(self):
        """Move the alien to the right and roll fire chance"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
    
    
        
