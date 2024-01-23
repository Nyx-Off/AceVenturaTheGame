import pygame
import sys
from main_menu import MainMenu
from end_screen import EndScreen
from inGame import InGame

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    
    while True:
        main_menu = MainMenu((1280, 720))
        main_menu.run()

        game_instance = InGame()
        game_instance.run_game()

        end_screen = EndScreen((1280, 720))
        end_screen.run()

    pygame.quit()
    sys.exit()