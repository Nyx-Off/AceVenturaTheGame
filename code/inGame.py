import math
import random
import pygame as py
from pygame.sprite import spritecollideany
import pygame.joystick as joystick

from Perso import Perso
from Rock import Rock
from Coin import Coin

# Constantes
SPEED_INCREASE_EVENT = py.USEREVENT + 1
SPEED_INCREASE_INTERVAL = 7000  # millisecondes (7 secondes)
FONT_PATH = 'font/Crang.ttf'
BG_IMAGE_PATH = "asset/Background/Fond_Final.png"
PLAYER_IMAGES = ["asset/Player/AceVenturaCharacter1.png", "asset/Player/AceVenturaCharacter2.png", "asset/Player/AceVenturaCharacter3.png"]
ROCK_IMAGES = [f"asset/Obstacles/Obstacles{i}.PNG" for i in range(1, 5)]
COIN_IMAGES = [f"asset/Points/{color}Diamond.png" for color in ['Bleu', 'Green', 'Purpel', 'Red']]
SOUNDS = {
    "life_lost": "music/hit.mp3",
    "game_over": "music/Game_Over.mp3",
    "get_point": "music/Coin01.mp3",
}
HEART_IMAGE_PATH = "asset/Others/heart.png"
BACKGROUND_SCORE_IMAGE_PATH = "asset/Others/BackgroundInGame.png"

class InGame():
    def __init__(self, initial_volume=1.0):
        # Initialisation
        joystick.init()
        self.font = py.font.Font(FONT_PATH, 15)
        self.speed = 15
        py.time.set_timer(SPEED_INCREASE_EVENT, SPEED_INCREASE_INTERVAL)
        self.setup_game()
        self.clock = py.time.Clock()
        self.run = True
        self.FrameHeight = 720
        self.FrameWidth = 1280
        self.dt = 0
        self.player_pos = 2
        self.spawn_timer = 0
        self.spawn_interval = 5
        self.text_color = (22, 69, 62)
        py.display.set_caption("Ace Ventura - The Game")
        self.screen = py.display.set_mode((self.FrameWidth, self.FrameHeight))
        self.bg = py.image.load(BG_IMAGE_PATH).convert()
        self.perso = Perso(PLAYER_IMAGES, 100, 100)
        self.all_sprites_group = py.sprite.Group()
        self.caillou_group = py.sprite.Group()
        self.coin_group = py.sprite.Group()
        self.ennemy_group = py.sprite.Group()
        self.frame_index = 0
        self.all_sprites_group.add(self.perso)
        self.pause_duration = 200
        self.last_move_time = py.time.get_ticks()
        self.scroll = 0
        self.tiles = math.ceil(self.FrameWidth / self.bg.get_width()) + 1000
        self.sounds = {key: py.mixer.Sound(value) for key, value in SOUNDS.items()}
        self.set_sound_volume(initial_volume)

    def set_sound_volume(self, volume):
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def setup_game(self):
        # Configuration du jeu
        if py.joystick.get_count() > 0:
            self.joystick = py.joystick.Joystick(0)
            self.joystick.init()
        else:
            print("Aucune manette détectée")
                
        self.clock = py.time.Clock()
        self.run = True
        self.all_sprites_group = py.sprite.Group()
        self.caillou_group = py.sprite.Group()
        self.coin_group = py.sprite.Group()
        self.ennemy_group = py.sprite.Group()
        self.perso = Perso(PLAYER_IMAGES, 100, 100)
        self.all_sprites_group.add(self.perso)
        Rock.last_rock_x = 1280
        Coin.last_coin_x = 1280
        
    def enregistrer_high_score(self, nouveau_score):
        # Enregistre le nouveau score dans un fichier
        try:
            with open("high_score.txt", "r") as fichier:
                high_score = int(fichier.read().strip())
        except (FileNotFoundError, ValueError):
                high_score = 0

        if nouveau_score > high_score:
            with open("high_score.txt", "w") as fichier:
                fichier.write(str(nouveau_score))

    def quitter_jeu(self):
        # Quitte le jeu
        self.run = False 

    def generate_random_objects(self, group, class_type, image_paths, width, height):
        # Génère des objets aléatoires
        if random.randint(1, 100) < 50:
            image_path = random.choice(image_paths)
            new_object = class_type(image_path, width, height)
            if not spritecollideany(new_object, self.all_sprites_group):
                group.add(new_object)
                self.ennemy_group.add(new_object)
                self.all_sprites_group.add(new_object)

    def update(self):
        # Met à jour le jeu
        self.clock.tick(50)
        
        i = 0
        while (i < self.tiles):
            self.screen.blit(self.bg, (self.bg.get_width() * i + self.scroll, 0))
            i += 1
        self.scroll -= 6

        if abs(self.scroll) > self.bg.get_width():
            scroll = 0

        for event in py.event.get():
            if event.type == py.QUIT:
                self.run = False
            elif event.type == SPEED_INCREASE_EVENT:
                print(self.speed)
                self.speed += 1

        keys = py.key.get_pressed()
        current_time = py.time.get_ticks()
        joystick_count = joystick.get_count()
        if joystick_count > 0:
            gamepad = joystick.Joystick(0)
            gamepad.init()
            
        move_up = keys[py.K_w] or keys[py.K_UP] or (joystick_count > 0 and gamepad.get_axis(1) < -0.5)
        move_down = keys[py.K_s] or keys[py.K_DOWN] or (joystick_count > 0 and gamepad.get_axis(1) > 0.5)
        
        if move_up and self.player_pos > 1 and current_time - self.last_move_time > self.pause_duration:
            self.player_pos -= 1
            self.last_move_time = current_time
        elif move_down and self.player_pos < 3 and current_time - self.last_move_time > self.pause_duration:
            self.player_pos += 1
            self.last_move_time = current_time

        if self.player_pos == 1:
            self.perso.rect.topleft = (100, 250)
        elif self.player_pos == 2:
            self.perso.rect.topleft = (100, 400)
        elif self.player_pos == 3:
            self.perso.rect.topleft = (100, 520)

        self.perso.update()
        self.ennemy_group.update(self.speed)
        self.screen.blit(self.perso.image, self.perso.rect)
        self.spawn_timer += self.dt
        
        if self.spawn_timer >= self.spawn_interval:
            choice = random.randint(1, 10)
            if 1 <= choice <= 8:
                rock_path = random.choice(ROCK_IMAGES)
                self.generate_random_objects(self.caillou_group, Rock, [rock_path], 50, 50)
            elif choice == 9:
                coin_path = random.choice(COIN_IMAGES)
                self.generate_random_objects(self.coin_group, Coin, [coin_path], 50, 50)

            self.spawn_timer = 0

        for caillou in self.caillou_group:
            if self.perso.rect.colliderect(caillou.rect):
                print("Collision !")
                self.perso.lives -= 1
                self.sounds["life_lost"].play()

                if self.perso.lives <= 0:
                    print("Game Over ! Vous n'avez plus de vies.")
                    self.sounds["game_over"].play()
                    self.perso.game_over = True
                    self.ennemy_group.empty()
                else:
                    self.perso.image.set_alpha(158)
                    self.perso.start_blinking()

                caillou.rect.x = -1000

        if self.perso.over:
            from end_screen import EndScreen
            py.mixer.music.load("music\Epic at the Jungle.mp3")
            py.mixer.music.play(-1)
            print("ici")
            self.quitter_jeu()
            self.enregistrer_high_score(self.perso.points)
            end_screen = EndScreen((1280, 720), self.perso.points)
            end_screen.run()
            self.run = False
            return

        background_score = py.image.load(BACKGROUND_SCORE_IMAGE_PATH)
        background_score_resized = py.transform.scale(background_score, (200, 200))
              
        x = 1050
        y = -25
        
        self.screen.blit(background_score_resized, (x, y))

        for coin in self.coin_group:
            if self.perso.rect.colliderect(coin.rect):
                print("+1 point")
                self.sounds["get_point"].play()
                self.perso.points += 1
                coin.rect.x = -1000

        if self.perso.lives > 0:
            heart = py.image.load(HEART_IMAGE_PATH).convert_alpha()
            heart = py.transform.scale(heart, (30, 30))
            for i in range(self.perso.lives):
                self.screen.blit(heart, (self.FrameWidth - (70 + 30 * i)-41, 70))

            points_text = self.font.render(f"Points : {self.perso.points}", True, self.text_color)
            self.screen.blit(points_text, (self.FrameWidth - 165, 100))

        self.ennemy_group.draw(self.screen)
        self.dt = self.clock.tick(50)
        py.display.flip()
        py.display.update()

    def run_game(self):
        # Lance le jeu
        self.setup_game()
        while self.run:
            self.update()

        from end_screen import EndScreen
        end_screen = EndScreen((1280, 720))
        end_screen.run()