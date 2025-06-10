import pygame
import os

global monitor_size
monitor_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
global screen
screen = pygame.display.set_mode((800, 400), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
pygame.display.set_caption("Element Clicker")
logo_image = pygame.image.load(os.path.join("assets", "images" ,"icon.png")).convert_alpha()
pygame.display.set_icon(logo_image)