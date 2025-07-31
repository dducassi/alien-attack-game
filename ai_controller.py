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
        closest_alien = sorted(
            self.aliens.sprites(),
            key=lambda alien: (-alien.rect.bottom, abs(alien.rect.centerx - self.ship.rect.centerx))
        )[0]

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

        # 1. Find dangerous alien bullets
        danger_zone_width = self.ship.rect.width * 1.1
        danger_zone_height = 150  # how far above the ship we start dodging

        dangerous_bullets = [
            b for b in self.game.alien_bullets.sprites()
            if (
                self.ship.rect.top - danger_zone_height < b.rect.centery < self.ship.rect.bottom and
                abs(b.rect.centerx - self.ship.rect.centerx) < danger_zone_width
            )
        ]

        if dangerous_bullets:
            # 2. Choose a dodge direction
            bullet = dangerous_bullets[0]  # Just dodge the first for now
            if bullet.rect.centerx >= self.ship.rect.centerx:
                return "left"  # Bullet is to the right, dodge left
            else:
                return "right"  # Bullet is to the left, dodge right

        if abs(dy) > 300:
            return "up"
        elif dy > - 250 and self.ship.rect.bottom < 600:
            return "down"
        elif abs(dx_lead) > (abs(alien_speed_x) * travel_time) * 2:
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
