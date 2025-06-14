# Scoreboard

import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """A class to report scoring info"""

    def __init__(self, rc_game):
        """Initialize scoring attributes"""
        self.rc_game = rc_game
        self.screen = rc_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = rc_game.settings
        self.stats = rc_game.stats
        
        # Font settings for scoring
        self.text_color = (10, 255, 40)
        self.font = pygame.font.SysFont('Courier Bold', 30)

        self.prep_images()
        

        

    def prep_images(self):
        # Prepare initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()


    def prep_score(self):
        """Turn score into rendered image"""
        rounded_score = round(self.stats.score, -1)
        score_str = f"Score: {rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color)

        # Display score at top right of screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"High: {high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True,
            self.text_color)
        
        # Center high score at top middle
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Check to see if new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """Turn level into rendered image"""
        level_str = f"Level {self.stats.level}"
        self.level_image = self.font.render(level_str, True, self.text_color)
        
        # Position on bottom right of screen
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.screen_rect.bottom - self.level_rect.height
    
    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.rc_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Draw score to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)


        