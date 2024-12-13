import pygame
import math
import random
from pygame import mixer

# Intialize the pygame
pygame.init()

# Create the screen and the screen size
# ( Width, Height )
screen = pygame.display.set_mode(( 800, 600 ))

# Background
background = pygame.image.load('Galaxy.png')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invadors")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
PlayerImg = pygame.image.load('spaceship.png')
PlayerX = 368
PlayerY = 480
Xchange = 0

# Enemy
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyXchange = []
EnemyYchange = []
num_of_Enemies = 6

for i in range(6):
    EnemyImg.append(pygame.image.load('art.png'))
    EnemyX.append(random.randint(0, 736))
    EnemyY.append(random.randint(50, 150))
    EnemyXchange.append(random.uniform(0.2, 0.4))
    EnemyYchange.append(40)

# Bullet
# ready state -> can't see the bullet on the screen
# fier state -> the bullet is currently moving
BulletImg = pygame.image.load('bullet.png')
BulletX = 0
BulletY = 480
BulletXchange = 0.2
BulletYchange = 0.5
Bullet_state = "ready"

# Score
Score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
TextX = 10
TextY = 10

# Game Over text
game_over = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score: " + str(Score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    # Draw the image on the screen
    screen.blit(PlayerImg, (x, y))

def Enemy(x, y, index):
    # Draw the image on the screen
    screen.blit(EnemyImg[index], (x, y))

def Fire_Bullet(x, y):
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))

def isCollision(EnemyX, EnemyY, BulletX, BulletY):
    distance = math.sqrt(math.pow(EnemyX - BulletX,2) + math.pow(EnemyY - BulletY, 2))
    return distance < 27

def game_over_text():
    over = game_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (200, 250))


# Game Loop
run = True
while run:
    # RGB in parentheses
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (-160, -100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # KEYDOWN is a key is pressed, KEYUP is a key is released
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                Xchange = -0.2
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                Xchange = 0.2
            elif event.key == pygame.K_SPACE:
                if Bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    BulletX = PlayerX
                    Fire_Bullet(PlayerX, BulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT or event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                Xchange = 0
    
    # Checking for boundaries of spaceship
    PlayerX += Xchange
    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 736:
        PlayerX = 736

    # Enemy boundaries
    for i in range(num_of_Enemies):
        # Game Over
        if EnemyY[i] > 440:
            for j in range(num_of_Enemies):
                EnemyY[j] = 2000

            game_over_text()
            break

        EnemyX[i] += EnemyXchange[i]
        if EnemyX[i] <= 0:
            EnemyXchange[i] = 0 - EnemyXchange[i]
            EnemyY[i] += EnemyYchange[i]
        elif EnemyX[i] >= 736:
            EnemyXchange[i] = 0 - EnemyXchange[i]
            EnemyY[i] += EnemyYchange[i]

        # Collision
        collision = isCollision(EnemyX[i], EnemyY[i], BulletX, BulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            Bullet_state = "ready"
            BulletY = 480
            Score_value += 1
            EnemyX[i] = random.randint(0, 736)
            EnemyY[i] = random.randint(50, 150)
            EnemyXchange[i] = random.uniform(0.2, 0.4)  

        Enemy(EnemyX[i], EnemyY[i], i)

    # Bullet Movement
    if BulletY <= 0:
        Bullet_state = "ready"
        BulletY = 480

    if Bullet_state == "fire":
        Fire_Bullet(BulletX, BulletY)
        BulletY -= BulletYchange

    player(PlayerX, PlayerY)
    show_score(TextX, TextY)
    pygame.display.update()

pygame.quit()