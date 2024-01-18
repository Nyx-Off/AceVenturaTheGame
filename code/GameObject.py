from pygame.sprite import Sprite
import pygame as py


class GameObject(py.sprite.Sprite):
    def __init__(self, image_path, width, height, initial_pos):
        super().__init__()

        self.image = py.image.load(image_path).convert_alpha()
        self.image = py.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect()
        self.rect.topleft = initial_pos

    def update(self):
        pass
