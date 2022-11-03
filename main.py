import pygame
from sys import exit

#initialixation of the pygame. This is more like a boiler plate code than anything else
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner Game")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font\Pixeltype.ttf", 50)

#ALL IMAGES
background_surf = pygame.image.load("graphics/background.png").convert()
ground_surf = pygame.image.load("graphics/ground.png").convert()

#font
text_surf = test_font.render("PyRunner", False, "Black")
text_rect = text_surf.get_rect(center = (400, 50))
#ALL CHARACTERS
snail_surf = pygame.image.load("graphics\Snail\snail1.png").convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (830,300))


player_surf = pygame.image.load("graphics\player\player_stand.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == 300:
            # if player_rect.collidepoint(event.pos):
            player_gravity = -20

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                player_gravity = -20


    #Showing everything on the screen_surface
    screen.blit(background_surf, (0,0))
    screen.blit(ground_surf, (0,300))
    pygame.draw.rect(screen, "Pink", text_rect)
    pygame.draw.rect(screen, "Black", text_rect, 1)

    screen.blit(text_surf, text_rect)
    #snail/ENEMY
    snail_rect.x -= 4
    if snail_rect.right <= 0:
        snail_rect.left = 800
    screen.blit(snail_surf, snail_rect)

    #player
    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.bottom >= 300:
        player_rect.bottom = 300
    screen.blit(player_surf, player_rect)

    #updating the frames
    pygame.display.update()
    clock.tick(60)