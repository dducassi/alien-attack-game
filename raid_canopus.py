import sys
from time import sleep

import os
script_dir = os.path.dirname(os.path.abspath(__file__))
if getattr(sys, 'frozen', False):
    # Running as EXE - use temporary bundle directory
    base_dir = sys._MEIPASS
else:
    # Running as script - use normal script directory
    base_dir = script_dir

import pygame
from pathlib import Path
from random import randint



from settings import Settings
from ship import Ship
from bullet import Bullet
from alien_bullet import AlienBullet
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from star import Star
from ai_controller import AIController 

class RaidCanopus:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, 
            self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Raid on Canopus Prime")

        # Create an instance to store game stats and make scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        

        self._create_fleet()
        
        # Start game inactive
        self.game_active = False
        
        # Make the Play button.
        self.play_button = Button(self, "Play", offset_y = -40)
        self.play_ai_button = Button(self, "Play (AI)", offset_y = 40)

        self.ai_mode = False 
        self.ai = AIController(self) 
        

    def run_game(self):
        """Start the game's main loop."""
        while True:
            # Check events and update.
            self._check_events()
            self._create_starfield()
            self._update_stars()
            
            if self.game_active:
                if self.ai_mode:
                    action = self.ai.get_action()
                    self._execute_ai_action(action)

                self.ship.update()
                self._update_bullets()
                self._update_alien_bullets()
                self._update_aliens(self.aliens)

            self._update_screen()
            self.clock.tick(60)

    def reset(self, ai_mode=False):
    # Reset the game statistics and settings
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.ai_mode = ai_mode
        self.game_active = True

        # Clear bullets and aliens
        self.bullets.empty()
        self.alien_bullets.empty()
        self.aliens.empty()

        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
    
    def _execute_ai_action(self, action):
        if action == "left":
            self.ship.moving_left = True
            self.ship.moving_right = False
        elif action == "right":
            self.ship.moving_right = True
            self.ship.moving_left = False
        else:
            self.ship.moving_left = False
            self.ship.moving_right = False

        if action == "up":
            self.ship.moving_up = True
            self.ship.moving_down = False
        elif action == "down":
            self.ship.moving_down = True
            self.ship.moving_up = False
        else:
            self.ship.moving_up = False
            self.ship.moving_down = False

        if action == "fire":
            self._fire_bullet()


    def _create_star(self, x_position, y_position):
        """Place one star in the grid"""
        new_star = Star(self)
        new_star.x = x_position
        new_star.rect.x = x_position
        new_star.rect.y = y_position
        self.stars.add(new_star)

    def _create_starfield(self):
        """Create the field of stars"""
        # Create a random grid of stars 
        star = Star(self)
        star_width, star_height = star.rect.size

        current_x, current_y = (randint(3, 900) * star_width, 
            randint(1, 5) * star_height)
        while current_x < (self.settings.screen_width):
            self._create_star(current_x, current_y)
            current_x += (randint(221, 881) * star_width) - 4 * star_width
            
    def _update_stars(self):
        """Update the positions of the stars in the grid"""
        self.stars.update()
        for star in self.stars.copy():
                if star.rect.bottom >= 600:
                    self.stars.remove(star)
    
    def get_hs_path(self):
        if getattr(sys, 'frozen', False):
        # For EXE: save to user's appdata folder
            return Path(os.getenv(
                'APPDATA')) / 'RaidCanopus' / 'high_score.txt'
        else:
        # For development: save in project folder
            return Path('high_score.txt')

    def write_high_score(self):
        current_high_score = str(self.stats.high_score)
        print(current_high_score)
        hs_path = self.get_hs_path()
        try:
            hs_path.write_text(current_high_score)
        except (FileNotFoundError, ValueError):
            current_high_score = 0

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.write_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # check key down events
                self._check_keydown_events(event)  
            elif event.type == pygame.KEYUP:
                # Stop moving right when not pressed
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_play_ai_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self.reset(ai_mode=False)

    def _check_play_ai_button(self, mouse_pos):
        if self.play_ai_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self.reset(ai_mode=True)
                
    
    def _check_keydown_events(self, event):
        if event.key == pygame.K_SPACE:
            if self.ai_mode == False:
                self._fire_bullet()
        elif event.key == pygame.K_RIGHT:
            if self.ai_mode == False:
                self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            if self.ai_mode == False:
                self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            if self.ai_mode == False:
                self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            if self.ai_mode == False:
                self.ship.moving_down = True
        elif event.key == pygame.K_q:
            self.write_high_score()
            sys.exit()
       
    
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self) 
            self.bullets.add(new_bullet)

    def _check_fire(self, alien):
        # Roll for whether alien fires
        self.fire_roll = randint(0, 121 * len(self.aliens))
        if self.fire_roll == 69:
            # Alien Fire
            new_alien_bullet = AlienBullet(rc, alien)
            self.alien_bullets.add(new_alien_bullet)
               

    
    def _create_alien(self, x_position, y_position):
            """Place one alien to place it in the fleet"""
            new_alien = Alien(self)
            new_alien.x = x_position
            new_alien.rect.x = x_position
            new_alien.rect.y = y_position
            self.aliens.add(new_alien)

    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Create aliens until no room left
        # Spacing between aliens is one alien width and one alien height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 20
                 * alien_height):
            while current_x < (self.settings.screen_width - 3 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2* alien_height
    
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached edge"""
        for alien in self.aliens.sprites():
            if alien in self.aliens.sprites():
                if alien.check_edges():
                    self._change_fleet_direction()
                    break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
                        
    def _update_bullets(self):
        """Update bullets position, delete old bullets"""
        self.bullets.update()
        for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _update_alien_bullets(self):
        self.alien_bullets.update()
        for ebullet in self.alien_bullets.copy():
                if ebullet.rect.top > self.settings.screen_height:
                    self.alien_bullets.remove(ebullet)
        self._check_bullet_ship_collision()

    def _check_bullet_alien_collisions(self):
        # Remove aliens and bullets that collide
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                    self.stats.score += self.settings.alien_points * len(aliens)
                    self.sb.prep_score()
                    self.sb.check_high_score()
        
        if not self.aliens:
            self._start_new_level()
           
    def _check_bullet_ship_collision(self):
        ship_collision = pygame.sprite.spritecollide(
            self.ship, self.alien_bullets, False)
        if ship_collision:
            self._ship_hit()


    def _start_new_level(self):
        self.bullets.empty()
        self.alien_bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        # Increase level
        self.stats.level += 1
        self.sb.prep_level()
        

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left >= 1:
            # Decrement ships_left and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Get rid of any remaiing bullets and aliens
            self.bullets.empty()
            self.alien_bullets.empty()
            self.aliens.empty()
            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(1)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reaches the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat like ship hit
                self._ship_hit()
                break

    def _update_aliens(self, alien):
        """Check if fleet at edge, then update positions"""
        self._check_fleet_edges()
        self.aliens.update()
        for alien in self.aliens:
            self._check_fire(alien)

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting bottom
        self._check_aliens_bottom()

    
    def _update_screen(self):
        # Redraw the screen during each pass thru loop
        ## (star field location?)
        self.screen.fill(self.settings.bg_color)

        self.stars.draw(self.screen)

        # Draw bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        for alien_bullet in self.alien_bullets.sprites():
            alien_bullet.draw_alien_bullet()

        ## Draw the ship
        self.ship.blitme()

        ## Draw the aliens
        self.aliens.draw(self.screen)

        

        # Draw the score info
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()
            self.play_ai_button.draw_button()
            
        ## Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance and run the game.
    rc = RaidCanopus()
    rc.run_game()
    