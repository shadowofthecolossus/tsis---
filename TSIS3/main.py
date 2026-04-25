import pygame
import json
import random
import db
from game import Snake, Food, Poison, PowerUp, Point, WIDTH, HEIGHT, CELL
from color_palette import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 4: Ultimate Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# load settings
try:
    with open('settings.json', 'r') as f:
        settings = json.load(f)
except:
    settings = {"snake_color": [0, 255, 0], "grid_overlay": True, "sound": False}

# draw text helper
def draw_text(text, x, y, color=colorWHITE, center=False):
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center: 
        rect.center = (x, y)
    else: 
        rect.topleft = (x, y)
    screen.blit(surf, rect)

def main():
    state = "MENU"
    username = ""
    score = 0
    level = 1
    personal_best = 0
    
    snake = None
    food = None
    poison = Poison()
    powerup = PowerUp()
    obstacles = []
    
    base_fps = 5
    current_fps = base_fps
    powerup_end_time = 0

    running = True
    while running:
        screen.fill(colorBLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if state == "MENU":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(username) > 0:
                        personal_best = db.get_personal_best(username)
                        # init game
                        snake = Snake(settings["snake_color"])
                        food = Food()
                        food.generate_random_pos(snake.body, obstacles)
                        score = 0
                        level = 1
                        obstacles = []
                        current_fps = base_fps
                        state = "PLAY"
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    # changed to numbers so letters s and l can be typed in username
                    elif event.key == pygame.K_1:
                        state = "LEADERBOARD"
                    elif event.key == pygame.K_2:
                        state = "SETTINGS"
                    else:
                        if len(username) < 15 and event.unicode.isprintable():
                            username += event.unicode
                            
            elif state == "PLAY":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and snake.dx == 0:
                        snake.dx, snake.dy = 1, 0
                    elif event.key == pygame.K_LEFT and snake.dx == 0:
                        snake.dx, snake.dy = -1, 0
                    elif event.key == pygame.K_DOWN and snake.dy == 0:
                        snake.dx, snake.dy = 0, 1
                    elif event.key == pygame.K_UP and snake.dy == 0:
                        snake.dx, snake.dy = 0, -1

            elif state == "GAME_OVER":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        state = "MENU" # go back to menu
                        
            elif state in ["LEADERBOARD", "SETTINGS"]:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "MENU"

        # --- STATE: MENU ---
        if state == "MENU":
            draw_text("ULTIMATE SNAKE", WIDTH//2, HEIGHT//3, colorGREEN, True)
            draw_text("Enter Username: " + username + "_", WIDTH//2, HEIGHT//2, colorWHITE, True)
            draw_text("Press ENTER to Play", WIDTH//2, HEIGHT//2 + 50, colorYELLOW, True)
            # updated menu text
            draw_text("Press 1 for Leaderboard | 2 for Settings", WIDTH//2, HEIGHT//2 + 100, colorGRAY, True)

        # --- STATE: LEADERBOARD ---
        elif state == "LEADERBOARD":
            draw_text("TOP 10 PLAYERS", WIDTH//2, 50, colorGREEN, True)
            tops = db.get_top_10()
            y = 100
            for i, r in enumerate(tops):
                draw_text(f"{i+1}. {r[0]} - Score: {r[1]} - Lvl: {r[2]}", 100, y)
                y += 40
            draw_text("Press ESC to return", WIDTH//2, HEIGHT - 50, colorGRAY, True)

        # --- STATE: SETTINGS ---
        elif state == "SETTINGS":
            draw_text("SETTINGS (Edit settings.json to change)", WIDTH//2, 100, colorGREEN, True)
            draw_text(f"Snake Color (RGB): {settings['snake_color']}", 100, 200)
            draw_text(f"Grid Overlay: {settings['grid_overlay']}", 100, 250)
            draw_text(f"Sound: {settings['sound']}", 100, 300)
            draw_text("Press ESC to return", WIDTH//2, HEIGHT - 50, colorGRAY, True)

        # --- STATE: PLAY ---
        elif state == "PLAY":
            now = pygame.time.get_ticks()
            
            # powerup logic
            if powerup.active and now - powerup.spawn_time > 8000:
                powerup.active = False
            if now > powerup_end_time:
                current_fps = base_fps + (level * 2) # normal speed
            
            # move snake
            snake.move()

            # wall / self / obstacle collisions
            if snake.check_wall_collision() or snake.check_self_collision() or \
               any(o.x == snake.body[0].x and o.y == snake.body[0].y for o in obstacles):
                db.save_result(username, score, level)
                state = "GAME_OVER"
                
            # eat food
            if snake.body[0].x == food.pos.x and snake.body[0].y == food.pos.y:
                score += food.weight
                # grow
                snake.body.append(Point(snake.body[-1].x, snake.body[-1].y))
                food.generate_random_pos(snake.body, obstacles)
                
                # level up check (every 30 points)
                new_level = (score // 30) + 1
                if new_level > level:
                    level = new_level
                    # level 3+ obstacles
                    if level >= 3:
                        obstacles.append(Point(random.randint(0, WIDTH//CELL-1), random.randint(0, HEIGHT//CELL-1)))
                
                # random spawn poison or powerup
                if random.random() < 0.3:
                    poison.active = True
                    poison.pos.x = random.randint(0, WIDTH//CELL-1)
                    poison.pos.y = random.randint(0, HEIGHT//CELL-1)
                if random.random() < 0.2 and not powerup.active:
                    powerup.active = True
                    powerup.type = random.choice(['speed', 'slow', 'shield'])
                    powerup.pos.x = random.randint(0, WIDTH//CELL-1)
                    powerup.pos.y = random.randint(0, HEIGHT//CELL-1)
                    powerup.spawn_time = now

            # eat poison
            if poison.active and snake.body[0].x == poison.pos.x and snake.body[0].y == poison.pos.y:
                poison.active = False
                if len(snake.body) > 2:
                    snake.body.pop()
                    snake.body.pop()
                else:
                    db.save_result(username, score, level)
                    state = "GAME_OVER"

            # eat powerup
            if powerup.active and snake.body[0].x == powerup.pos.x and snake.body[0].y == powerup.pos.y:
                powerup.active = False
                if powerup.type == 'speed':
                    current_fps += 10
                    powerup_end_time = now + 5000
                elif powerup.type == 'slow':
                    current_fps = max(2, current_fps - 5)
                    powerup_end_time = now + 5000
                elif powerup.type == 'shield':
                    snake.shield_active = True

            # draw grid if enabled
            if settings["grid_overlay"]:
                for i in range(HEIGHT // CELL):
                    for j in range(WIDTH // CELL):
                        pygame.draw.rect(screen, colorGRAY, (j * CELL, i * CELL, CELL, CELL), 1)

            # draw entities
            for o in obstacles:
                pygame.draw.rect(screen, colorGRAY, (o.x * CELL, o.y * CELL, CELL, CELL))
            poison.draw(screen)
            powerup.draw(screen)
            food.draw(screen)
            snake.draw(screen)
            
            # draw HUD
            draw_text(f"Score: {score} | Level: {level} | Best: {personal_best}", 10, 10)

        # --- STATE: GAME OVER ---
        elif state == "GAME_OVER":
            draw_text("GAME OVER", WIDTH//2, HEIGHT//3, colorRED, True)
            draw_text(f"Final Score: {score}", WIDTH//2, HEIGHT//2, colorWHITE, True)
            draw_text(f"Level Reached: {level}", WIDTH//2, HEIGHT//2 + 40, colorWHITE, True)
            draw_text("Press R to return to Menu", WIDTH//2, HEIGHT//2 + 100, colorGRAY, True)

        pygame.display.flip()
        
        if state == "PLAY":
            clock.tick(current_fps)
        else:
            clock.tick(15)

    pygame.quit()

if __name__ == "__main__":
    main()