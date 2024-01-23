from pygame.sprite import *
import pygame as py

from GameObject import GameObject

class Perso(GameObject):
    def __init__(self, image_paths, width, height):
        super().__init__(image_paths[0], width, height, (0, 0))
        self.character_width = width
        self.character_height = height
        self.lives = 3
        self.points = 0
        self.is_blinking = False
        self.blinking_duration = 500
        self.blinking_timer = 0
        self.invulnerable = False
        self.image_paths = image_paths
        self.frames_per_movement = 3
        self.current_frame_index = 0
        self.frame_duration = 100
        self.frame_delays = [100, 100, 100]
        self.last_frame_change = py.time.get_ticks()
        self.game_over = False
        self.list_over = ["asset/Player/AceVenturaCharacter_dead.png", "asset/Player/AceVenturaCharacter_dead.png","asset/Player/AceVenturaCharacter_dead.png"]
        self.index_over = 0
        self.over = False
        self.image = py.image.load(self.image_paths[self.current_frame_index]).convert_alpha()
        self.image = py.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.rect.topleft = (self.rect.x, self.rect.y + 100)

    #Blinking function
    def start_blinking(self):
            self.is_blinking = True
            self.blinking_timer = py.time.get_ticks()
            self.invulnerable = True
            self.last_hit_time = py.time.get_ticks()

    def update(self):
        current_time = py.time.get_ticks()
        # Dans la partie 'Animation Game over'
        if self.game_over:
            if current_time - self.last_frame_change >= self.frame_duration:
                self.frame_duration = 700 
                if self.index_over < len(self.list_over):
                    self.image = py.image.load(self.list_over[self.index_over]).convert_alpha()
                    self.image = py.transform.scale(self.image, (150, 150))

                    # Mettez à jour la position du rectangle ici
                    self.rect = self.image.get_rect(center=self.rect.center)

                    self.last_frame_change = current_time
                    self.index_over += 1
                else:
                    self.over = True


            
        #Animation du perso
        elif current_time - self.last_frame_change >= self.frame_duration:
            self.image = py.image.load(self.image_paths[self.current_frame_index]).convert_alpha()
            self.image = py.transform.scale(self.image, (self.rect.width, self.rect.height))
            self.last_frame_change = current_time
            self.current_frame_index = (self.current_frame_index + 1) % len(self.image_paths)

        #Gestion Blinking
        if self.is_blinking:
            elapsed_time = current_time - self.blinking_timer
            if elapsed_time < self.blinking_duration:
                if elapsed_time % 200 < 100:
                    self.image.set_alpha(0)
                else:
                    self.image.set_alpha(255)
            else:
                self.image.set_alpha(255)
                self.is_blinking = False