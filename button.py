import pygame.font

class Button:
    """A class to build buttons for the game"""



    def __init__(self, rc_game, msg, offset_y=0):
        """Initialize button attributes"""
        self.screen= rc_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set button dimensions and properties
        self.width, self.height = 200, 50
        self.button_color = (200, 30, 30)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont("Courier Bold", 30)

        # Build button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y += offset_y

        # Prep button message
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into an image and center text"""
        self.msg_image = self.font.render(msg, True, self.text_color,
            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)