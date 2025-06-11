# GAME STATS

from pathlib import Path
import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
if getattr(sys, 'frozen', False):
    # Running as EXE - use temporary bundle directory
    base_dir = sys._MEIPASS
else:
    # Running as script - use normal script directory
    base_dir = script_dir



class GameStats:
    "Track stats for Raid on Conopus Prime"

    def __init__(self, rc_game):
        """Initialize statistics"""
        self.settings = rc_game.settings
        self.reset_stats()
        # High score should never be reset
        self.high_score = 0
        self._load_high_score()

    
    def _get_hs_path(self):
        if getattr(sys, 'frozen', False):
            app_data_dir = Path(os.getenv('APPDATA')) / 'RaidCanopus'
            return app_data_dir / 'high_score.txt'
        return Path('high_score.txt')
    
    def _load_high_score(self):
        hs_path = self._get_hs_path()
        hs_path.parent.mkdir(parents=True, exist_ok=True) 
        try:
            with open(hs_path, 'r') as file:
                self.high_score = int(file.read())
        except (FileNotFoundError, ValueError):
            self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1