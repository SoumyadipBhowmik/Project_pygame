import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics\player\player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics\player\player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics\player\jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound("audio/audio_jump.mp3")

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
            self.jump_sound.set_volume(0.2)

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def player_Animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_Animation()

class Enemies(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load("graphics/fly/Fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/fly/Fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load("graphics\Snail\snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics\Snail\snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
    def enemy_Animation(self):

        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.enemy_Animation()
        self.rect.x -= 6
        self.destroy()

def collision():
    if pygame.sprite.spritecollide(player.sprite, enemies, False):
        enemies.empty()
        return False
    return True


def get_score():
    current_time = int(pygame.time.get_ticks() / 100) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

#GAME INITIALIZATION
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner Game")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font\Pixeltype.ttf", 50)
game_active = False
start_time = 0


#-----------------------------------BACKGROUND---------------------------------------
background_surf = pygame.image.load("graphics/background.png").convert()
ground_surf = pygame.image.load("graphics/ground.png").convert()
background_music = pygame.mixer.Sound("audio\music.wav")
background_music.set_volume(0.1)
main_menu_music = pygame.mixer.Sound("audio/this-is-war-version-e-95411.mp3")
main_menu_music.set_volume(0.1)
background_music.play()
#MISC VARIABLES
score = 0

#PLAYER AND ENEMIES

#-------------------------------------PLAYER-----------------------------------------
player = pygame.sprite.GroupSingle()
player.add(Player())
#------------------------------------ENEMIES-----------------------------------------
enemies = pygame.sprite.Group()
#--------------------------------MAIN MENU DESIGN------------------------------------
title = test_font.render("PyRunner", False, (111, 196, 169))
title_rect = title.get_rect(center = (400, 50) )

player_stand_surf = pygame.image.load("graphics\player\player_stand.png").convert_alpha()
player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2)
player_stand_rect = player_stand_surf.get_rect(center = (400, 200))

instruction_surf = test_font.render("Press Spacebar to start", False, (111, 196, 169))
instruction_rec = instruction_surf.get_rect(center = (410, 330))
#--------------------------------------------------------------------------------------

#-----------------------------------TIMERS---------------------------------------------
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, randint(1000, 1500))

#GANE LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                enemies.add(Enemies(choice(['fly', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/100)


#DISPLAYING ON THE SCREEN
    if game_active:
        screen.blit(background_surf, (0,0))
        screen.blit(ground_surf, (0,300))
#--------------------------------SCORE------------------------------
        score = get_score()
#--------------------------------------------------------------------
#DISPLAY PLAYER
        player.draw(screen)
        player.update()

#DISPLAY ENEMIES
        enemies.draw(screen)
        enemies.update()
#COLLISION
        game_active = collision()
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

#UPDATE FRAMES PER SECOND
    pygame.display.update()
    clock.tick(60)