import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, assets):
        super().__init__()
        self.image = assets.wall_img
        self.rect = self.image.get_rect(topleft=(x, y))
        
class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y, assets):
        super().__init__()
        self.image = assets.dot_img
        self.rect = self.image.get_rect(center=(x + 32 // 2, y + 32 // 2))
