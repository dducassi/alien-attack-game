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


class Ship(Sprite):

    def __init__(self, rc_game):
        """Initialize the ship and set starting position"""
        super().__init__()
        self.screen = rc_game.screen
        self.settings = rc_game.settings
        self.screen_rect = rc_game.screen.get_rect()

        # Load the ship image and get its rect
        self.image = pygame.image.load(os.path.join(base_dir,'images/ship.bmp'))
        self.rect = self.image.get_rect()

        # Start each new ship at bottom center
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the ship's exact horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flag; start with a ship that's not moving
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > ((2 * (self.settings.screen_height))/3):
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # Update rect object self.x
        self.rect.x = self.x
        self.rect.y = self.y

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
