import pygame
from config import *
import sys

class Button:
    def __init__(self, text, y, font_path, action=None, x_offset=0, text_color=TEXT_COLOR):
        # Initialize the Button object
        self.text = text
        self.y = y
        self.action = action

        # Load the font for normal and zoomed text
        try:
            self.font_normal = pygame.font.Font(font_path, FONT_SIZE_NORMAL)
            self.font_zoomed = pygame.font.Font(font_path, FONT_SIZE_ZOOMED)
        except IOError:
            print(f"Erreur de chargement de la police depuis {font_path}")
            sys.exit()

        # Render the text surface for normal font
        text_surface = self.font_normal.render(self.text, True, TEXT_COLOR)
        self.w, self.h = text_surface.get_size()
        self.w += 20
        self.h += 20
        self.x = SCREEN_SIZE[0] / 2 - self.w / 2
        self.x_offset = x_offset
        self.horizontal_offset = 0
        self.text_color = text_color

    def draw(self, surface, mouse_x, mouse_y, pressed):
        # Draw the button on the surface
        zoom = self.mouse_over_button(mouse_x, mouse_y)
        press = (pressed and zoom)
        
        # Determine the font and text color based on the button state
        font = self.font_zoomed if zoom else self.font_normal
        text_color = PRESSED_TEXT_COLOR if press else self.text_color

        # Render the text surface with the appropriate font and color
        text_surface = font.render(self.text, True, text_color)
        self.w, self.h = text_surface.get_size()
        self.w += 20
        self.h += 20
        self.x = SCREEN_SIZE[0] / 2 - self.w / 2 - self.horizontal_offset + self.x_offset

        def draw_button(surface, x, y, w, h, text_surface):
            # Draw the button rectangle and text on the surface
            button_surface = pygame.Surface((w, h))
            button_surface.set_alpha(BUTTON_OPACITY)
            pygame.draw.rect(button_surface, RECTANGLE_COLOR, (0, 0, w, h))
            surface.blit(button_surface, (x, y))
            text_rect = text_surface.get_rect()
            text_rect.center = (x + w / 2, y + h / 2)
            surface.blit(text_surface, text_rect)

        draw_button(surface, self.x, self.y, self.w, self.h, text_surface)

    def mouse_over_button(self, mouse_x, mouse_y):
        # Check if the mouse is over the button
        return self.x <= mouse_x <= self.x + self.w and self.y <= mouse_y <= self.y + self.h

    def click(self):
        # Perform the button action if defined
        if self.action:
            self.action()