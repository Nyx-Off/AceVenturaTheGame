import pygame
from button import Button
from main_menu import MainMenu
import sys

class EndScreen:
    def __init__(self, screen_size, score):
        # Initialize the EndScreen object
        self.score_value = score
        self.is_running = True
        self.screen = pygame.display.set_mode(screen_size,pygame.FULLSCREEN)
        self.font_path = 'font/Crang.ttf'
        self.background_image_path = 'asset/Background/backGroundMainMenue.png'
        self.background_menu_image_path = 'asset/Background/backGroudMenu.png'
        self.highScore_image_path = 'asset/Others/highScore.png'
        self.score_image_path = 'asset/Others/score.png'
        self.font = pygame.font.Font(self.font_path, 55)
        self.high_score = self.lire_high_score()
        self.running = True

        # Create the buttons
        self.menu_items = [
            Button("Menu", self.screen.get_height() / 1.6, self.font_path, self.rejouer, x_offset=-150),
            Button("Quitter", self.screen.get_height() / 1.6, self.font_path, self.quitter, x_offset=150)
        ]
        
    def lire_high_score(self):
        # Read the high score from a file
        try:
            with open("high_score.txt", "r") as fichier:
                return int(fichier.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def rejouer(self):
        # Restart the game
        print("Menu")
        main_menu = MainMenu((1280, 720))
        main_menu.run()
        # Add logic here to restart the game

    def quitter(self):
        # Quit the game
        print("Quitter")
        pygame.quit()
        sys.exit()

    def run(self):
        # Run the end screen loop
        while self.is_running:
            background_image = pygame.image.load(self.background_image_path)
            self.screen.blit(background_image, (0, 0)) 
            
            background_menu_image = pygame.image.load(self.background_menu_image_path)
            self.background_menu = pygame.transform.scale(background_menu_image, (700, 600))
            self.screen.blit(self.background_menu, (290, 100))

            score_text_surface = self.font.render(str(self.score_value), True, (255, 255, 255))
            score_text_size = score_text_surface.get_size()
            score_text_x = self.screen.get_width() / 2.65 - score_text_size[0] / 2
            score_text_y = self.screen.get_height() / 1.8 - score_text_size[1] / 2
            self.screen.blit(score_text_surface, (score_text_x, score_text_y))
            
            high_score_text = self.font.render(str(self.high_score), True, (255, 255, 255))
            high_score_text_size = high_score_text.get_size()
            high_score_text_x = self.screen.get_width() / 1.65 - high_score_text_size[0] / 2
            high_score_text_y = self.screen.get_height() / 1.8 - high_score_text_size[1] / 2
            self.screen.blit(high_score_text, (high_score_text_x, high_score_text_y))
            
            highScore_image = pygame.image.load(self.highScore_image_path)
            self.highScore = pygame.transform.scale(highScore_image, (400, 100))
            self.screen.blit(self.highScore, (self.screen.get_width() / 2.1-30, self.screen.get_height() / 1.5 - 200))
            
            score_image = pygame.image.load(self.score_image_path)
            self.score = pygame.transform.scale(score_image, (400, 100))
            self.screen.blit(self.score, (self.screen.get_width() / 4.5, self.screen.get_height() / 1.5 - 200))
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for button in self.menu_items:
                button.draw(self.screen, mouse_x, mouse_y, pygame.mouse.get_pressed()[0])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        for button in self.menu_items:
                            if button.mouse_over_button(event.pos[0], event.pos[1]):
                                button.click()

            pygame.display.update()
            
    def quitter_ecran_fin(self):
        # Quit the end screen
        self.is_running = False