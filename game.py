import pygame
import sys
from settings import WIDTH, HEIGHT, FPS, BLACK
from assets import Assets
from player import Player
from ghost import Ghost
from map import Wall, Dot


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.assets = Assets()
        self.score = 0

        self.walls = pygame.sprite.Group()
        self.dots = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.load_map()

    def load_map(self):
        layout = [
            "WWWWWWWWWWWWWWWWWWWW",
            "W........WW........W",
            "W.WWWW.WW.WW.WWWW.WW",
            "W..................W",
            "W.WW.WWWWWWWW.WW.WWW",
            "W....W...W...W....WW",
            "W.W          .WW.WWW",
            "W........P.........W",
            "W.W          .WW.WWW",
            "W..................W",
            "WWWWWWWWWWWWWWWWWWWW",
        ]

        for row_index, row in enumerate(layout):
            for col_index, tile in enumerate(row):
                x, y = col_index * 32, row_index * 32
                if tile == "W":
                    wall = Wall(x, y, self.assets)
                    self.walls.add(wall)
                    self.all_sprites.add(wall)
                elif tile == ".":
                    dot = Dot(x, y, self.assets)
                    self.dots.add(dot)
                    self.all_sprites.add(dot)
                elif tile == "P":
                    if not hasattr(self, 'player'):
                        self.player = Player(x, y, self.assets)
                        self.all_sprites.add(self.player)

        # Só cria fantasma se ainda não foi criado
        if not hasattr(self, 'ghost'):
            self.ghost = Ghost(32, 32, self.assets)
            self.ghosts.add(self.ghost)
            self.all_sprites.add(self.ghost)

    def draw_score(self):
        text = self.font.render(f"Pontos: {self.score}", True, (255, 255, 0))
        self.screen.blit(text, (10, HEIGHT - 30))

    def run(self):
        running = True
        while running:
            self.screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.player.update(self.walls)
            self.ghosts.update(self.walls)

            self.score += len(pygame.sprite.spritecollide(self.player, self.dots, True))

            if pygame.sprite.spritecollide(self.player, self.ghosts, False):
                print("Game Over!")
                pygame.quit()
                sys.exit()

            self.all_sprites.draw(self.screen)
            self.draw_score()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
