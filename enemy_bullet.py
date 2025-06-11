# ENEMY BULLET

import pygame
from pygame.sprite import Sprite

from enemy import Enemy

class EnemyBullet(Sprite):

    def __init__(self, tw_game, alien):
    
        super().__init__()
        self.screen = tw_game.screen
        self.settings = tw_game.settings
        self.color = self.settings.enemy_bullet_color

        # Create a bullet rect at (0, 0) and set correct position
        self.rect = pygame.Rect(0, 0, self.settings.enemy_bullet_width, 
            self.settings.enemy_bullet_height)
        self.rect.midbottom = alien.rect.midbottom

        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet left across the screen"""
        # Update the exact position of the bullet
        self.x -= self.settings.enemy_bullet_speed
        # Update the rect position
        self.rect.x = self.x

    def draw_enemy_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
