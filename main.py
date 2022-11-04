import pygame
from sys import exit
from random import randint

def get_score():
    current_time = int(pygame.time.get_ticks() / 100) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):

    if obstacle_list:
        for obstacle_rec in obstacle_list:
            obstacle_rec.x -= 5
            if obstacle_rec.bottom == 300:
                screen.blit(snail_surf, obstacle_rec)
            else:
                screen.blit(fly_surf, obstacle_rec)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []
def collision(player, obstacles):
    if obstacles:
        for obstacle_rec in obstacles:
            if player.colliderect(obstacle_rec): return False
    return True
def player_animation():
    global player_surf, player_index
    #animate when player's in floor
    if player_rect.bottom < 300:
        player_surf = player_jump
    #animation while player is jumping
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]

#GAME INITIALIZATION
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner Game")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font\Pixeltype.ttf", 50)
game_active = False
start_time = 0

#BACKGROUND
background_surf = pygame.image.load("graphics/background.png").convert()
ground_surf = pygame.image.load("graphics/ground.png").convert()


#PLAYER AND ENEMIES

#-------------------------------------PLAYER-----------------------------------------
player_walk_1 = pygame.image.load("graphics\player\player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics\player\player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics\player\jump.png").convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

#Enemies
#--------------------------------------SNAIL------------------------------------------
obstacles_rec_list = []
snail_frame_1 = pygame.image.load("graphics\Snail\snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics\Snail\snail2.png").convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_index = 0
snail_surf = snail_frames[snail_index]
#---------------------------------------FLY--------------------------------------------
fly_frame_1 = pygame.image.load("graphics/fly/Fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/fly/Fly2.png").convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_index = 0
fly_surf = fly_frames[fly_index]


#MAIN MENU DESIGN
title = test_font.render("PyRunner", False, (111, 196, 169))
title_rect = title.get_rect(center = (400, 50) )

player_stand_surf = pygame.image.load("graphics\player\player_stand.png").convert_alpha()
player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2)
player_stand_rect = player_stand_surf.get_rect(center = (400, 200))

instruction_surf = test_font.render("Press Spacebar to start", False, (111, 196, 169))
instruction_rec = instruction_surf.get_rect(center = (410, 330))

#MISC VARIABLES
score = 0


#TIMERS
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 200)
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 100)

#GANE LOOP
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
                if randint(0, 2):
                    obstacles_rec_list.append(snail_surf.get_rect(midbottom = (randint(900, 1100),300)))
                else:
                    obstacles_rec_list.append(fly_surf.get_rect(midbottom = (randint(900, 1100),210)))

            if event.type == snail_animation_timer:
                if snail_index == 1: snail_index = 0
                else: snail_index = 1
                snail_surf = snail_frames[snail_index]

            if event.type == fly_animation_timer:
                if fly_index == 1: fly_index = 0
                else: fly_index = 1
                fly_surf = fly_frames[fly_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/100)




#DISPLAYING ON THE SCREEN
    if game_active:
        screen.blit(background_surf, (0,0))
        screen.blit(ground_surf, (0,300))
        score = get_score()

#DISPLAY PLAYER
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)

#DISPLAY ENEMIES
        obstacle_rect_list = obstacle_movement(obstacles_rec_list)
#COLLISION
        game_active = collision(player_rect, obstacles_rec_list)
    else:
        screen.fill((94,129,162))
        screen.blit(title, title_rect)
        screen.blit(player_stand_surf, player_stand_rect)
        obstacles_rec_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        score_message = test_font.render(f"Your Score is: {score}", False, (111, 196, 169))
        score_message_rec = score_message.get_rect(center = (410, 330))

        if score == 0:
            screen.blit(instruction_surf, instruction_rec)
        else:
            screen.blit(score_message, score_message_rec)


#UPDATE FRAMES PER SECOND
    pygame.display.update()
    clock.tick(60)