import pygame

from pygame.sprite import Sprite
import sys

import os
script_dir = os.path.dirname(os.path.abspath(__file__))
if getattr(sys, 'frozen', False):
    # Running as EXE - use temporary bundle directory
    base_dir = sys._MEIPASS
else:
    # Running as script - use normal script directory
    base_dir = script_dir




class Star(Sprite):

    def __init__(self, starscape):
        
        """Create a star object"""
        super().__init__()
        self.screen = starscape.screen
        self.star_speed = 2

        # Set rect attribute from image load
        self.image = pygame.image.load(os.path.join(base_dir,'images/star.bmp'))
        self.rect = self.image.get_rect()

        # Start each new star near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the star's exact horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
    
    def update(self):
        "Move the star down the screen"
        self.y += self.star_speed
        self.rect.y = self.y
        
        

        
