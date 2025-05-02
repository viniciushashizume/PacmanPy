import pygame, random

class Ghost:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/Ghost.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = random.choice([pygame.Vector2(1,0), pygame.Vector2(0,1), pygame.Vector2(-1,0), pygame.Vector2(0,-1)])
        self.speed = 2

    def update(self, game_map):
        new_pos = self.rect.move(self.direction * self.speed)
        if game_map.is_wall(new_pos.center):
            self.direction = random.choice([pygame.Vector2(1,0), pygame.Vector2(0,1), pygame.Vector2(-1,0), pygame.Vector2(0,-1)])
        else:
            self.rect = new_pos

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
