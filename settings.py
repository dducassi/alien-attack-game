class Settings:
    """A class to store the settings for Raid on Canpus Prime"""

    def __init__(self):
        """Initialize the game's static settings."""

        # Screen settings
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (10, 10, 40)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 4
        self.bullet_height = 12
        self.bullet_color = (10, 255, 10)
        self.bullets_allowed = 7

        # Enemy Bomb settings
        self.alien_bullet_color = (255, 20, 20)
        self.alien_bullet_width = 7
        self.alien_bullet_height = 7
       

        # Alien settings
        self.fleet_drop_speed = 15
       

        # How quickly game speeds up
        self.speedup_scale = 1.2

        # How quickly alien points scale
        self.score_scale = 2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_bullet_speed = 1.0
        self.alien_speed = 1.0
        
         # fleet_direction of 1 = right, -1 = left
        self.fleet_direction = 1

        # Score settings
        self.alien_points = 10

    def increase_speed(self):
        """Increase the speed settings and alien points"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_bullet_speed *= self.speedup_scale 

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
        
