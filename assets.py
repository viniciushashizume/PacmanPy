import pygame

class Assets:
    def __init__(self):
        self.pacman_img = pygame.transform.scale(pygame.image.load("assets/PacMan.png"), (32, 32))
        self.ghost_img = pygame.transform.scale(pygame.image.load("assets/Ghost.png"), (32, 32))
        self.dot_img = pygame.transform.scale(pygame.image.load("assets/dot.png"), (8, 8))
        self.wall_img = pygame.transform.scale(pygame.image.load("assets/wall.png"), (32, 32))