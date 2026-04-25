import pygame
import sys
import random
import time
import persistence
import ui
import racer

# init
pygame.init() #[cite: 3]
pygame.mixer.init() # Инициализация звука
W, H = 400, 600
screen = pygame.display.set_mode((W, H)) #[cite: 3]
pygame.display.set_caption("SNAKE GAME") #[cite: 3]
clock = pygame.time.Clock() #[cite: 3]

# fonts
try:
    font = pygame.font.Font("retro.ttf", 40)
    small = pygame.font.Font("retro.ttf", 16) # Уменьшил для ретро-шрифта
except:
    font = pygame.font.SysFont("Verdana", 40) #[cite: 3]
    small = pygame.font.SysFont("Verdana", 20) #[cite: 3]

# Загрузка спрайта дороги[cite: 3]
bg = pygame.image.load("AnimatedStreet.png").convert() 

# Загрузка звуков[cite: 3]
try:
    crash_sound = pygame.mixer.Sound('crash.wav')
    pygame.mixer.music.load('background.wav')
    pygame.mixer.music.play(-1) # Зациклить фоновую музыку
except:
    print("Не найдены звуковые файлы")

# game state vars
state = "MENU"
username = ""
settings = persistence.load_settings()

# Управление звуком при старте
if not settings.get("sound", True):
    pygame.mixer.music.pause()

def reset_game():
    global P1, enemies, coins, obstacles, powerups, all_sprites
    global score, distance, base_speed, active_power, power_timer
    
    score = 0 #[cite: 3]
    distance = 0
    base_speed = 5 #[cite: 3]
    active_power = None
    power_timer = 0
    
    P1 = racer.Player(settings["color"]) #[cite: 3]
    enemies = pygame.sprite.Group() #[cite: 3]
    coins = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    
    all_sprites = pygame.sprite.Group() #[cite: 3]
    all_sprites.add(P1) #[cite: 3]

bg_y = 0
reset_game()

while True:
    for event in pygame.event.get(): #[cite: 3]
        if event.type == pygame.QUIT: #[cite: 3]
            pygame.quit() #[cite: 3]
            sys.exit() #[cite: 3]
            
        if state == "MENU":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(username) > 0:
                    reset_game()
                    state = "PLAY"
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_1:
                    state = "LEADERBOARD"
                elif event.key == pygame.K_2:
                    state = "SETTINGS"
                else:
                    if len(username) < 15 and event.unicode.isprintable():
                        username += event.unicode
                        
        elif state == "GAMEOVER":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    state = "MENU"
                    
        elif state == "SETTINGS":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    persistence.save_settings(settings)
                    state = "MENU"
                elif event.key == pygame.K_c:
                    settings["color"] = "red" if settings["color"] == "blue" else "blue"
                elif event.key == pygame.K_s:
                    settings["sound"] = not settings.get("sound", True)
                    if settings["sound"]:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                elif event.key == pygame.K_d:
                    settings["diff"] = "hard" if settings["diff"] == "normal" else "normal"
                    
        elif state == "LEADERBOARD":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = "MENU"

    screen.fill((0, 0, 0))

    if state == "MENU":
        ui.draw_text(screen, "RACER", W//2, 100, font, (0,255,0), True)
        ui.draw_text(screen, "NAME: " + username + "_", W//2, 250, small, center=True)
        ui.draw_text(screen, "ENTER TO PLAY", W//2, 300, small, (255,255,0), True)
        ui.draw_text(screen, "1: LEADERBOARD", W//2, 350, small, center=True)
        ui.draw_text(screen, "2: SETTINGS", W//2, 390, small, center=True)

    elif state == "SETTINGS":
        ui.draw_text(screen, "SETTINGS", W//2, 100, font, center=True)
        ui.draw_text(screen, "C: COLOR -> " + settings["color"].upper(), W//2, 250, small, center=True)
        ui.draw_text(screen, "D: DIFF -> " + settings["diff"].upper(), W//2, 300, small, center=True)
        sound_status = "ON" if settings.get("sound", True) else "OFF"
        ui.draw_text(screen, "S: SOUND -> " + sound_status, W//2, 350, small, center=True)
        ui.draw_text(screen, "ESC TO SAVE", W//2, 450, small, center=True)

    elif state == "LEADERBOARD":
        ui.draw_text(screen, "TOP 10", W//2, 50, font, center=True)
        lb = persistence.load_leaderboard()
        y = 120
        for i, row in enumerate(lb):
            ui.draw_text(screen, f"{i+1}. {row['name']} | S:{row['score']} | D:{row['dist']}", 20, y, small)
            y += 30
        ui.draw_text(screen, "ESC TO BACK", W//2, 500, small, center=True)

    elif state == "PLAY":
        # background scrolling[cite: 3]
        bg_y = (bg_y + base_speed) % H
        screen.blit(bg, (0, bg_y - H)) #[cite: 3]
        screen.blit(bg, (0, bg_y)) #[cite: 3]
        
        # update difficulty
        diff_mult = 1.5 if settings["diff"] == "hard" else 1.0
        distance += (base_speed / 60)
        
        # powerup timer logic
        now = pygame.time.get_ticks()
        if active_power and now > power_timer:
            active_power = None
            if P1.shield: P1.shield = False
            
        p_speed = 5 if active_power == "nitro" else 0
        real_speed = base_speed + p_speed + (distance / 200)

        # random spawners
        if random.random() < 0.02 * diff_mult:
            e = racer.Enemy(diff_mult)
            enemies.add(e)
            all_sprites.add(e)
            
        if random.random() < 0.03:
            c = racer.Coin()
            coins.add(c)
            all_sprites.add(c)
            
        if random.random() < 0.01 * diff_mult:
            o = racer.Obstacle()
            obstacles.add(o)
            all_sprites.add(o)
            
        if random.random() < 0.005 and not active_power:
            pw = racer.PowerUp()
            powerups.add(pw)
            all_sprites.add(pw)

        # move everything
        P1.move(p_speed)
        for s in all_sprites:
            if s != P1:
                s.move(real_speed)

        # Отрисовка спрайтов
        for s in all_sprites:
            if s == P1:
                P1.draw(screen) # Используем кастомный метод draw для Player (чтобы рисовать щит)
            else:
                screen.blit(s.image, s.rect) #[cite: 3]
            
        # UI during play
        ui.draw_text(screen, f"SCORE: {score}", 10, 10, small, (0,0,0)) #[cite: 3]
        ui.draw_text(screen, f"DIST: {int(distance)}M", 10, 30, small, (0,0,0))
        if active_power:
            ui.draw_text(screen, f"PWR: {active_power.upper()}", 10, 50, small, (255,0,0))

        # collisions
        if pygame.sprite.spritecollideany(P1, coins):
            hits = pygame.sprite.spritecollide(P1, coins, True)
            for h in hits:
                score += h.weight
                if score % 10 == 0:
                    base_speed += 0.5 # increase speed
                    
        if pygame.sprite.spritecollideany(P1, powerups):
            hits = pygame.sprite.spritecollide(P1, powerups, True)
            for h in hits:
                active_power = h.type
                power_timer = now + 4000
                if h.type == "shield":
                    P1.shield = True
                elif h.type == "repair":
                    for o in obstacles: o.kill() # clear obstacles
                    active_power = None # repair is instant
                    
        if pygame.sprite.spritecollideany(P1, enemies) or pygame.sprite.spritecollideany(P1, obstacles):
            if P1.shield:
                hits = pygame.sprite.spritecollide(P1, enemies, True)
                hits += pygame.sprite.spritecollide(P1, obstacles, True)
                P1.shield = False
                active_power = None
            else:
                # Звук аварии[cite: 3]
                if settings.get("sound", True):
                    try:
                        crash_sound.play()
                    except:
                        pass
                
                # game over[cite: 3]
                screen.fill((255,0,0)) #[cite: 3]
                ui.draw_text(screen, "CRASH!", W//2, H//2, font, center=True)
                pygame.display.update() #[cite: 3]
                time.sleep(1) #[cite: 3]
                persistence.save_score(username, score, distance)
                state = "GAMEOVER"

    elif state == "GAMEOVER":
        ui.draw_text(screen, "GAME OVER", W//2, 100, font, (255,0,0), True) #[cite: 3]
        ui.draw_text(screen, f"SCORE: {score}", W//2, 200, small, center=True)
        ui.draw_text(screen, f"DISTANCE: {int(distance)}M", W//2, 250, small, center=True)
        ui.draw_text(screen, "PRESS R TO RESTART", W//2, 400, small, center=True)

    pygame.display.update() #[cite: 3]
    clock.tick(60) #[cite: 3]