import pygame

class AIController:
    def __init__(self, game):
        self.game = game
        self.ship = game.ship
        self.aliens = game.aliens
        self.last_fire_time = 0 
        self.fire_delay = 250    # milliseconds

    def get_action(self):
        if not self.aliens:
            return "idle"

        # Track the closest alien
        closest_alien = min(
            self.aliens.sprites(),
            key=lambda alien: abs(alien.rect.centerx - self.ship.rect.centerx)
        )

        alien_x = closest_alien.rect.centerx
        alien_y = closest_alien.rect.centery
        ship_x = self.ship.rect.centerx
        ship_y = self.ship.rect.centery

        dx = alien_x - ship_x
        dy = alien_y - ship_y

        bullet_speed = -self.game.settings.bullet_speed
        alien_speed_x = self.game.settings.alien_speed * self.game.settings.fleet_direction

        # Estimate time it takes bullet to reach the alien's Y level
        travel_time = abs((alien_y - ship_y) / bullet_speed)

        # Predict where alien will be when bullet gets there
        lead_x = alien_x + alien_speed_x * travel_time
        dx_lead = lead_x - ship_x

        if abs(dy) > 400:
            return "up"
        elif dy > - 300 and self.ship.rect.bottom < 600:
            return "down"
        elif abs(dx_lead) > 180:
            return "right" if dx> 0 else "left"
        else:
            now = pygame.time.get_ticks()
            if now - self.last_fire_time >= self.fire_delay:
                self.last_fire_time = now
                if dx > 0 and alien_speed_x < 0:
                    return "fire"
                elif dx < 0 and alien_speed_x > 0:
                    return "fire"
                else:
                    return "idle"
