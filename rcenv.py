import numpy as np
import pygame

MAX_ALIENS = 50
MAX_BULLETS = 10
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class RaidCanopusEnv:
    def __init__(self, game):
        self.game = game
        self.action_space = [
            "idle",
            "left", "right", "up", "down",
            "left-up", "left-down", "right-up", "right-down",
            "fire",
            "left-fire", "right-fire", "up-fire", "down-fire",
            "left-up-fire", "left-down-fire", "right-up-fire", "right-down-fire"
        ]
        self.action_lookup = [
            "idle",                 # 0
            "left",                 # 1
            "right",                # 2
            "up",                   # 3
            "down",                 # 4
            "fire",                 # 5
            "left+up",              # 6
            "right+up",             # 7
            "left+down",            # 8
            "right+down",           # 9
            "up+fire",              # 10
            "down+fire",            # 11
            "left+fire",            # 12
            "right+fire",           # 13
            "left+up+fire",         # 14
            "right+up+fire",        # 15
            "left+down+fire",       # 16
            "right+down+fire",      # 17
        ]
        self.action_size = len(self.action_space)
        
        # Get one sample observation to infer size
        sample_obs = self._get_observation()
        self.observation_space = np.array(sample_obs)
        self.observation_size = self.observation_space.shape[0]

        self.prev_alien_count = len(self.game.aliens)

    def reset(self):
        self.game.reset()
        self.done = False
        self.prev_alien_count = len(self.game.aliens)
        return self._get_observation()

    def step(self, action):
        action_str = self.action_lookup[action]
        self._apply_action(action_str)

        # Run a single frame of the game loop
        self.game._update_bullets()
        self.game._update_alien_bullets()
        self.game._update_aliens(self.game.aliens)
        self.game.ship.update()

        # Compute reward and done flag
        reward = self._calculate_reward()
        done = not self.game.game_active

        obs = self._get_observation()
        self.prev_alien_count = len(self.game.aliens)
        self.prev_ships_left = self.game.stats.ships_left
        return obs, reward, done, {}


    def _calculate_reward(self):
        reward = -0.1  # small time penalty

        current_alien_count = len(self.game.aliens)
        if current_alien_count < self.prev_alien_count:
            reward += 100 * (self.prev_alien_count - current_alien_count)
        if current_alien_count < 2:
            reward = 10000

        # Penalize *only* when ships_left decreases
        if hasattr(self, "prev_ships_left"):
            if self.game.stats.ships_left < self.prev_ships_left:
                reward -= 1000

        self.prev_ships_left = self.game.stats.ships_left
        return reward

    def _get_observation(self):
        obs = []

        # Normalize ship position
        ship_x = self.game.ship.rect.centerx / SCREEN_WIDTH
        ship_y = self.game.ship.rect.centery / SCREEN_HEIGHT
        obs.extend([ship_x, ship_y])

        # Get alien positions
        alien_positions = [
            (alien.rect.centerx / SCREEN_WIDTH, alien.rect.centery / SCREEN_HEIGHT)
            for alien in self.game.aliens.sprites()
        ]

        # Pad or trim to MAX_ALIENS
        while len(alien_positions) < MAX_ALIENS:
            alien_positions.append((0.0, 0.0))
        alien_positions = alien_positions[:MAX_ALIENS]
        for pos in alien_positions:
            obs.extend(pos)

        # Get alien bullet positions
        bullet_positions = [
            (bullet.rect.centerx / SCREEN_WIDTH, bullet.rect.centery / SCREEN_HEIGHT)
            for bullet in self.game.alien_bullets.sprites()
        ]

        # Pad or trim to MAX_BULLETS
        while len(bullet_positions) < MAX_BULLETS:
            bullet_positions.append((0.0, 0.0))
        bullet_positions = bullet_positions[:MAX_BULLETS]
        for pos in bullet_positions:
            obs.extend(pos)

        return np.array(obs, dtype=np.float32)
    
    def _apply_action(self, action_str):
        """Translate a composite action string into game control."""
        # Reset all movement
        self.game.ship.moving_left = False
        self.game.ship.moving_right = False
        self.game.ship.moving_up = False
        self.game.ship.moving_down = False

        # Parse the composite action
        if "left" in action_str:
            self.game.ship.moving_left = True
        if "right" in action_str:
            self.game.ship.moving_right = True
        if "up" in action_str:
            self.game.ship.moving_up = True
        if "down" in action_str:
            self.game.ship.moving_down = True
        if "fire" in action_str:
            self.game._fire_bullet()
