import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, assets):
        super().__init__()
        self.image = assets.pacman_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2

    def update(self, walls):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]: dx = -self.speed
        elif keys[pygame.K_RIGHT]: dx = self.speed
        elif keys[pygame.K_UP]: dy = -self.speed
        elif keys[pygame.K_DOWN]: dy = self.speed

        self.rect.x += dx
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x -= dx
        self.rect.y += dy
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.y -= dy