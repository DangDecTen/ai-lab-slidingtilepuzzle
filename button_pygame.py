import pygame
pygame.init()

screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)

# --- Button Properties ---
button_color = (70, 130, 180)
hover_color = (100, 160, 210)
text_color = (255, 255, 255)
button_rect = pygame.Rect(300, 150, 200, 60)
button_text = font.render("Click Me", True, text_color)
button_text_rect = button_text.get_rect(center=button_rect.center)

# --- Main Loop ---
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Draw Background ---
    screen.fill((30, 30, 30))

    # --- Hover Effect ---
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button_rect)
        if mouse_click[0]:  # left click
            print("Button clicked!")
    else:
        pygame.draw.rect(screen, button_color, button_rect)

    # --- Draw Text ---
    screen.blit(button_text, button_text_rect)

    pygame.display.update()
    clock.tick(60)
