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

        if abs(dx) > 10:
            return "right" if dx > 0 else "left"
        elif abs(dy) > 400:
            return "up"
        elif dy > - 300 and self.ship.rect.bottom < 600:
            return "down"
        else:
            now = pygame.time.get_ticks()
            if now - self.last_fire_time >= self.fire_delay:
                self.last_fire_time = now
                return "fire"
            else:
                return "idle"
