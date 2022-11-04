import pygame
from sys import exit

def get_score():
    current_time = int(pygame.time.get_ticks() / 100) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

#initialixation of the pygame. This is more like a boiler plate code than anything else
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner Game")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font\Pixeltype.ttf", 50)
game_active = False
start_time = 0

#ALL IMAGES
background_surf = pygame.image.load("graphics/background.png").convert()
ground_surf = pygame.image.load("graphics/ground.png").convert()

#Player
player_surf = pygame.image.load("graphics\player\player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

#Obstacles
snail_surf = pygame.image.load("graphics\Snail\snail1.png").convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (830,300))

#This is for the main menu
title = test_font.render("PyRunner", False, (111, 196, 169))
title_rect = title.get_rect(center = (400, 50) )

player_stand_surf = pygame.image.load("graphics\player\player_stand.png").convert_alpha()
player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2)
player_stand_rect = player_stand_surf.get_rect(center = (400, 200))

instruction_surf = test_font.render("Press Spacebar to start", False, (111, 196, 169))
instruction_rec = instruction_surf.get_rect(center = (410, 330))
score = 0

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 900)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == 300:
                player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20
            if event.type == obstacle_timer:
                print("text")
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                start_time = int(pygame.time.get_ticks()/100)

    #Showing everything on the screen_surface
    if game_active:
        screen.blit(background_surf, (0,0))
        screen.blit(ground_surf, (0,300))
        score = get_score()

        #player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)
        if player_rect.colliderect(snail_rect):
            game_active = False
    else:
        screen.fill((94,129,162))
        screen.blit(title, title_rect)
        screen.blit(player_stand_surf, player_stand_rect)

        score_message = test_font.render(f"Your Score is: {score}", False, (111, 196, 169))
        score_message_rec = score_message.get_rect(center = (410, 330))

        if score == 0:
            screen.blit(instruction_surf, instruction_rec)
        else:
            screen.blit(score_message, score_message_rec)


    #updating the frames
    pygame.display.update()
    clock.tick(60)