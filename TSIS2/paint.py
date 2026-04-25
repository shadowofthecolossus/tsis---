import pygame
from datetime import datetime
import my_tools

def main():
    pygame.init()
    
    # big resolution
    WIDTH = 1280
    HEIGHT = 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("paint app")
    
    # create canvas
    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill((255, 255, 255)) # white background
    
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)
    ui_font = pygame.font.SysFont("Arial", 16)
    
    # my variables
    radius = 5
    mode = 'blue'
    
    # paint variables
    tool = 'pencil'
    drawing = False
    start_pos = (0, 0)
    last_pos = (0, 0)
    is_typing = False
    text_input = ""
    text_pos = (0, 0)
    
    colors = {
        'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255),
        'black': (0, 0, 0), 'white': (255, 255, 255), 'yellow': (255, 255, 0)
    }
    
    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        current_color = colors.get(mode, (0, 0, 0))
        
        for event in pygame.event.get():
            
            # check quit
            if event.type == pygame.QUIT:
                return
            
            # text typing mode
            if is_typing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        txt_surface = font.render(text_input, True, current_color)
                        canvas.blit(txt_surface, text_pos)
                        is_typing = False
                        text_input = ""
                    elif event.key == pygame.K_ESCAPE:
                        is_typing = False
                        text_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode
                continue # ignore other keys

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held: return
                if event.key == pygame.K_F4 and alt_held: return
                if event.key == pygame.K_ESCAPE: return
                
                # save file
                if event.key == pygame.K_s and ctrl_held:
                    filename = f"canvas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    pygame.image.save(canvas, filename)
                    print("saved!")

                # get color
                if event.key == pygame.K_r: mode = 'red'
                elif event.key == pygame.K_g: mode = 'green'
                elif event.key == pygame.K_b: mode = 'blue'
                elif event.key == pygame.K_k: mode = 'black'
                elif event.key == pygame.K_w: mode = 'white'
                elif event.key == pygame.K_y: mode = 'yellow'
                
                # get size
                if event.key == pygame.K_1: radius = 2
                elif event.key == pygame.K_2: radius = 5
                elif event.key == pygame.K_3: radius = 10

                # get tool
                if event.key == pygame.K_p: tool = 'pencil'
                elif event.key == pygame.K_l: tool = 'line'
                elif event.key == pygame.K_e: tool = 'eraser'
                elif event.key == pygame.K_f: tool = 'fill'
                elif event.key == pygame.K_t: tool = 'text'
                elif event.key == pygame.K_q: tool = 'rect'
                elif event.key == pygame.K_c: tool = 'circle'
                elif event.key == pygame.K_u: tool = 'square'
                elif event.key == pygame.K_v: tool = 'right_tri'
                elif event.key == pygame.K_x: tool = 'eq_tri'
                elif event.key == pygame.K_z: tool = 'rhombus'

            # mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left click
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos
                    
                    if tool == 'fill':
                        my_tools.flood_fill(canvas, start_pos[0], start_pos[1], current_color)
                    elif tool == 'text':
                        is_typing = True
                        text_pos = start_pos
                        text_input = ""
                        
                # mouse wheel for size
                elif event.button == 4: # scroll up
                    radius = min(200, radius + 1)
                elif event.button == 5: # scroll down
                    radius = max(1, radius - 1)

            # mouse release
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if drawing and tool not in ['pencil', 'eraser', 'fill', 'text']:
                        # draw shape on canvas
                        my_tools.draw_shape(canvas, tool, start_pos, event.pos, radius, current_color)
                    drawing = False

            # mouse move
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if tool == 'pencil':
                        my_tools.drawLineBetween(canvas, last_pos, event.pos, radius, current_color)
                    elif tool == 'eraser':
                        my_tools.drawLineBetween(canvas, last_pos, event.pos, radius*2, (255, 255, 255))
                    last_pos = event.pos
                
        # draw background
        screen.fill((200, 200, 200)) 
        screen.blit(canvas, (0, 0))
        
        # preview shape
        if drawing and tool not in ['pencil', 'eraser', 'fill', 'text']:
            my_tools.draw_shape(screen, tool, start_pos, pygame.mouse.get_pos(), radius, current_color)

        # show typing text
        if is_typing:
            txt_surf = font.render(text_input + "|", True, current_color)
            screen.blit(txt_surf, text_pos)

        # draw top panel
        ui_text = f"tool: {tool.upper()} | size: {radius} | color: {mode.upper()} | ctrl+s: save"
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, WIDTH, 25))
        screen.blit(ui_font.render(ui_text, True, (255, 255, 255)), (10, 5))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()