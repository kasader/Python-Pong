# Importing Libraries
import pygame
import time
import random

from pygame import mixer
from pygame.locals import *

# Window Size:
window_x = 720
window_y = 480

# Defining Colors:
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)

pygame.init()
mixer.init()

pygame.display.set_caption('Pong 2022')
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

main_menu = True

# Paddle Definitions:
player_pos = [window_x/10, window_y/2]
opponent_pos = [window_x-window_x/10, window_y/2]
paddle_direction = 'DOWN'
paddle_speed = 10
paddle_length = 125
paddle_width = 20

# Ball Definitions:
ball_pos = [window_x/2, window_y/2]
ball_size = 20
starting_dir = ['UP', 'DOWN']
starting_dir_RL = ['RIGHT', 'LEFT']
ball_direction = [random.choice(starting_dir_RL), random.choice(starting_dir)]
ball_velocity = [5, random.randrange(0,5,1)]
ball_cooldown = 0
ball_pass = random.choice(starting_dir_RL)

# Score List
player_score = 0
opponent_score = 0

# displaying Score function
def show_score(choice):
    score_font = pygame.font.Font('PublicPixel.ttf', 20)
    score_surface = score_font.render('Your Score : ' + str(player_score) + 
            ' Opponent Score : ' + str(opponent_score), True, white, black)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, (5, 5))

# game over function
def game_over():
    base_font = pygame.font.Font('PublicPixel.ttf', 25)
    game_over_surface = base_font.render(
        'GAME OVER', True, white, black)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x/2, window_y/4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

def opponent_ai():
    if (ball_direction[0] == 'LEFT' and ball_pos[0] < window_x/3):
        opponent_pos[1] = opponent_pos[1]
    if (ball_direction[0] == 'LEFT' and ball_pos[0] > window_x/3):
        if opponent_pos[1]+paddle_length/2 < window_y/3 and (
                opponent_pos[1]+paddle_length/2 > window_y/2):
            opponent_pos[1] += paddle_speed/2
        if opponent_pos[1]+paddle_length/2 < (window_y*2)/3 and (
                opponent_pos[1]+paddle_length/2 > window_y/2):
            opponent_pos[1] -= paddle_speed/2
        else:
            opponent_pos[1] = opponent_pos[1]
            
    if (ball_direction[0] == 'RIGHT'):
        if (ball_pos[1]-ball_size) < opponent_pos[1]+int((paddle_length*4)/10):
            if opponent_pos[1] <= 30:
                opponent_pos[1] = opponent_pos[1]
            else:
                opponent_pos[1] -= paddle_speed/2
        if (ball_pos[1]-ball_size) > opponent_pos[1]+int((paddle_length*6)/10):
            if opponent_pos[1] >= window_y-paddle_length-30:
                opponent_pos[1] = opponent_pos[1]
            else:
                opponent_pos[1] += paddle_speed/2

    if (ball_velocity[1] >= 7):
        if ball_direction[1] == 'DOWN':
            if opponent_pos[1] <= 30:
                opponent_pos[1] += paddle_speed
        else:
            if opponent_pos[1] >= window_y-paddle_length-30:
                opponent_pos[1] -= paddle_speed

    if (ball_velocity[1] <= 3):
        if ball_direction[1] == 'DOWN':
            if opponent_pos[1] <= 30:
                if (ball_pos[1]-ball_size) > opponent_pos[1]+int(
                        (paddle_length)):
                        opponent_pos[1] += paddle_speed/2
        if ball_direction[1] == 'UP':
            if opponent_pos[1] >= window_y-paddle_length-30:
                if (ball_pos[1]-ball_size) > opponent_pos[1]+int(
                    (paddle_length)):
                    opponent_pos[1] -= paddle_speed/2
        else:
            opponent_pos[1] = opponent_pos[1]

def player_movement():
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_UP]:
        if player_pos[1] <= 30:
            player_pos[1] = player_pos[1]
        else:
            player_pos[1] -= paddle_speed
    if keys_pressed[pygame.K_DOWN]:
        if player_pos[1] >= window_y-paddle_length-30:
            player_pos[1] = player_pos[1]
        else:
            player_pos[1] += paddle_speed



# Main Function
while main_menu == True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RETURN]:
            mixer.music.load("game_start.wav")
            mixer.music.play()
            time.sleep(1)
            main_menu = False
        if keys_pressed[pygame.K_ESCAPE]:
            time.sleep(1)
            pygame.quit()
            quit()

    font_size = 60
    base_font = pygame.font.Font('PublicPixel.ttf', font_size)
    game_over_surface = base_font.render(
        'P O N G ', True, white, black)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x/2+font_size/2, window_y/3)
    game_window.blit(game_over_surface, game_over_rect)

    confirm_font = pygame.font.Font('PublicPixel.ttf', int(font_size/4))
    play_confirmation_surface = confirm_font.render(
        'PRESS ENTER TO PLAY ', True, white, black)
    play_confirmation_rect = play_confirmation_surface.get_rect()
    play_confirmation_rect.midtop = (window_x/2+font_size/8, window_y*6/10)
    game_window.blit(play_confirmation_surface, play_confirmation_rect)
    pygame.display.flip()
    #time.sleep(2)


while True:

    # handling key events
    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            quit()

    opponent_ai()
    player_movement()

    mixer.music.load("hit.wav")
    # Ball Movement:
    # Ball Cooldown
    if ball_cooldown > 0:
        print(ball_cooldown)
        ball_cooldown +=1
        if ball_cooldown == 25:
            ball_cooldown = 0

    # PLAYER-PADDLE CONTACT:
    if ball_direction[0] == 'LEFT':
        if ball_pos[1] >= player_pos[1] and (ball_pos[1] + 
                ball_size) <= (player_pos[1] + paddle_length+20):
            ball_pos[0] -= ball_velocity[0]
            if ball_pos[0] >= (player_pos[0]) and ball_pos[0] <= (
                    player_pos[0] + paddle_width):
                ball_direction[0] = 'RIGHT'
                # Y-Velocity Calculation:
                topDist = (ball_pos[1]-10)-player_pos[1]
                print("TOP DIST: " + str(topDist))
                botDist = (player_pos[1]+paddle_length)-(ball_pos[1]-10)
                print("BOT DIST: " + str(botDist))
                if topDist < botDist:
                    ball_velocity[1] = abs(botDist/topDist-1)
                    print("TOP HIT: " + str(abs(botDist/topDist-1)))
                    ball_direction[1] = 'UP'
                if topDist > botDist:
                    ball_velocity[1] = abs(topDist/botDist-1)*3
                    print("BOT HIT: " + str(abs(topDist/botDist)*3))
                    ball_direction[1] = 'DOWN'
                mixer.music.load("paddle_hit.wav")
                mixer.music.play()
        else:
            ball_pos[0] -= ball_velocity[0]

    # OPPONENT-PADDLE CONTACT:
    if ball_direction[0] == 'RIGHT':
        if ball_pos[1] >= opponent_pos[1] and (ball_pos[1] +
                ball_size) <= (opponent_pos[1] + paddle_length+20):
            ball_pos[0] += ball_velocity[0]
            if ball_pos[0] >= (opponent_pos[0]-
                    paddle_width) and ball_pos[0] <= (opponent_pos[0]):
                ball_direction[0] = 'LEFT'
                # Y-Velocity Calculation:
                topDist = opponent_pos[1]-(ball_pos[1]-10)
                botDist = (opponent_pos[1]+paddle_length)-(ball_pos[1]-10)
                if topDist > botDist:
                    ball_velocity[1] = abs(topDist/botDist-1)
                else:
                    ball_velocity[1] = abs(botDist/topDist-1)*3
                mixer.music.load("paddle_hit.wav")
                mixer.music.play()
        else:
            ball_pos[0] += ball_velocity[0]

    # UP
    if ball_direction[1] == 'UP':
        if ball_pos[1] <= 30:
            print("FLIPPING DOWN")
            ball_direction[1] = 'DOWN'
            mixer.music.play()
        else:
            ball_pos[1] -= ball_velocity[1]

    # DOWN
    if ball_direction[1] == 'DOWN':
        if ball_pos[1] >= (window_y - ball_size)-30:
            print("FLIPPING UP")
            ball_direction[1] = 'UP' 
            mixer.music.play()
        else:
            ball_pos[1] += ball_velocity[1]

    # Velocity Bound-Check
    if ball_velocity[1] > 8:
        ball_velocity[1] = 8

    # POINT STATE CHECK:
    # OPPONENT WINS POINT:
    if ball_pos[0] < -10:
        opponent_score += 1
        mixer.music.load("point_score.wav")
        mixer.music.play()
        # Ball Reset
        ball_pos = [window_x/2, window_y/2]
        ball_velocity = [0,0]
        ball_cooldown += 1
        ball_pass = 'RIGHT'
    # PLAYER WINS POINT:
    if ball_pos[0] > window_x+10:
        mixer.music.load("point_score.wav")
        mixer.music.play()
        player_score += 1
        # Ball Reset
        ball_pos = [window_x/2, window_y/2]
        ball_velocity = [0,0]
        ball_cooldown += 1
        ball_pass = 'LEFT'

    # Ball Reinitializaion
    if ball_cooldown == 0 and ball_velocity[0] == 0:
        ball_pos = [window_x/2, window_y/2]
        ball_direction = [ball_pass, random.choice(starting_dir)]
        ball_velocity = [5, random.randrange(0,5,1)]

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_ESCAPE]:
        game_over()

    # RENDERING
    game_window.fill(black)

    dash = 40
    for i in range(30):
        pygame.draw.line(game_window, white, [window_x/2, 1 + dash], 
                [window_x/2, dash + 10], 4)
        dash += 20
    #all_sprites.draw(game_window)
    #pygame.display.flip()

    pygame.draw.rect(game_window, white,
            pygame.Rect(ball_pos[0]-(ball_size/2), 
                ball_pos[1]-(ball_size/2), ball_size, ball_size))
    pygame.draw.rect(game_window, white, 
            pygame.Rect(player_pos[0], player_pos[1], paddle_width, paddle_length))
    pygame.draw.rect(game_window, white, 
            pygame.Rect(opponent_pos[0], opponent_pos[1], paddle_width, paddle_length))

    # displaying score countinuously
    show_score(1)

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick(30)
