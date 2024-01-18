import pygame
from configV2 import *
import sys

class Button:
    def __init__(self, text, y, font_path, action=None, x_offset=0, text_color=TEXT_COLOR):
        self.text = text
        self.y = y
        self.action = action
        try:
            self.font_normal = pygame.font.Font(font_path, FONT_SIZE_NORMAL)
            self.font_zoomed = pygame.font.Font(font_path, FONT_SIZE_ZOOMED)
        except IOError:
            print(f"Erreur de chargement de la police depuis {font_path}")
            sys.exit()
        self.font_normal = pygame.font.Font(font_path, FONT_SIZE_NORMAL)
        self.font_zoomed = pygame.font.Font(font_path, FONT_SIZE_ZOOMED)
        text_surface = self.font_normal.render(self.text, True, TEXT_COLOR)
        self.w, self.h = text_surface.get_size()
        self.w += 20
        self.h += 20
        self.x = SCREEN_SIZE[0] / 2 - self.w / 2
        self.x_offset = x_offset  # Définir le décalage supplémentaire en x
        self.horizontal_offset = 0  # Nouvel attribut pour le décalage horizontal
        self.text_color = text_color  # Ajout de la couleur de texte personnalisée

    def draw(self, surface, mouse_x, mouse_y, pressed):
        zoom = self.mouse_over_button(mouse_x, mouse_y)
        press = (pressed and zoom)
        
        font = self.font_zoomed if zoom else self.font_normal
        text_color = PRESSED_TEXT_COLOR if press else self.text_color

        text_surface = font.render(self.text, True, text_color)
        self.w, self.h = text_surface.get_size()  # Get the size of the text
        self.w += 20  # Add some padding
        self.h += 20  # Add some padding
        self.x = SCREEN_SIZE[0] / 2 - self.w / 2 - self.horizontal_offset + self.x_offset

        # Fonction pour dessiner le bouton
        def draw_button(surface, x, y, w, h, text_surface):
            button_surface = pygame.Surface((w, h))
            button_surface.set_alpha(BUTTON_OPACITY)
            pygame.draw.rect(button_surface, RECTANGLE_COLOR, (0, 0, w, h))
            surface.blit(button_surface, (x, y))
            text_rect = text_surface.get_rect()
            text_rect.center = (x + w / 2, y + h / 2)
            surface.blit(text_surface, text_rect)

        draw_button(surface, self.x, self.y, self.w, self.h, text_surface)

        
    def mouse_over_button(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.w and self.y <= mouse_y <= self.y + self.h

    def click(self):
        if self.action:
            self.action()