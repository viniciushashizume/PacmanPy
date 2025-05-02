import pygame
import random
import sys
from pygame import time

# Inicialização do pygame
pygame.init()

# Configurações de tela
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)  # Cor dos fantasmas quando vulneráveis

# FPS
clock = pygame.time.Clock()
FPS = 60

# Carregando sprites
pacman_spritesheet = pygame.image.load("PacMan.png").convert_alpha()
ghost_spritesheet = pygame.image.load("PacMan.png").convert_alpha()
dot_img = pygame.image.load("dot.png").convert_alpha()
power_dot_img = pygame.Surface((12, 12), pygame.SRCALPHA)  # Criando power dot
pygame.draw.circle(power_dot_img, WHITE, (6, 6), 6)  # Dot branco maior
wall_img = pygame.image.load("wall.png").convert_alpha()

# Redimensionar (mantendo proporções para spritesheets)
wall_img = pygame.transform.scale(wall_img, (32, 32))
dot_img = pygame.transform.scale(dot_img, (8, 8))

# Mapa simples: W = parede, . = ponto, ' ' = caminho, O = power dot
map_layout = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W........WW........W",
    "W.WWWW.WW.WW.WWWW.WW",
    "W. ............O...W",
    "W.WW.WWWWWWWW.WW.WWW",
    "W....W...W...W....WW",
    "WWWW.WW.WW.WW.WWWW.W",
    "W........P.........W",
    "W.WW.        ....WWW",
    "W.O....OOO.....O...W",
    "WWWWWWWWWWWWWWWWWWWW",
]

TILE_SIZE = 32

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Configuração do spritesheet do Pac-Man
        self.spritesheet = pacman_spritesheet
        self.frame_width = 16
        self.frame_height = 16
        self.frames = self.load_frames()
        self.current_frame = 0
        self.animation_speed = 0.2
        self.animation_counter = 0
        
        self.direction = 'right'  # Direção inicial
        self.image = self.frames[self.direction][self.current_frame]
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2
        self.power_time = 0  # Tempo restante do power-up
        
    def load_frames(self):
        # Carrega os frames do spritesheet (128x16)
        frames = {
            'right': [],
            'left': [],
            'up': [],
            'down': []
        }
        
        # Extrai frames do spritesheet (8 frames de 16x16)
        for i in range(8):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.spritesheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
            
            # Frame original (direita)
            frames['right'].append(frame)
            
            # Frame esquerda (flip horizontal)
            left_frame = pygame.transform.flip(frame, True, False)
            frames['left'].append(left_frame)
            
            # Frame para cima (rotação 90 graus)
            up_frame = pygame.transform.rotate(frame, 90)
            frames['up'].append(up_frame)
            
            # Frame para baixo (rotação 270 graus)
            down_frame = pygame.transform.rotate(frame, 270)
            frames['down'].append(down_frame)
            
        return frames
    
    def update(self, walls):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        new_direction = self.direction
        
        if keys[pygame.K_LEFT]:
            dx = -self.speed
            new_direction = 'left'
        elif keys[pygame.K_RIGHT]:
            dx = self.speed
            new_direction = 'right'
        elif keys[pygame.K_UP]:
            dy = -self.speed
            new_direction = 'up'
        elif keys[pygame.K_DOWN]:
            dy = self.speed
            new_direction = 'down'
            
        # Atualiza a direção se mudou
        if new_direction != self.direction:
            self.direction = new_direction
            self.current_frame = 0  # Reseta a animação ao mudar de direção
            
        # Animação
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames[self.direction])
            self.image = pygame.transform.scale(self.frames[self.direction][self.current_frame], (32, 32))
            
        # Movimento e colisão
        self.rect.x += dx
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x -= dx
            
        self.rect.y += dy
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.y -= dy
            
        # Atualiza tempo do power-up
        if self.power_time > 0:
            self.power_time -= 1

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_path=None, color='red'):
        super().__init__()
        # Carrega o spritesheet personalizado ou o padrão
        if sprite_path:
            self.spritesheet = pygame.image.load(sprite_path).convert_alpha()
        else:
            self.spritesheet = ghost_spritesheet
            
        self.frame_width = 16
        self.frame_height = 16
        self.frames = self.load_frames()
        self.current_frame = 0
        self.animation_speed = 0.15
        self.animation_counter = 0
        
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.image = self.frames[self.current_frame]
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 1
        self.color = color
        self.vulnerable = False
        self.normal_image = None
        self.vulnerable_image = None
        self.create_images()
        
    def create_images(self):
        # Cria imagens normal e vulnerável
        frame = self.frames[0]  # Usamos o primeiro frame como base
        self.normal_image = pygame.transform.scale(frame, (32, 32))
        
        # Cria imagem vulnerável (fantasma azul piscando)
        vulnerable_frame = frame.copy()
        vulnerable_frame.fill(BLUE, special_flags=pygame.BLEND_MULT)
        self.vulnerable_image = pygame.transform.scale(vulnerable_frame, (32, 32))
        
    def load_frames(self):
        # Carrega os frames do spritesheet (128x16)
        frames = []
        
        # Extrai frames do spritesheet (8 frames de 16x16)
        for i in range(8):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.spritesheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
            frames.append(frame)
            
        return frames
    
    def update(self, walls, player=None):
        # Comportamento base (aleatório)
        directions = ['left', 'right', 'up', 'down']
        dx = dy = 0
        
        if self.direction == 'left':
            dx = -self.speed
        elif self.direction == 'right':
            dx = self.speed
        elif self.direction == 'up':
            dy = -self.speed
        elif self.direction == 'down':
            dy = self.speed
            
        # Animação
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            
            # Alterna entre imagem normal e vulnerável se estiver vulnerável
            if self.vulnerable:
                if (pygame.time.get_ticks() // 200) % 2 == 0:  # Pisca a cada 200ms
                    self.image = self.vulnerable_image
                else:
                    self.image = self.normal_image
            else:
                self.image = pygame.transform.scale(self.frames[self.current_frame], (32, 32))
            
        # Movimento
        self.rect.x += dx
        self.rect.y += dy
        
        # Colisão e mudança de direção
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x -= dx
            self.rect.y -= dy
            self.direction = random.choice(directions)

class Blinky(Ghost):
    """O fantasma vermelho (perseguidor agressivo)"""
    def __init__(self, x, y, sprite_path=None):
        super().__init__(x, y, sprite_path, 'red')
        self.speed = 1.5  # Mais rápido que os outros
        
    def update(self, walls, player):
        # Blinky persegue diretamente o Pac-Man
        if player and not self.vulnerable:
            # Calcula a direção para o jogador
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            
            # Escolhe a direção predominante
            if abs(dx) > abs(dy):
                self.direction = 'right' if dx > 0 else 'left'
            else:
                self.direction = 'down' if dy > 0 else 'up'
        
        super().update(walls, player)

class Pinky(Ghost):
    """O fantasma rosa (emboscada)"""
    def __init__(self, x, y, sprite_path=None):
        super().__init__(x, y, sprite_path, 'pink')
        self.speed = 1.2
        
    def update(self, walls, player):
        # Pinky tenta se posicionar à frente do Pac-Man
        if player and not self.vulnerable:
            # Prever a posição à frente do Pac-Man
            if player.direction == 'right':
                target_x = player.rect.centerx + 4 * TILE_SIZE
                target_y = player.rect.centery
            elif player.direction == 'left':
                target_x = player.rect.centerx - 4 * TILE_SIZE
                target_y = player.rect.centery
            elif player.direction == 'up':
                target_x = player.rect.centerx
                target_y = player.rect.centery - 4 * TILE_SIZE
            else:  # down
                target_x = player.rect.centerx
                target_y = player.rect.centery + 4 * TILE_SIZE
                
            # Move-se em direção ao alvo previsto
            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            
            if abs(dx) > abs(dy):
                self.direction = 'right' if dx > 0 else 'left'
            else:
                self.direction = 'down' if dy > 0 else 'up'
        
        super().update(walls, player)

class Inky(Ghost):
    """O fantasma ciano (imprevisível)"""
    def __init__(self, x, y, sprite_path=None):
        super().__init__(x, y, sprite_path, 'cyan')
        self.speed = 1.1
        self.change_direction_counter = 0
        
    def update(self, walls, player):
        # Inky tem um comportamento mais imprevisível
        self.change_direction_counter += 1
        
        if self.change_direction_counter >= 60:  # Muda de direção a cada segundo
            self.change_direction_counter = 0
            if random.random() < 0.3:  # 30% de chance de mudar de direção
                self.direction = random.choice(['left', 'right', 'up', 'down'])
        
        super().update(walls, player)

class Clyde(Ghost):
    """O fantasma laranja (aleatório/com medo)"""
    def __init__(self, x, y, sprite_path=None):
        super().__init__(x, y, sprite_path, 'orange')
        self.speed = 0.9  # Mais lento
        
    def update(self, walls, player):
        # Clyde foge quando o Pac-Man está perto
        if player and not self.vulnerable:
            # Calcula a distância para o Pac-Man
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            distance = (dx**2 + dy**2)**0.5
            
            if distance < 8 * TILE_SIZE:  # Se estiver muito perto, foge
                self.direction = 'left' if dx > 0 else 'right'
                if abs(dy) > abs(dx):
                    self.direction = 'up' if dy > 0 else 'down'
        
        super().update(walls, player)

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = wall_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = dot_img
        self.rect = self.image.get_rect()
        self.rect.center = (x + TILE_SIZE // 2, y + TILE_SIZE // 2)

class PowerDot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = power_dot_img
        self.rect = self.image.get_rect()
        self.rect.center = (x + TILE_SIZE // 2, y + TILE_SIZE // 2)

# Grupos de sprites
walls = pygame.sprite.Group()
dots = pygame.sprite.Group()
power_dots = pygame.sprite.Group()
ghosts = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Criar mapa
player = None
for row_index, row in enumerate(map_layout):
    for col_index, tile in enumerate(row):
        x = col_index * TILE_SIZE
        y = row_index * TILE_SIZE
        if tile == "W":
            wall = Wall(x, y)
            walls.add(wall)
            all_sprites.add(wall)
        elif tile == ".":
            dot = Dot(x, y)
            dots.add(dot)
            all_sprites.add(dot)
        elif tile == "O":
            power_dot = PowerDot(x, y)
            power_dots.add(power_dot)
            all_sprites.add(power_dot)
        elif tile == "P":
            player = Player(x, y)
            all_sprites.add(player)

# Criar fantasmas com sprites personalizados (se quiser)
# Substitua None pelo caminho para um arquivo de sprite personalizado
blinky = Blinky(32, 32, sprite_path="Blinky.png")  # sprite_path="blinky.png"
pinky = Pinky(96, 32, sprite_path="Pinky.png")    # sprite_path="pinky.png"
inky = Inky(160, 32, sprite_path="Inky.png")     # sprite_path="inky.png"
clyde = Clyde(224, 32, sprite_path="Clyde.png")   # sprite_path="clyde.png"

ghosts.add(blinky, pinky, inky, clyde)
all_sprites.add(blinky, pinky, inky, clyde)

# Pontuação
score = 0
font = pygame.font.SysFont(None, 30)

# Loop principal
running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(walls)
    for ghost in ghosts:
        ghost.update(walls, player)

    # Comer pontos normais
    eaten_dots = pygame.sprite.spritecollide(player, dots, True)
    score += len(eaten_dots)

    # Comer power dots
    eaten_power_dots = pygame.sprite.spritecollide(player, power_dots, True)
    for _ in eaten_power_dots:
        score += 10  # Pontos extras por pegar o power dot
        player.power_time = 300  # 5 segundos de power-up (60 FPS * 5)
        
        # Tornar todos os fantasmas vulneráveis
        for ghost in ghosts:
            ghost.vulnerable = True
            ghost.image = ghost.vulnerable_image

    # Verifica colisão com fantasmas
    ghost_collisions = pygame.sprite.spritecollide(player, ghosts, False)
    for ghost in ghost_collisions:
        if player.power_time > 0 and ghost.vulnerable:
            # Pac-Man come o fantasma
            ghost.kill()
            score += 50  # Pontos extras por comer fantasma
        else:
            # Game Over
            print("Game Over! Pontuação:", score)
            pygame.quit()
            sys.exit()

    # Verifica se o power-up acabou
    if player.power_time <= 0:
        for ghost in ghosts:
            ghost.vulnerable = False
            ghost.image = ghost.normal_image

    all_sprites.draw(screen)

    # Mostrar pontuação
    score_text = font.render(f"Pontos: {score}", True, (255, 255, 0))
    screen.blit(score_text, (10, HEIGHT - 30))

    # Mostrar tempo restante do power-up
    if player.power_time > 0:
        power_text = font.render(f"Power: {player.power_time//60}s", True, BLUE)
        screen.blit(power_text, (WIDTH - 120, HEIGHT - 30))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()