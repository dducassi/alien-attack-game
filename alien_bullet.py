import pygame
from pygame.sprite import Sprite

from alien import Alien

class AlienBullet(Sprite):

    def __init__(self, rc_game, alien):
    
        super().__init__()
        self.screen = rc_game.screen
        self.settings = rc_game.settings
        self.color = self.settings.alien_bullet_color

        # Create a bullet rect at (0, 0) and set correct position
        self.rect = pygame.Rect(0, 0, self.settings.alien_bullet_width, 
            self.settings.alien_bullet_height)
        self.rect.midbottom = alien.rect.midbottom

        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet down the screen"""
        # Update the exact position of the bullet
        self.y += self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y

    def draw_alien_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
