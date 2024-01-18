from pygame import *
from pygame.sprite import *
import pygame as py
import random
from GameObject import GameObject


class Rock(GameObject):
    last_rock_x = 1280

    def __init__(self, image_path, width, height):
        super().__init__(image_path, width, height, (0, 0))
        self.reset()

    def reset(self):
        self.rect.x = Rock.last_rock_x + 300
        Rock.last_rock_x = self.rect.x
        self.randomize_y()

    def randomize_y(self):
        random_pos = random.choice([1, 2, 3])
        if random_pos == 1:
            self.rect.y = 300
        if random_pos == 2:
            self.rect.y = 400
        if random_pos == 3:
            self.rect.y = 550

    def update(self):
        #Augmenter la vitesse
        speed = 18
        self.rect.x -= speed
        if self.rect.right < 0:
            self.reset()
            self.randomize_y()

        if self.rect.right > 0:
            super().update()