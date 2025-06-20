import pygame
from sys import exit


def display_score():
    current_time = pygame.time.get_ticks() // 1000 - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, 'Black')
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)  


pygame.init()
pygame.display.set_caption('Wibu')
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)
game_active = True
start_time = 0

text_surf = test_font.render('My Waifu', False, (253, 247, 244))
text_rect = text_surf.get_rect(midtop=(400, 40))
padded_text_rect = text_rect.inflate(20, 8)

reset_surf = test_font.render('Reset Game', False, (253, 247, 244))
reset_rect = reset_surf.get_rect(center=(400, 200))
padded_reset_rect = reset_rect.inflate(20, 8)

platform_surf = pygame.image.load('images/platform.jpg').convert()
platform_rect = platform_surf.get_rect(topleft=(0, 0))

back_surf = pygame.image.load('images/background.webp').convert()
back_rect = back_surf.get_rect(topleft=(0, 300))

opponent_surf = pygame.image.load('images/opponent.png').convert_alpha()  # Convert to format that boost Pygame speed
opponent_rect = opponent_surf.get_rect(midbottom=(400, 300))

ghost_surf = pygame.image.load('images/ghost.png').convert_alpha()
ghost_rect = ghost_surf.get_rect(midbottom=(200, 300))
ghost_gravity = 0
jump_state = False
JUMP_HEIGHT = 11

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not jump_state:
                    jump_state = True
                    ghost_gravity = -JUMP_HEIGHT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not jump_state:
                    jump_state = True
                    ghost_gravity = -JUMP_HEIGHT
                # if event.key == pygame.K_SPACE and jump_state and ghost_gravity >= 9:
                #     ghost_rect.midbottom = (200, 300)
                #     ghost_gravity = -JUMP_HEIGHT
        
        if not game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if padded_reset_rect.collidepoint(event.pos):
                    game_active = True
                    opponent_rect.left = 800
                    start_time = pygame.time.get_ticks() // 1000

    screen.fill('Black')

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_ESCAPE]:
    #     pygame.quit()
    #     exit()
    # if keys[pygame.K_UP] and not jump_state:
    #     jump_state = True
    #     print('up just pressed')
    # if not keys[pygame.K_UP] and jump_state:
    #     jump_state = False
    
    if game_active:
        screen.blit(platform_surf, platform_rect)
        screen.blit(back_surf, back_rect)
        # pygame.draw.rect(screen, (184, 47, 26), padded_text_rect, border_radius=3)
        # screen.blit(text_surf, text_rect)
        display_score()
            
        if opponent_rect.right < 0:
            opponent_rect.left = 800
        screen.blit(opponent_surf, opponent_rect)
        opponent_rect.left -= 4

        if jump_state:
            if ghost_gravity <= JUMP_HEIGHT:
                ghost_rect.y += ghost_gravity
                ghost_gravity += 1
            else:
                jump_state = False   
        screen.blit(ghost_surf, ghost_rect)

        if ghost_rect.colliderect(opponent_rect):
            game_active = False
    else:
        screen.fill((253, 247, 244))

        pygame.draw.rect(screen, (184, 47, 26), padded_reset_rect, border_radius=3)
        screen.blit(reset_surf, reset_rect)

    pygame.display.update()
    clock.tick(60)