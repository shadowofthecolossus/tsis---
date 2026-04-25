import pygame
import random
from color_palette import *

WIDTH = 600 #
HEIGHT = 600 #[cite: 1]
CELL = 30 #[cite: 1]

class Point:
    def __init__(self, x, y):
        self.x = x #[cite: 1]
        self.y = y #[cite: 1]

class Snake:
    def __init__(self, color):
        # original starting points[cite: 1]
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13), Point(10, 14)] 
        self.dx = 1 #[cite: 1]
        self.dy = 0 #[cite: 1]
        self.color = color
        self.shield_active = False

    def move(self):
        for i in range(len(self.body) - 1, 0, -1): #[cite: 1]
            self.body[i].x = self.body[i - 1].x #[cite: 1]
            self.body[i].y = self.body[i - 1].y #[cite: 1]

        self.body[0].x += self.dx #[cite: 1]
        self.body[0].y += self.dy #[cite: 1]

    def draw(self, screen):
        head = self.body[0]
        # if shield is active, head is cyan
        h_color = colorCYAN if self.shield_active else colorRED 
        pygame.draw.rect(screen, h_color, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]: #[cite: 1]
            pygame.draw.rect(screen, self.color, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_wall_collision(self):
        head = self.body[0]
        if head.x >= WIDTH // CELL or head.x < 0 or head.y >= HEIGHT // CELL or head.y < 0:
            if self.shield_active:
                self.shield_active = False
                # bounce back
                head.x -= self.dx
                head.y -= self.dy
                return False
            return True
        return False

    def check_self_collision(self):
        head = self.body[0]
        for p in self.body[1:]:
            if head.x == p.x and head.y == p.y:
                if self.shield_active:
                    self.shield_active = False
                    return False
                return True
        return False

class Food:
    def __init__(self):
        self.pos = Point(9, 9) #[cite: 1]
        self.weight = random.choice([1, 2, 3])
        self.spawn_time = pygame.time.get_ticks()
        self.timer = random.randint(5000, 10000) # 5-10 secs

    def draw(self, screen):
        color = colorGREEN if self.weight == 1 else (colorYELLOW if self.weight == 2 else colorBLUE)
        pygame.draw.rect(screen, color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, snake_body, obstacles):
        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1) #[cite: 1]
            self.pos.y = random.randint(0, HEIGHT // CELL - 1) #[cite: 1]
            if not any(p.x == self.pos.x and p.y == self.pos.y for p in snake_body) and \
               not any(o.x == self.pos.x and o.y == self.pos.y for o in obstacles):
                break
        self.weight = random.choice([1, 2, 3])
        self.spawn_time = pygame.time.get_ticks()

class Poison:
    def __init__(self):
        self.pos = Point(-1, -1)
        self.active = False
    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, colorPURPLE, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

class PowerUp:
    def __init__(self):
        self.pos = Point(-1, -1)
        self.type = None # 'speed', 'slow', 'shield'
        self.active = False
        self.spawn_time = 0
    def draw(self, screen):
        if self.active:
            c = colorORANGE if self.type == 'speed' else (colorWHITE if self.type == 'shield' else colorGRAY)
            pygame.draw.circle(screen, c, (self.pos.x * CELL + CELL//2, self.pos.y * CELL + CELL//2), CELL//2)