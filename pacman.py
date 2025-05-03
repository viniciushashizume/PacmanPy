import pygame
import random
import math
from collections import deque
import heapq

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 608, 672
GRID_SIZE = 16
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 184, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 184, 82)
GRAY = (40, 40, 40)

# Estados do jogo
MENU = 0
PLAYING = 1
GAME_OVER = 2
WIN = 3

# Direções
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Maze:
    def __init__(self):
        self.grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
            [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
            [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.pellets = [[1 for _ in row] for row in self.grid]
        self.power_pellets = [(1, 3), (1, 33), (21, 3), (21, 33)]
        self.reset_pellets()
        
    def reset_pellets(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 0:
                    self.pellets[i][j] = 1
                else:
                    self.pellets[i][j] = 0
        
        for i, j in self.power_pellets:
            self.pellets[i][j] = 2
    
    def draw(self, screen):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1:
                    pygame.draw.rect(screen, BLUE, (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
        
        for i in range(len(self.pellets)):
            for j in range(len(self.pellets[i])):
                if self.pellets[i][j] == 1:
                    pygame.draw.circle(screen, WHITE, 
                                     (j * GRID_SIZE + GRID_SIZE // 2, i * GRID_SIZE + GRID_SIZE // 2), 
                                     2)
                elif self.pellets[i][j] == 2:
                    pygame.draw.circle(screen, WHITE, 
                                     (j * GRID_SIZE + GRID_SIZE // 2, i * GRID_SIZE + GRID_SIZE // 2), 
                                     5)
    
    def is_wall(self, x, y):
        if 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid):
            return self.grid[y][x] == 1
        return True
    
    def eat_pellet(self, x, y):
        if 0 <= x < len(self.pellets[0]) and 0 <= y < len(self.pellets):
            if self.pellets[y][x] > 0:
                value = self.pellets[y][x]
                self.pellets[y][x] = 0
                return value
        return 0
    
    def has_pellets_left(self):
        for row in self.pellets:
            if 1 in row or 2 in row:
                return True
        return False

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.speed = 2
        self.radius = GRID_SIZE // 2 - 2
        self.mouth_angle = 0
        self.mouth_opening = True
        self.lives = 3
        self.score = 0
        self.powered_up = False
        self.power_timer = 0
    
    def update(self, maze):
        # Mudança de direção
        new_x = self.x + self.next_direction[0] * self.speed / 2
        new_y = self.y + self.next_direction[1] * self.speed / 2
        
        if not maze.is_wall(int(new_x), int(new_y)):
            self.direction = self.next_direction
        
        # Movimento
        new_x = self.x + self.direction[0] * self.speed / 2
        new_y = self.y + self.direction[1] * self.speed / 2
        
        if not maze.is_wall(int(new_x), int(new_y)):
            self.x = new_x
            self.y = new_y
        
        # Animação da boca
        if self.mouth_opening:
            self.mouth_angle += 0.1
            if self.mouth_angle >= 0.4:
                self.mouth_opening = False
        else:
            self.mouth_angle -= 0.1
            if self.mouth_angle <= 0:
                self.mouth_opening = True
        
        # Comer pellets
        cell_x, cell_y = int(self.x), int(self.y)
        pellet_value = maze.eat_pellet(cell_x, cell_y)
        
        if pellet_value == 1:
            self.score += 10
        elif pellet_value == 2:
            self.score += 50
            self.powered_up = True
            self.power_timer = 600  # 10 segundos a 60 FPS
        
        # Atualizar estado de power-up
        if self.powered_up:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.powered_up = False
    
    def draw(self, screen):
        # Desenhar Pac-Man
        angle = 0
        if self.direction == RIGHT:
            angle = 0
        elif self.direction == DOWN:
            angle = 90
        elif self.direction == LEFT:
            angle = 180
        elif self.direction == UP:
            angle = 270
        
        start_angle = angle + math.degrees(self.mouth_angle)
        end_angle = angle - math.degrees(self.mouth_angle)
        
        pygame.draw.arc(screen, YELLOW, 
                       (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                       math.radians(start_angle), math.radians(end_angle), self.radius)
        
        # Preencher o Pac-Man (simplificado)
        center = (int(self.x * GRID_SIZE + GRID_SIZE // 2), int(self.y * GRID_SIZE + GRID_SIZE // 2))
        pygame.draw.circle(screen, YELLOW, center, self.radius)
        
        # Desenhar olho
        eye_offset_x = 0
        eye_offset_y = 0
        
        if self.direction == RIGHT:
            eye_offset_x = 3
        elif self.direction == DOWN:
            eye_offset_y = 3
        elif self.direction == LEFT:
            eye_offset_x = -3
        elif self.direction == UP:
            eye_offset_y = -3
        
        pygame.draw.circle(screen, BLACK, 
                          (center[0] + eye_offset_x, center[1] + eye_offset_y), 
                          self.radius // 3)
    
    def set_direction(self, direction):
        self.next_direction = direction
    
    def get_position(self):
        return (self.x, self.y)
    
    def reset(self, x, y):
        self.x = x
        self.y = y
        self.direction = (0, 0)
        self.next_direction = (0, 0)

class Ghost:
    def __init__(self, x, y, color, name):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.direction = (0, 0)
        self.speed = 1
        self.radius = GRID_SIZE // 2 - 2
        self.target = (0, 0)
        self.frightened = False
        self.frightened_timer = 0
        self.home = (x, y)
        self.state = "chase"  # "chase", "scatter", "frightened", "eaten"
        self.scatter_target = (0, 0)
        self.set_scatter_target()
    
    def set_scatter_target(self):
        if self.name == "Blinky":
            self.scatter_target = (35, 0)
        elif self.name == "Pinky":
            self.scatter_target = (0, 0)
        elif self.name == "Inky":
            self.scatter_target = (35, 21)
        elif self.name == "Clyde":
            self.scatter_target = (0, 21)
    
    def update(self, maze, pacman, ghosts):
        if self.state == "frightened":
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.state = "chase"
                self.frightened = False
        
        # Máquina de estados do fantasma
        if self.state != "eaten":
            # Mudança entre perseguição e dispersão
            if self.state in ["chase", "scatter"]:
                if random.random() < 0.005:  # Pequena chance de mudar de estado
                    if self.state == "chase":
                        self.state = "scatter"
                    else:
                        self.state = "chase"
        
        # Definir alvo com base no estado
        if self.state == "chase":
            self.set_target(pacman, ghosts)
        elif self.state == "scatter":
            self.target = self.scatter_target
        elif self.state == "frightened":
            # Movimento aleatório quando assustado
            if random.random() < 0.2 or self.direction == (0, 0):
                self.random_direction(maze)
        elif self.state == "eaten":
            # Voltar para casa quando comido
            if (int(self.x), int(self.y)) == self.home:
                self.state = "chase"
            else:
                self.target = self.home
        
        # Movimento
        if self.state != "frightened":
            self.move_towards_target(maze)
        
        # Verificar se está em um túnel
        if self.y == 9 and (self.x < 1 or self.x > 34):
            if self.x < 1:
                self.x = 35
            else:
                self.x = 0
    
    def set_target(self, pacman, ghosts):
        pac_x, pac_y = pacman.get_position()
        
        if self.name == "Blinky":
            # Persegue diretamente o Pac-Man
            self.target = (pac_x, pac_y)
            
            # Aumenta a velocidade após muitos pellets serem comidos
            if pacman.score > 1000:
                self.speed = 1.5
            else:
                self.speed = 1
        
        elif self.name == "Pinky":
            # Tenta ficar à frente do Pac-Man
            if pacman.direction == UP:
                self.target = (pac_x - 4, pac_y - 4)
            elif pacman.direction == DOWN:
                self.target = (pac_x, pac_y + 4)
            elif pacman.direction == LEFT:
                self.target = (pac_x - 4, pac_y)
            elif pacman.direction == RIGHT:
                self.target = (pac_x + 4, pac_y)
            else:
                self.target = (pac_x + 2, pac_y)
        
        elif self.name == "Inky":
            # Move-se de forma imprevisível, usando Blinky como referência
            blinky = next((g for g in ghosts if g.name == "Blinky"), None)
            if blinky:
                blinky_x, blinky_y = blinky.x, blinky.y
                # Ponto intermediário entre Blinky e o alvo de Pinky
                target_x = pac_x + (pac_x - blinky_x)
                target_y = pac_y + (pac_y - blinky_y)
                self.target = (target_x, target_y)
            else:
                self.target = (pac_x, pac_y)
        
        elif self.name == "Clyde":
            # Persegue como Blinky, mas vai para o canto quando perto
            distance = math.sqrt((pac_x - self.x)**2 + (pac_y - self.y)**2)
            if distance > 8:
                self.target = (pac_x, pac_y)
            else:
                self.target = self.scatter_target
    
    def move_towards_target(self, maze):
        # Encontrar a melhor direção usando A* ou busca gulosa
        if random.random() < 0.1 or self.direction == (0, 0):
            path = self.a_star_search(maze, (int(self.x), int(self.y)), 
                                    (int(self.target[0]), int(self.target[1])))
            
            if path and len(path) > 1:
                next_pos = path[1]
                self.direction = (next_pos[0] - int(self.x), next_pos[1] - int(self.y))
        
        # Movimento
        new_x = self.x + self.direction[0] * self.speed / 2
        new_y = self.y + self.direction[1] * self.speed / 2
        
        if not maze.is_wall(int(new_x), int(new_y)):
            self.x = new_x
            self.y = new_y
        else:
            # Se bateu em uma parede, tenta outra direção
            possible_directions = [UP, DOWN, LEFT, RIGHT]
            random.shuffle(possible_directions)
            
            for direction in possible_directions:
                new_x = self.x + direction[0] * self.speed / 2
                new_y = self.y + direction[1] * self.speed / 2
                
                if not maze.is_wall(int(new_x), int(new_y)):
                    self.direction = direction
                    self.x = new_x
                    self.y = new_y
                    break
    
    def random_direction(self, maze):
        possible_directions = [UP, DOWN, LEFT, RIGHT]
        random.shuffle(possible_directions)
        
        for direction in possible_directions:
            new_x = self.x + direction[0] * self.speed / 2
            new_y = self.y + direction[1] * self.speed / 2
            
            if not maze.is_wall(int(new_x), int(new_y)):
                self.direction = direction
                break
    
    def a_star_search(self, maze, start, goal):
        """Algoritmo A* para encontrar o caminho até o alvo"""
        def heuristic(a, b):
            # Distância de Manhattan
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        
        while frontier:
            current = heapq.heappop(frontier)[1]
            
            if current == goal:
                break
            
            for dx, dy in [UP, DOWN, LEFT, RIGHT]:
                next_pos = (current[0] + dx, current[1] + dy)
                
                if maze.is_wall(next_pos[0], next_pos[1]):
                    continue
                
                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + heuristic(goal, next_pos)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current
        
        # Reconstruir o caminho
        path = []
        if goal in came_from:
            current = goal
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
        
        return path
    
    def greedy_search(self, maze, start, goal):
        """Busca gulosa usando apenas a heurística"""
        def heuristic(a, b):
            # Distância de Manhattan
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        frontier = []
        heapq.heappush(frontier, (heuristic(start, goal), start))
        came_from = {}
        came_from[start] = None
        
        while frontier:
            current = heapq.heappop(frontier)[1]
            
            if current == goal:
                break
            
            for dx, dy in [UP, DOWN, LEFT, RIGHT]:
                next_pos = (current[0] + dx, current[1] + dy)
                
                if maze.is_wall(next_pos[0], next_pos[1]):
                    continue
                
                if next_pos not in came_from:
                    priority = heuristic(goal, next_pos)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current
        
        # Reconstruir o caminho
        path = []
        if goal in came_from:
            current = goal
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
        
        return path
    
    def draw(self, screen):
        # Desenhar fantasma
        body_rect = pygame.Rect(self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        
        if self.frightened:
            color = BLUE
        elif self.state == "eaten":
            color = GRAY
        else:
            color = self.color
        
        pygame.draw.rect(screen, color, body_rect, border_radius=self.radius)
        
        # Desenhar olhos (exceto quando comido)
        if self.state != "eaten":
            left_eye = (int(self.x * GRID_SIZE + GRID_SIZE // 3), 
                       int(self.y * GRID_SIZE + GRID_SIZE // 3))
            right_eye = (int(self.x * GRID_SIZE + 2 * GRID_SIZE // 3), 
                        int(self.y * GRID_SIZE + GRID_SIZE // 3))
            
            pygame.draw.circle(screen, WHITE, left_eye, self.radius // 3)
            pygame.draw.circle(screen, WHITE, right_eye, self.radius // 3)
            
            # Desenhar pupilas (direção do movimento)
            pupil_offset = self.radius // 6
            left_pupil = (left_eye[0] + self.direction[0] * pupil_offset, 
                         left_eye[1] + self.direction[1] * pupil_offset)
            right_pupil = (right_eye[0] + self.direction[0] * pupil_offset, 
                          right_eye[1] + self.direction[1] * pupil_offset)
            
            pygame.draw.circle(screen, BLACK, left_pupil, self.radius // 6)
            pygame.draw.circle(screen, BLACK, right_pupil, self.radius // 6)
        
        # Desenhar "pernas" onduladas
        if not self.frightened and self.state != "eaten":
            for i in range(3):
                start_x = self.x * GRID_SIZE + i * GRID_SIZE // 3
                end_x = start_x + GRID_SIZE // 3
                wave_y = self.y * GRID_SIZE + GRID_SIZE + math.sin(pygame.time.get_ticks() / 200 + i) * 2 - 2
                
                pygame.draw.line(screen, color, 
                                (start_x, wave_y), 
                                (end_x, wave_y), 2)
    
    def frighten(self):
        self.frightened = True
        self.state = "frightened"
        self.frightened_timer = 600  # 10 segundos a 60 FPS
        self.speed = 0.5
    
    def eat(self):
        self.state = "eaten"
        self.frightened = False
        self.speed = 2
    
    def reset(self, x, y):
        self.x = x
        self.y = y
        self.direction = (0, 0)
        self.frightened = False
        self.frightened_timer = 0
        self.state = "chase"

class Game:
    def __init__(self):
        self.maze = Maze()
        self.pacman = Pacman(18, 15)
        self.ghosts = [
            Ghost(18, 9, RED, "Blinky"),
            Ghost(16, 9, PINK, "Pinky"),
            Ghost(20, 9, CYAN, "Inky"),
            Ghost(18, 9, ORANGE, "Clyde")
        ]
        self.state = MENU
        self.font = pygame.font.SysFont("Arial", 24)
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.level = 1
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.state == MENU:
                    if event.key == pygame.K_RETURN:
                        self.state = PLAYING
                        self.reset_game()
                
                elif self.state == PLAYING:
                    if event.key == pygame.K_UP:
                        self.pacman.set_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.pacman.set_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.pacman.set_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.set_direction(RIGHT)
                
                elif self.state in [GAME_OVER, WIN]:
                    if event.key == pygame.K_RETURN:
                        self.state = MENU
        
        return True
    
    def update(self):
        if self.state == PLAYING:
            self.pacman.update(self.maze)
            
            for ghost in self.ghosts:
                ghost.update(self.maze, self.pacman, self.ghosts)
            
            # Verificar colisões com fantasmas
            pac_x, pac_y = self.pacman.get_position()
            
            for ghost in self.ghosts:
                ghost_x, ghost_y = ghost.x, ghost.y
                distance = math.sqrt((pac_x - ghost_x)**2 + (pac_y - ghost_y)**2)
                
                if distance < 0.8:  # Colisão
                    if ghost.frightened:
                        ghost.eat()
                        self.pacman.score += 200
                    elif ghost.state != "eaten":
                        self.pacman.lives -= 1
                        
                        if self.pacman.lives <= 0:
                            self.state = GAME_OVER
                        else:
                            self.reset_positions()
            
            # Verificar se comeu power pellet
            if self.pacman.powered_up:
                for ghost in self.ghosts:
                    if ghost.state != "eaten":
                        ghost.frighten()
            
            # Verificar vitória
            if not self.maze.has_pellets_left():
                self.state = WIN
                self.level += 1
    
    def draw(self):
        SCREEN.fill(BLACK)
        
        if self.state == MENU:
            title = self.font.render("PAC-MAN", True, YELLOW)
            start = self.font.render("Press ENTER to Start", True, WHITE)
            
            SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
            SCREEN.blit(start, (WIDTH // 2 - start.get_width() // 2, HEIGHT // 2))
            
            # Desenhar fantasmas pequenos para demonstração
            ghost_y = HEIGHT * 2 // 3
            ghost_spacing = WIDTH // 5
            
            for i, ghost in enumerate(self.ghosts):
                ghost_rect = pygame.Rect(i * ghost_spacing + ghost_spacing // 2 - 15, ghost_y, 30, 30)
                pygame.draw.rect(SCREEN, ghost.color, ghost_rect, border_radius=15)
                
                name = self.font.render(ghost.name, True, ghost.color)
                SCREEN.blit(name, (i * ghost_spacing + ghost_spacing // 2 - name.get_width() // 2, ghost_y + 40))
        
        elif self.state == PLAYING:
            self.maze.draw(SCREEN)
            self.pacman.draw(SCREEN)
            
            for ghost in self.ghosts:
                ghost.draw(SCREEN)
            
            # Desenhar pontuação e vidas
            score_text = self.font.render(f"Score: {self.pacman.score}", True, WHITE)
            lives_text = self.font.render(f"Lives: {self.pacman.lives}", True, WHITE)
            level_text = self.font.render(f"Level: {self.level}", True, WHITE)
            
            SCREEN.blit(score_text, (10, HEIGHT - 30))
            SCREEN.blit(lives_text, (WIDTH // 2 - lives_text.get_width() // 2, HEIGHT - 30))
            SCREEN.blit(level_text, (WIDTH - level_text.get_width() - 10, HEIGHT - 30))
        
        elif self.state == GAME_OVER:
            game_over = self.font.render("GAME OVER", True, RED)
            score = self.font.render(f"Final Score: {self.pacman.score}", True, WHITE)
            restart = self.font.render("Press ENTER to return to Menu", True, WHITE)
            
            SCREEN.blit(game_over, (WIDTH // 2 - game_over.get_width() // 2, HEIGHT // 3))
            SCREEN.blit(score, (WIDTH // 2 - score.get_width() // 2, HEIGHT // 2))
            SCREEN.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT * 2 // 3))
        
        elif self.state == WIN:
            win = self.font.render(f"LEVEL {self.level} COMPLETE!", True, YELLOW)
            score = self.font.render(f"Score: {self.pacman.score}", True, WHITE)
            next_level = self.font.render("Press ENTER for Next Level", True, WHITE)
            
            SCREEN.blit(win, (WIDTH // 2 - win.get_width() // 2, HEIGHT // 3))
            SCREEN.blit(score, (WIDTH // 2 - score.get_width() // 2, HEIGHT // 2))
            SCREEN.blit(next_level, (WIDTH // 2 - next_level.get_width() // 2, HEIGHT * 2 // 3))
        
        pygame.display.flip()
    
    def reset_game(self):
        self.maze.reset_pellets()
        self.pacman.reset(18, 15)
        self.pacman.score = 0
        self.pacman.lives = 3
        
        for i, ghost in enumerate(self.ghosts):
            ghost.reset(18 + i, 9)
    
    def reset_positions(self):
        self.pacman.reset(18, 15)
        
        for i, ghost in enumerate(self.ghosts):
            ghost.reset(18 + i, 9)
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()