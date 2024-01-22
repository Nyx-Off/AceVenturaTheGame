import pygame
import pygame_gui
import sys
from buttonV2 import Button
from configV2 import *

from inGame import InGame

class MainMenu:
    def __init__(self, size):
        self.is_running = True 
        self.size = size
        self.screen = pygame.display.set_mode(self.size,pygame.FULLSCREEN)
        # le reste de votre code d'initialisation ici
        # Initialisation de Pygame et des paramètres de base
        pygame.mixer.init()
        pygame.display.set_caption("Menu Principal Ace Ventura - The Game")

        # Définition des attributs de la classe
        self.font_path = 'font/Crang.ttf'
        self.background_menu_image_path = 'asset/backGroudMenu.png'
        self.logo_image_path = 'asset/logo32x32.png'
        self.background_image_path = 'asset/backGroundMainMenue.png'
        self.logo_ventura_image_path = 'asset/logoVentura.png'
        self.menu_music_path = 'music/MenuMusic.mp3'


        # Charger et configurer les ressources
        self.load_resources()
        self.create_ui_elements(size)
        self.create_buttons()

    def reinitialiser_pygame(self):
        pygame.init()
        pygame.font.init()  # réinitialise le module de police
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(self.size)

    def load_resources(self):
        self.background_menu = pygame.image.load(self.background_menu_image_path)
        self.background_menu = pygame.transform.scale(self.background_menu, (700, 600))

        self.logo_image = pygame.image.load(self.logo_image_path)
        pygame.display.set_icon(self.logo_image)

        self.background_image = pygame.image.load(self.background_image_path)
        self.logo_ventura_image = pygame.image.load(self.logo_ventura_image_path)

        pygame.mixer.music.load(self.menu_music_path)
        pygame.mixer.music.play(-1)

    def create_ui_elements(self, screen_size):
        self.ui_manager = pygame_gui.UIManager(screen_size)
        self.volume_slider_rect = pygame.Rect((screen_size[0] / 2 + 650, screen_size[1] / 2 + 22), (300, 30))
        self.volume_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=self.volume_slider_rect,
            start_value=pygame.mixer.music.get_volume(),
            value_range=(0.0, 1.0),
            manager=self.ui_manager
        )

    def create_buttons(self):
        self.menu_items = [
            Button("Jouer", self.screen.get_height() / 2 - 60, self.font_path, self.jouer),
            Button("Paramètres", self.screen.get_height() / 2.5 + MESSAGE_SPACING, self.font_path, self.parametres),
            Button("Quitter", self.screen.get_height() / 2.4 + MESSAGE_SPACING * 2, self.font_path, self.quitter),
            Button("Retour", self.screen.get_height() / 1.9 + MESSAGE_SPACING, self.font_path, self.retour, x_offset=800),
            Button("Son", self.screen.get_height() / 2 - MESSAGE_SPACING, self.font_path, self.nothing, x_offset=800),
            Button("Crédit", self.screen.get_height() / 1.1 - MESSAGE_SPACING, self.font_path, self.credit, x_offset=-350, text_color=(255, 255, 255)),
            Button("Retour", self.screen.get_height() / 1.8 + MESSAGE_SPACING, self.font_path, self.retour, x_offset=-1500),
            Button("Marine ", self.screen.get_height() / 2.8 + MESSAGE_SPACING, self.font_path, self.nothing, x_offset=-1600, text_color=(240, 212, 29)),
            Button("Adrien ", self.screen.get_height() / 2.3 + MESSAGE_SPACING, self.font_path, self.nothing, x_offset=-1600, text_color=(14, 91, 135)),
            Button("Samy ", self.screen.get_height() / 3.1 + MESSAGE_SPACING, self.font_path, self.nothing, x_offset=-1370, text_color=(224, 20, 20)),
            Button("Bilel ", self.screen.get_height() / 2.5 + MESSAGE_SPACING, self.font_path, self.nothing, x_offset=-1370, text_color=(14, 135, 66)),
            Button("Thommy ", self.screen.get_height() / 2.1+ MESSAGE_SPACING, self.font_path, self.nothing, x_offset=-1370, text_color=(158, 50, 168)),
        ]

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.background_menu, (290, 100))
        self.screen.blit(self.logo_ventura_image, (220, -10))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for button in self.menu_items:
            button.draw(self.screen, mouse_x, mouse_y, pygame.mouse.get_pressed()[0])

        self.ui_manager.draw_ui(self.screen)
        pygame.display.update()

    def update(self, time_delta):
        for event in pygame.event.get():
            self.ui_manager.process_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Bouton gauche de la souris
                    for button in self.menu_items:
                        if button.mouse_over_button(event.pos[0], event.pos[1]):
                            button.click()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.volume_slider:
                        pygame.mixer.music.set_volume(event.value)

        self.ui_manager.update(time_delta)
    
    def run(self):
        while self.is_running:
            time_delta = pygame.time.get_ticks() / 1000.0
            self.update(time_delta)
            self.draw()

    def shift_buttons_left(self):
        button_offset = 800
        self.volume_slider.set_relative_position((self.volume_slider_rect.x - button_offset, self.volume_slider_rect.y))
        for button in self.menu_items:
            button.horizontal_offset = button_offset  # Définir le décalage pour chaque bouton

    def shift_buttons_right(self):
        button_offset = 0
        self.volume_slider.set_relative_position((self.volume_slider_rect.x, self.volume_slider_rect.y))
        for button in self.menu_items:
            button.horizontal_offset = button_offset  # Remettre le décalage à zéro pour chaque bouton
    
    def shift_buttons_right2(self):
        button_offset = -1500
        self.volume_slider.set_relative_position((self.volume_slider_rect.x, self.volume_slider_rect.y))
        for button in self.menu_items:
            button.horizontal_offset = button_offset  # Remettre le décalage à zéro pour chaque bouton

    def jouer(self):
        print("Jouer")
        pygame.mixer.music.load("music\Jungle.mp3")
        pygame.mixer.music.play(-1)
        game_instance = InGame()
        game_instance.run_game()
        self.is_running = False  # Ajoutez cette ligne pour arrêter la boucle
        self.reinitialiser_pygame()  # Réinitialisez Pygame après la fermeture de InGame

    def parametres(self):
        print("Paramètres")
        self.shift_buttons_left()

    def quitter(self):
        print("Quitter")
        pygame.quit()
        sys.exit()

    def retour(self):
        print("Retour")
        self.shift_buttons_right()

    def Son(self):
        print("Son")

    def credit(self):
        self.shift_buttons_right2()
        print("Crédit")
        
    def nothing(self):
        print("not used yet")
        #from end_screen import EndScreen
        # À l'endroit où vous gérez la fin du jeu :
        #end_screen = EndScreen((1280, 720))
        #end_screen.run()
