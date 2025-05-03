import pygame
import random
import sys
from pygame import time

# Inicialização do pygame
pygame.init()

# Configurações de tela
WIDTH, HEIGHT = 800, 600  # Aumentado para caber o labirinto clássico
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Clássico")

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)  # Cor dos fantasmas quando vulneráveis
YELLOW = (255, 255, 0)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Tamanho do tile (reduzido para caber o labirinto grande)
TILE_SIZE = 16

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE-2, TILE_SIZE-2))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2
        self.direction = 'right'
        self.next_direction = None
        self.power_time = 0
        
    def update(self, walls):
        # First try to change to next direction if possible
        if self.next_direction:
            # Create a temporary sprite for collision testing
            temp_sprite = pygame.sprite.Sprite()
            temp_sprite.rect = self.rect.copy()
            
            if self.next_direction == 'left':
                temp_sprite.rect.x -= self.speed
            elif self.next_direction == 'right':
                temp_sprite.rect.x += self.speed
            elif self.next_direction == 'up':
                temp_sprite.rect.y -= self.speed
            elif self.next_direction == 'down':
                temp_sprite.rect.y += self.speed
                
            if not pygame.sprite.spritecollide(temp_sprite, walls, False):
                self.direction = self.next_direction
                self.next_direction = None
        
        # Movement based on current direction
        dx = dy = 0
        if self.direction == 'left':
            dx = -self.speed
        elif self.direction == 'right':
            dx = self.speed
        elif self.direction == 'up':
            dy = -self.speed
        elif self.direction == 'down':
            dy = self.speed
            
        # Horizontal movement
        old_x = self.rect.x
        self.rect.x += dx
        if self.check_collision(walls):
            self.rect.x = old_x
            
        # Vertical movement
        old_y = self.rect.y
        self.rect.y += dy
        if self.check_collision(walls):
            self.rect.y = old_y
            
        # Power-up timer
        if self.power_time > 0:
            self.power_time -= 1
            
        # Tunnel teleport
        if self.rect.right < 0:
            self.rect.left = WIDTH
        elif self.rect.left > WIDTH:
            self.rect.right = 0
    
    def check_collision(self, walls):
        # Create temporary sprite for collision detection
        temp_sprite = pygame.sprite.Sprite()
        temp_sprite.rect = self.rect.copy()
        return pygame.sprite.spritecollideany(temp_sprite, walls)

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 1
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.vulnerable = False
        self.target = None
        
    def update(self, walls, player=None):
        # Se vulnerável, muda para azul
        if self.vulnerable:
            if (pygame.time.get_ticks() // 200) % 2 == 0:  # Pisca
                self.image.fill(BLUE)
            else:
                self.image.fill(WHITE)
        else:
            self.image.fill(self.color)
            
        # Movimento baseado na direção atual
        dx = dy = 0
        if self.direction == 'left':
            dx = -self.speed
        elif self.direction == 'right':
            dx = self.speed
        elif self.direction == 'up':
            dy = -self.speed
        elif self.direction == 'down':
            dy = self.speed
            
        # Movimento horizontal
        old_x = self.rect.x
        self.rect.x += dx
        if self.check_collision(walls):
            self.rect.x = old_x
            self.change_direction(walls)
            
        # Movimento vertical
        old_y = self.rect.y
        self.rect.y += dy
        if self.check_collision(walls):
            self.rect.y = old_y
            self.change_direction(walls)
            
        # Teleporte nos túneis
        if self.rect.right < 0:
            self.rect.left = WIDTH
        elif self.rect.left > WIDTH:
            self.rect.right = 0
            
    def check_collision(self, walls):
        # Cria um sprite temporário para verificar colisão
        temp_sprite = pygame.sprite.Sprite()
        temp_sprite.rect = self.rect.copy()
        return pygame.sprite.spritecollideany(temp_sprite, walls)
            
    def change_direction(self, walls):
        # Escolhe uma nova direção que não cause colisão
        directions = ['left', 'right', 'up', 'down']
        random.shuffle(directions)  # Aleatoriza a ordem
        
        for new_dir in directions:
            if new_dir == self.direction:
                continue
                
            # Cria um sprite temporário para testar a nova posição
            temp_sprite = pygame.sprite.Sprite()
            temp_sprite.rect = self.rect.copy()
            
            if new_dir == 'left':
                temp_sprite.rect.x -= self.speed
            elif new_dir == 'right':
                temp_sprite.rect.x += self.speed
            elif new_dir == 'up':
                temp_sprite.rect.y -= self.speed
            elif new_dir == 'down':
                temp_sprite.rect.y += self.speed
                
            if not pygame.sprite.spritecollideany(temp_sprite, walls):
                self.direction = new_dir
                break

class Blinky(Ghost):
    """O fantasma vermelho (perseguidor agressivo)"""
    def __init__(self, x, y):
        super().__init__(x, y, (255, 0, 0))  # Vermelho
        self.speed = 1.5
        
    def update(self, walls, player):
        # Se não está vulnerável, persegue o jogador
        if not self.vulnerable and player:
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
    def __init__(self, x, y):
        super().__init__(x, y, (255, 184, 255))  # Rosa
        self.speed = 1.2
        
    def update(self, walls, player):
        # Se não está vulnerável, tenta se posicionar à frente do Pac-Man
        if not self.vulnerable and player:
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
    def __init__(self, x, y):
        super().__init__(x, y, (0, 255, 255))  # Ciano
        self.speed = 1.1
        self.change_direction_counter = 0
        
    def update(self, walls, player):
        # Comportamento mais imprevisível
        self.change_direction_counter += 1
        
        if self.change_direction_counter >= 60:  # Muda de direção a cada segundo
            self.change_direction_counter = 0
            if random.random() < 0.3:  # 30% de chance de mudar de direção
                self.direction = random.choice(['left', 'right', 'up', 'down'])
        
        super().update(walls, player)

class Clyde(Ghost):
    """O fantasma laranja (aleatório/com medo)"""
    def __init__(self, x, y):
        super().__init__(x, y, (255, 184, 82))  # Laranja
        self.speed = 0.9
        
    def update(self, walls, player):
        # Clyde foge quando o Pac-Man está perto
        if not self.vulnerable and player:
            # Calcula a distância para o Pac-Man
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            distance = (dx**2 + dy**2)**0.5
            
            if distance < 8 * TILE_SIZE:  # Se estiver muito perto, foge
                self.direction = 'left' if dx > 0 else 'right'
                if abs(dy) > abs(dx):
                    self.direction = 'up' if dy > 0 else 'down'
            else:
                # Comportamento aleatório
                if random.random() < 0.02:  # 2% de chance de mudar de direção
                    self.direction = random.choice(['left', 'right', 'up', 'down'])
        
        super().update(walls, player)

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((0, 0, 255))  # Azul para paredes
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x + TILE_SIZE // 2, y + TILE_SIZE // 2)

class PowerDot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x + TILE_SIZE // 2, y + TILE_SIZE // 2)

# Criar o labirinto clássico do Pac-Man
def create_classic_maze():
    # 1 = parede, 0 = caminho, 2 = ponto, 3 = power dot
    maze_grid = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
        [1, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
        [1, 3, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 3, 1],
        [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
        [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
        [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    
    walls = pygame.sprite.Group()
    dots = pygame.sprite.Group()
    power_dots = pygame.sprite.Group()
    player = None
    
    for row in range(len(maze_grid)):
        for col in range(len(maze_grid[0])):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            
            if maze_grid[row][col] == 1:  # Parede
                walls.add(Wall(x, y))
            elif maze_grid[row][col] == 2:  # Ponto
                dots.add(Dot(x, y))
            elif maze_grid[row][col] == 3:  # Power dot
                power_dots.add(PowerDot(x, y))
            elif maze_grid[row][col] == 0 and row == 14:  # Túnel de teleporte
                pass  # Nada a adicionar, é caminho vazio
            elif maze_grid[row][col] == 0 and row == 23 and (col == 13 or col == 14):  # Covil dos fantasmas
                pass  # Área dos fantasmas
    
    # Posição inicial do Pac-Man (centro do labirinto)
    player = Player(14 * TILE_SIZE, 23 * TILE_SIZE)
    
    return walls, dots, power_dots, player

# Criar o jogo
walls, dots, power_dots, player = create_classic_maze()
all_sprites = pygame.sprite.Group(walls, dots, power_dots, player)

# Criar fantasmas
ghosts = pygame.sprite.Group()
blinky = Blinky(14 * TILE_SIZE, 11 * TILE_SIZE)  # Blinky (vermelho)
pinky = Pinky(13 * TILE_SIZE, 14 * TILE_SIZE)    # Pinky (rosa)
inky = Inky(14 * TILE_SIZE, 14 * TILE_SIZE)      # Inky (ciano)
clyde = Clyde(15 * TILE_SIZE, 14 * TILE_SIZE)    # Clyde (laranja)

ghosts.add(blinky, pinky, inky, clyde)
all_sprites.add(ghosts)

# Pontuação
score = 0
font = pygame.font.SysFont(None, 36)

# Texto de início
start_font = pygame.font.SysFont(None, 48)
start_text = start_font.render("PRESSIONE ESPAÇO PARA COMEÇAR", True, WHITE)
start_rect = start_text.get_rect(center=(WIDTH//2, HEIGHT//2))

# Estado do jogo
game_started = False
game_over = False
game_win = False

# Loop principal
running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_started:
                game_started = True
                
            if game_started and not game_over:
                if event.key == pygame.K_LEFT:
                    player.next_direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    player.next_direction = 'right'
                elif event.key == pygame.K_UP:
                    player.next_direction = 'up'
                elif event.key == pygame.K_DOWN:
                    player.next_direction = 'down'
    
    if game_started and not game_over and not game_win:
        player.update(walls)
        
        # Atualizar fantasmas
        for ghost in ghosts:
            ghost.update(walls, player)
        
        # Comer pontos normais
        eaten_dots = pygame.sprite.spritecollide(player, dots, True)
        score += len(eaten_dots)
        
        # Comer power dots
        eaten_power_dots = pygame.sprite.spritecollide(player, power_dots, True)
        for _ in eaten_power_dots:
            score += 50  # Pontos extras por pegar o power dot
            player.power_time = 300  # 5 segundos de power-up (60 FPS * 5)
            
            # Tornar todos os fantasmas vulneráveis
            for ghost in ghosts:
                ghost.vulnerable = True
        
        # Verifica colisão com fantasmas
        ghost_collisions = pygame.sprite.spritecollide(player, ghosts, False)
        for ghost in ghost_collisions:
            if player.power_time > 0 and ghost.vulnerable:
                # Pac-Man come o fantasma
                ghost.kill()
                score += 200  # Pontos extras por comer fantasma
            else:
                # Game Over
                game_over = True
        
        # Verifica se o power-up acabou
        if player.power_time <= 0:
            for ghost in ghosts:
                ghost.vulnerable = False
        
        # Verifica vitória (todos os pontos comidos)
        if len(dots) == 0 and len(power_dots) == 0:
            game_win = True
    
    # Desenhar tudo
    all_sprites.draw(screen)
    
    # Mostrar pontuação
    score_text = font.render(f"Pontos: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Mostrar tempo restante do power-up
    if player.power_time > 0:
        power_text = font.render(f"Power: {player.power_time//60}s", True, BLUE)
        screen.blit(power_text, (WIDTH - 150, 10))
    
    # Tela de início
    if not game_started:
        screen.blit(start_text, start_rect)
    
    # Tela de game over
    if game_over:
        over_text = start_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(over_text, over_text.get_rect(center=(WIDTH//2, HEIGHT//2)))
    
    # Tela de vitória
    if game_win:
        win_text = start_font.render("VOCÊ VENCEU!", True, (0, 255, 0))
        screen.blit(win_text, win_text.get_rect(center=(WIDTH//2, HEIGHT//2)))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()