import pygame
import random
import math
from pygame import mixer

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Space invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
background = pygame.image.load('background.png')

mixer.music.load('background.wav')
mixer.music.play()

playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
player_change = 0

number_of_enemies = 6
enemyImage = []
enemyX = []
enemyY = []
enemy_changeX = []
enemy_changeY = []

for enemy in range(number_of_enemies):
    enemyImage.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemy_changeX.append(4)
    enemy_changeY.append(20)

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render("Score: " + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x+16,y+10))

def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow(enemyx - bulletx,2)+(math.pow(enemyy-bullety,2)))
    if distance < 27:
        return True
    else:
        return False

def game_over_text():
    over_text = over_font.render('GAME OVER',True,(255,255,255))
    screen.blit(over_text, (200,250))

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_change += -4
            elif event.key == pygame.K_RIGHT:
                player_change += 4
            elif event.key == pygame.K_SPACE:
                bullet_Sound = mixer.Sound('laser.wav')
                bullet_Sound.play()
                if bullet_state is 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            player_change = 0


    playerX += player_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(number_of_enemies):
        if enemyY[i] > 400:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemy_changeX[i]
        if enemyX[i] <= 0:
            enemy_changeX[i] = 3
            enemyY[i] += enemy_changeY[i]
        elif enemyX[i] >= 736:
            enemy_changeX[i] = -3
            enemyY[i] += enemy_changeY[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_Sound = mixer.Sound('explosion.wav')
            collision_Sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # movement bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state is 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY)
    show_score(10,10)
    pygame.display.update()
