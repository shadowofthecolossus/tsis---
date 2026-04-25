import pygame
import random

W = 400
H = 600

# basic sprite classes
class Player(pygame.sprite.Sprite):
    def __init__(self, color_setting):
        super().__init__()
        # ИСПОЛЬЗУЕМ СПРАЙТ
        self.image = pygame.image.load("Player.png").convert_alpha() 
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520) #
        self.shield = False
        
        # Если включен щит, добавим визуальный эффект (полупрозрачный круг вокруг машины)
        self.shield_surface = pygame.Surface((self.rect.width + 20, self.rect.height + 20), pygame.SRCALPHA)
        pygame.draw.ellipse(self.shield_surface, (0, 255, 255, 128), self.shield_surface.get_rect(), 3)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.shield:
            screen.blit(self.shield_surface, (self.rect.x - 10, self.rect.y - 10))

    def move(self, extra_speed):
        keys = pygame.key.get_pressed() #[cite: 3]
        if self.rect.left > 0 and keys[pygame.K_LEFT]: #[cite: 3]
            self.rect.move_ip(-5 - extra_speed, 0)
        if self.rect.right < W and keys[pygame.K_RIGHT]: #[cite: 3]
            self.rect.move_ip(5 + extra_speed, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, diff_mult):
        super().__init__()
        # ИСПОЛЬЗУЕМ СПРАЙТ[cite: 3]
        self.image = pygame.image.load("Enemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        # random lane
        self.rect.center = (random.randint(40, W-40), -100) #[cite: 3]
        self.diff_mult = diff_mult

    def move(self, speed):
        self.rect.move_ip(0, speed * self.diff_mult) #[cite: 3]
        if self.rect.top > H:
            self.kill()

# Для монет, препятствий и бонусов оставил рисование, 
# так как в твоем списке файлов для них картинок нет.
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = random.choice([1, 2, 3])
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        c = (255, 255, 0) if self.weight == 1 else ((0, 255, 0) if self.weight == 2 else (0, 255, 255))
        pygame.draw.circle(self.image, c, (10, 10), 10)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, W-40), -50)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > H:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 20))
        self.image.fill((50, 50, 50)) # grey obstacle
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, W-40), -50)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > H:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(["nitro", "shield", "repair"])
        self.image = pygame.Surface((25, 25))
        c = (255, 100, 0) if self.type == "nitro" else ((200, 200, 255) if self.type == "shield" else (255, 100, 255))
        self.image.fill(c)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, W-40), -50)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > H:
            self.kill()