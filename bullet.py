import pygame
from pygame.sprite import Sprite



class Bullet(Sprite):

    def __init__(self, rc_game):
        """Create a bullet object at the ship's current position"""
        super().__init__()
        self.screen = rc_game.screen
        self.settings = rc_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, 
            self.settings.bullet_height)
        self.rect.midtop = rc_game.ship.rect.midtop
        
        # Store the bullet's position as a float
        self.y = float(self.rect.y)
        
    def update(self):
        """Move the bullet up the screen"""
        # Update the exact position of the bullet
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)

