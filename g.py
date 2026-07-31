import pygame
import random

pygame.init()

# -----------------------
# SCREEN
# -----------------------
WIDTH = 500
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing")

clock = pygame.time.Clock()

# -----------------------
# IMAGES
# -----------------------

road = pygame.image.load("ROAD1.webp").convert()
road = pygame.transform.scale(road, (300, HEIGHT))

tree1 = pygame.image.load("T2.png").convert_alpha()
tree2 = pygame.image.load("T2.png").convert_alpha()

tree1 = pygame.transform.scale(tree1, (90, 140))
tree2 = pygame.transform.scale(tree2, (90, 140))

player = pygame.image.load("enemy car.webp").convert_alpha()
enemy = pygame.image.load("extra car.webp").convert_alpha()

player = pygame.transform.smoothscale(player, (70,120))
enemy = pygame.transform.smoothscale(enemy, (70,120))

# -----------------------
# PLAYER
# -----------------------

car_x = 215
car_y = 560

car_speed = 7

# -----------------------
# ENEMY
# -----------------------

lanes = [120,190,260,330]

enemy_x = random.choice(lanes)
enemy_y = -150

game_speed = 8

# -----------------------
# STARS
# -----------------------

stars=[]

for i in range(150):

    x=random.randint(0,WIDTH)
    y=random.randint(0,HEIGHT)
    r=random.randint(1,3)

    stars.append([x,y,r])

# -----------------------
# BACKGROUND
# -----------------------

road_y = 0
tree_y = 0



# -----------------------
# SCORE
# -----------------------

score = 0
font = pygame.font.SysFont("Arial",30)

game_over = False
running = True

# ==========================
# GAME LOOP
# ==========================

while running:

    clock.tick(60)

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # --------------------
    # GAME OVER
    # --------------------

    if game_over:

        screen.fill((0,0,0))

        t1 = font.render("GAME OVER",True,(255,0,0))
        t2 = font.render("Press R To Restart",True,(255,255,255))

        screen.blit(t1,(140,280))
        screen.blit(t2,(95,330))

        pygame.display.update()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:

            car_x = 215
            car_y = 560

            enemy_x = random.choice(lanes)
            enemy_y = -150

            score = 0
            game_speed = 8

            road_y = 0
            tree_y = 0

            game_over = False

        continue

    # --------------------
    # KEYBOARD
    # --------------------

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and car_x > 110:
        car_x -= car_speed

    if keys[pygame.K_RIGHT] and car_x < 320:
        car_x += car_speed

    if keys[pygame.K_UP]:
        game_speed += 0.1

    if keys[pygame.K_DOWN]:
        game_speed -= 0.1

    if game_speed < 5:
        game_speed = 5

    if game_speed > 20:
        game_speed = 20

    # --------------------
    # ENEMY
    # --------------------

    enemy_y += game_speed

    if enemy_y > HEIGHT:

        enemy_y = -150
        enemy_x = random.choice(lanes)

        score += 1

    # --------------------
    # ANIMATION
    # --------------------

    road_y += game_speed

    if road_y >= HEIGHT:
        road_y = 0

    tree_y += game_speed * 0.6

    if tree_y >= 200:
        tree_y = 0

    # --------------------
    # BACKGROUND
    # --------------------



    # --------------------
    # MAP BACKGROUND
    # --------------------

    # Night Sky
    screen.fill((8,10,30))


# Moon
    pygame.draw.circle(
        screen,
        (240,240,200),
        (420,80),
        35
    )


# Stars

    for star in stars:

        pygame.draw.circle(
            screen,
            (255,255,255),
            (star[0],star[1]),
            star[2]
        )


# Grass Left

    pygame.draw.rect(
        screen,
        (20,90,20),
        (0,0,100,HEIGHT)
    )


# Grass Right

    pygame.draw.rect(
        screen,
        (20,90,20),
        (400,0,100,HEIGHT)
    )


# Footpath

    pygame.draw.rect(
        screen,
        (120,120,120),
        (85,0,15,HEIGHT)
    )


    pygame.draw.rect(
        screen,
        (120,120,120),
        (400,0,15,HEIGHT)
    )



# Road Image

    screen.blit(road,(100,road_y-HEIGHT))
    screen.blit(road,(100,road_y))
    


    
    
    for y in range(-200,HEIGHT+200,200):

        screen.blit(tree1,(5,y+tree_y))
        screen.blit(tree2,(410,y+100+tree_y))

    # --------------------
    # CARS
    # --------------------

    screen.blit(player,(car_x,car_y))
    screen.blit(enemy,(enemy_x,enemy_y))

    # --------------------
    # COLLISION
    # --------------------

    player_rect = pygame.Rect(
        car_x+15,
        car_y+15,
        40,
        90
    )

    enemy_rect = pygame.Rect(
        enemy_x+15,
        enemy_y+15,
        40,
        90
    )

    if player_rect.colliderect(enemy_rect):
        game_over = True

    # --------------------
    # SCORE
    # --------------------

    score_text = font.render(
        f"Score : {score}",
        True,
        (255,255,255)
    )

    speed_text = font.render(
        f"Speed : {round(game_speed,1)}",
        True,
        (255,255,0)
    )

    screen.blit(score_text,(20,20))
    screen.blit(speed_text,(20,60))

    pygame.display.update()

pygame.quit()
