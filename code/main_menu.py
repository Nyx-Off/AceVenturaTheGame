import pygame
import pygame_gui
import sys
from button import Button
from config import *
from inGame import InGame

class MainMenu:
    def __init__(self, size):
        self.volume_text_offset = 0
        self.volume_level = 5  # Niveau de volume initial
        self.is_running = True 
        self.size = size
        self.screen = pygame.display.set_mode(self.size,pygame.FULLSCREEN)
        self.font_path = 'font/Crang.ttf'
        self.background_menu_image_path = 'asset/Background/backGroudMenu.png'
        self.background_image_path = 'asset/Background/backGroundMainMenue.png'
        self.logo_ventura_image_path = 'asset/Others/logoVentura.png'
        self.menu_music_path = 'music/MenuMusic.mp3'
        self.logo_ventura_image_path = 'asset/Others/logoVentura.png'
        self.logo_image_path = 'asset/Others/logo32x32.png'
        self.load_resources()
        self.create_ui_elements(size)
        self.create_buttons()
        self.game_instance = InGame()

    def reinitialiser_pygame(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(self.size)

    def load_resources(self):
        # Load images and music
        self.background_menu = pygame.image.load(self.background_menu_image_path)
        self.background_menu = pygame.transform.scale(self.background_menu, (700, 600))
        self.background_image = pygame.image.load(self.background_image_path)
        self.logo_ventura_image = pygame.image.load(self.logo_ventura_image_path)
        pygame.mixer.music.load(self.menu_music_path)
        pygame.mixer.music.play(-1)
        self.logo_image = pygame.image.load(self.logo_image_path)
        pygame.display.set_icon(self.logo_image)

    def create_ui_elements(self, screen_size):
        self.ui_manager = pygame_gui.UIManager(screen_size)

    def create_buttons(self):
        # Create menu buttons
        self.menu_items = [
            Button("Jouer", self.screen.get_height() / 2 - 60, self.font_path, self.jouer),
            Button("Paramètres", self.screen.get_height() / 2.5 + MESSAGE_SPACING, self.font_path, self.parametres),
            Button("Quitter", self.screen.get_height() / 2.4 + MESSAGE_SPACING * 2, self.font_path, self.quitter),
            Button("Retour", self.screen.get_height() / 1.9 + MESSAGE_SPACING, self.font_path, self.retour, x_offset=800),
            Button("Son", self.screen.get_height() / 2.1 - MESSAGE_SPACING, self.font_path, self.Son, x_offset=800),
            Button("+", self.screen.get_height() / 2.35 + MESSAGE_SPACING, self.font_path, self.increase_volume, x_offset=880, text_color=(255, 255, 255)),
            Button("-", self.screen.get_height() / 2.35 + MESSAGE_SPACING, self.font_path, self.decrease_volume, x_offset=720, text_color=(255, 255, 255)),
            Button("Crédit", self.screen.get_height() / 1.1 - MESSAGE_SPACING, self.font_path, self.credit, x_offset=-350, text_color=(255, 255, 255)),
            Button("Retour", self.screen.get_height() / 1.8 + MESSAGE_SPACING, self.font_path, self.retour, x_offset=-1500),
            Button("Marine ", self.screen.get_height() / 2.8 + MESSAGE_SPACING, self.font_path, self.Marine, x_offset=-1600, text_color=(240, 212, 29)),
            Button("Adrien ", self.screen.get_height() / 2.3 + MESSAGE_SPACING, self.font_path, self.Adrien, x_offset=-1600, text_color=(14, 91, 135)),
            Button("Samy ", self.screen.get_height() / 3.1 + MESSAGE_SPACING, self.font_path, self.Samy, x_offset=-1370, text_color=(224, 20, 20)),
            Button("Bilel ", self.screen.get_height() / 2.5 + MESSAGE_SPACING, self.font_path, self.Bilel, x_offset=-1370, text_color=(14, 135, 66)),
            Button("Thommy ", self.screen.get_height() / 2.1+ MESSAGE_SPACING, self.font_path, self.Thommy, x_offset=-1370, text_color=(158, 50, 168)),
        ]

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.background_menu, (290, 100))
        self.screen.blit(self.logo_ventura_image, (220, -10))
        self.draw_volume_level()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for button in self.menu_items:
            button.draw(self.screen, mouse_x, mouse_y, pygame.mouse.get_pressed()[0])
        pygame.display.update()

    def update(self, time_delta):
        pygame.display.set_caption("Menu Principal Ace Ventura - The Game")
        # Handle events and update UI manager
        for event in pygame.event.get():
            self.ui_manager.process_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.menu_items:
                        if button.mouse_over_button(event.pos[0], event.pos[1]):
                            button.click()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.volume_slider:
                        pygame.mixer.music.set_volume(event.value)
        self.ui_manager.update(time_delta)
    
    def run(self):
        # Main loop for the menu screen
        while self.is_running:
            time_delta = pygame.time.get_ticks() / 1000.0
            self.update(time_delta)
            self.draw()

    def shift_buttons_left(self):
        # Shift buttons to the left for settings screen
        button_offset = 800
        self.volume_text_offset = button_offset
        for button in self.menu_items:
            button.horizontal_offset = button_offset

    def shift_buttons_right(self):
        # Shift buttons to the right for main menu screen
        button_offset = 0
        self.volume_text_offset = button_offset
        for button in self.menu_items:
            button.horizontal_offset = button_offset
    
    def shift_buttons_right2(self):
        # Shift buttons to the right for credits screen
        button_offset = -1500
        self.volume_text_offset = button_offset
        for button in self.menu_items:
            button.horizontal_offset = button_offset

    def jouer(self):
        print("Jouer")
        pygame.mixer.music.load("music\\Jungle.mp3")
        pygame.mixer.music.play(-1)
        self.game_instance = InGame()  # Recréez l'instance pour s'assurer qu'elle est réinitialisée
        volume_actuel = self.volume_level / 10
        self.game_instance = InGame(initial_volume=volume_actuel)
        self.game_instance.run_game()
        self.is_running = False
        self.reinitialiser_pygame()


    def parametres(self):
        # Action for "Paramètres" button
        print("Paramètres - ya pas grand chose et ca nous a pris trop de temps ಠ_ಠ")
        self.shift_buttons_left()

    def quitter(self):
        # Action for "Quitter" button
        print("Quitter")
        pygame.quit()
        sys.exit()

    def retour(self):
        # Action for "Retour" button
        print("Retour")
        self.shift_buttons_right()

    def Son(self):
        # Action for "Son" button
        print("Son mit a 0 - un bouton mute quoi ಠ_ಠ")
        if self.volume_level != 0:
            self.volume_level = 0
            pygame.mixer.music.set_volume(0)
            self.game_instance.set_sound_volume(0)
    
    def Samy(self):
        # Action for "Samy" button
        print("Le crack (chef d'équipe) - Dev Partie Menu/fin + integrateurs code (rassemblement des codes) (╯°□°）╯︵ ┻━┻")
        
    def Marine(self):
        # Action for "Marine" button
        print("La boss - Dev Moteur du Jeu(ennemis, perso, cailloux, points, vie, logique, etc) (✿◡‿◡)")
        
    def Adrien(self):
        # Action for "Adrien" button
        print("Le plus beau - graphiste + sound designer ( ͡° ͜ʖ ͡°)")
        
    def Bilel(self):
        # Action for "Bilel" button
        print("Le plus fort - graphiste (*￣3￣)╭")
        
    def Thommy(self):
        # Action for "Thommy" button
        print("Le gourmant - secrétaire xD [il a fait le power point, redactions cahier des charges etc ..., il bien fait ...  ] ( ma faute /samy/ car je ne savais pas quoi lui donner comme rôle) (￣﹏￣；)")        

    def increase_volume(self):
        if self.volume_level < 10:
            self.volume_level += 1
            new_volume = self.volume_level / 10
            pygame.mixer.music.set_volume(new_volume)
            self.game_instance.set_sound_volume(new_volume)  # Mettre à jour le volume des effets sonores

    def decrease_volume(self):
        if self.volume_level > 0:
            self.volume_level -= 1
            new_volume = self.volume_level / 10
            pygame.mixer.music.set_volume(new_volume)
            self.game_instance.set_sound_volume(new_volume)  # Mettre à jour le volume des effets sonores


    def draw_volume_level(self):
        font = pygame.font.Font(self.font_path, 55)
        volume_text = font.render(str(self.volume_level), True, (255, 255, 255))
        text_x = -160 + self.volume_text_offset  # Ajoutez le décalage ici
        text_y = self.screen.get_height() / 2.15 + MESSAGE_SPACING
        text_rect = volume_text.get_rect(center=(text_x, text_y))
        self.screen.blit(volume_text, text_rect)

    def credit(self):
        # Action for "Crédit" button
        self.shift_buttons_right2()
        print("Crédit - L'equipe de choc qui a fait ce jeu")
        
    def nothing(self):
        # Placeholder action for unused buttons
        print("not used yet - ouais je fait l'ameriquain, et alors ? tu vas faire quoi ?")