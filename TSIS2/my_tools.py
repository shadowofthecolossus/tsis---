import pygame

# draw shapes
def draw_shape(surface, tool, start, end, width, color):
    if tool == 'rect':
        rect = pygame.Rect(start[0], start[1], end[0]-start[0], end[1]-start[1])
        rect.normalize()
        pygame.draw.rect(surface, color, rect, width)
    elif tool == 'circle':
        radius = max(abs(end[0]-start[0]), abs(end[1]-start[1])) // 2
        center = ((start[0]+end[0])//2, (start[1]+end[1])//2)
        if width > radius: 
            width = 0 # solid circle if width is too big
        pygame.draw.circle(surface, color, center, radius, width)
    elif tool == 'square':
        side = max(abs(end[0]-start[0]), abs(end[1]-start[1]))
        sign_x = 1 if end[0] >= start[0] else -1
        sign_y = 1 if end[1] >= start[1] else -1
        rect = pygame.Rect(start[0], start[1], side*sign_x, side*sign_y)
        rect.normalize()
        pygame.draw.rect(surface, color, rect, width)
    elif tool == 'right_tri':
        points = [start, (start[0], end[1]), end]
        pygame.draw.polygon(surface, color, points, width)
    elif tool == 'eq_tri':
        mid_x = (start[0] + end[0]) // 2
        points = [(mid_x, start[1]), (start[0], end[1]), (end[0], end[1])]
        pygame.draw.polygon(surface, color, points, width)
    elif tool == 'rhombus':
        mid_x = (start[0] + end[0]) // 2
        mid_y = (start[1] + end[1]) // 2
        points = [(mid_x, start[1]), (end[0], mid_y), (mid_x, end[1]), (start[0], mid_y)]
        pygame.draw.polygon(surface, color, points, width)
    elif tool == 'line':
        pygame.draw.line(surface, color, start, end, width)

# fill tool algorithm
def flood_fill(surface, x, y, fill_color):
    target_color = surface.get_at((x, y))
    if target_color == fill_color: 
        return
    stack = [(x, y)]
    width, height = surface.get_size()
    while stack:
        cx, cy = stack.pop()
        if 0 <= cx < width and 0 <= cy < height:
            if surface.get_at((cx, cy)) == target_color:
                surface.set_at((cx, cy), fill_color)
                stack.append((cx + 1, cy))
                stack.append((cx - 1, cy))
                stack.append((cx, cy + 1))
                stack.append((cx, cy - 1))

# line drawing for smooth pencil
def drawLineBetween(screen, start, end, width, color):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    if iterations == 0: 
        iterations = 1

    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)