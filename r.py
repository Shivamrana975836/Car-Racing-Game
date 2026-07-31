import pygame
import random
import math

pygame.init()

WIDTH=500
HEIGHT=700

screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Car Racing")
clock=pygame.time.Clock()

# Images
road=pygame.image.load("rs3.png").convert()
road=pygame.transform.scale(road,(360,HEIGHT))

tree=pygame.image.load("t3.png").convert_alpha()
tree=pygame.transform.scale(tree,(80,120))

player=pygame.image.load("enemy car.webp").convert_alpha()
enemy=pygame.image.load("extra car.webp").convert_alpha()

player=pygame.transform.smoothscale(player,(65,110))
enemy=pygame.transform.smoothscale(enemy,(65,110))

# Coin Icon
coin_img = pygame.image.load("coin.png").convert_alpha()
coin_img = pygame.transform.smoothscale(coin_img,(26,26))

# Player
car_x=220
car_y=560
car_speed=7

# Enemy
lanes=[110,180,250,320]
enemy_x=random.choice(lanes)
enemy_y=-150

speed=8

# Stars
stars=[]
for i in range(100):
    stars.append([
        random.randint(0,WIDTH),
        random.randint(0,HEIGHT),
        random.randint(1,3)
    ])

road_y=0
tree_y=0

score=0
try:
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())
except:
    high_score = 0
font=pygame.font.SysFont("Arial",30)
small_font = pygame.font.SysFont("Arial",18)

game_over=False
running=True
paused = False

pause_btn = pygame.Rect(445, 5, 45, 45)
pause_font = pygame.font.SysFont("Arial",28,True)

left_btn = pygame.Rect(20, 600, 90, 80)
right_btn = pygame.Rect(390, 600, 90, 80)
boost_btn = pygame.Rect(200, 580, 100, 100)

boost = False

move_left = False
move_right = False

go_timer = pygame.time.get_ticks()
show_go = True
# ===== GAME SYSTEM =====

coins = 0

fuel = 100

engine_temp = 25

fuel_timer = pygame.time.get_ticks()

needle_speed = 0

coin_x = random.choice(lanes) + 20
coin_y = -300
coin_angle = 0

# =======================

while running:
    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:

            if pause_btn.collidepoint(event.pos):
                paused = not paused

            if left_btn.collidepoint(event.pos):
                move_left = True

            if right_btn.collidepoint(event.pos):
                move_right = True

            if boost_btn.collidepoint(event.pos):

                if show_go:
                    speed = min(speed + 5,20)

                boost = True


        if event.type == pygame.MOUSEBUTTONUP:
            move_left = False
            move_right = False
            boost = False
            
            
    if paused:

        screen.fill((15,15,15))

        txt = pygame.font.SysFont("Arial",50,True)
        text = txt.render("PAUSED",True,(255,255,0))

        screen.blit(text,(135,280))

        pygame.display.update()
        continue
    
    if game_over:
        screen.fill((0,0,0))
        screen.blit(font.render("GAME OVER",True,(255,0,0)),(150,280))
        screen.blit(font.render("Press R Restart",True,(255,255,255)),(120,330))
        pygame.display.update()

        if pygame.key.get_pressed()[pygame.K_r]:
            car_x=220
            enemy_x=random.choice(lanes)
            enemy_y=-150
            score=0
            speed=8
            game_over=False

        continue

    keys=pygame.key.get_pressed()

    if (keys[pygame.K_LEFT] or move_left) and car_x > 80:
        car_x -= car_speed

    if (keys[pygame.K_RIGHT] or move_right) and car_x < 350:
        car_x += car_speed

    if keys[pygame.K_UP]:
        speed+=0.1

    if keys[pygame.K_DOWN]:
        speed-=0.1
        
    if boost:
        speed += 0.25
    else:
        speed -= 0.08


    speed=max(8,min(speed,20))
    # ===== ENGINE =====

    if speed > 15:
        engine_temp += 0.05
    else:
        engine_temp -= 0.03

    engine_temp = max(25,min(engine_temp,100))

    # Fuel

    if pygame.time.get_ticks()-fuel_timer>400:

        fuel -= 0.15

        fuel_timer = pygame.time.get_ticks()

    fuel=max(0,min(fuel,100))

    if fuel<=0:
        game_over=True

    if engine_temp>=100:
        game_over=True

    # Smooth Needle

    meter_speed=int((speed-8)/12*200)

    needle_speed += (meter_speed-needle_speed)*0.08


    # Enemy

    enemy_y += speed
    coin_y += speed

    if enemy_y > HEIGHT:
        enemy_y = -150
        enemy_x = random.choice(lanes)
        score += 1

    # Coin tabhi respawn hoga jab screen se bahar chala jayega  
    
    if coin_y > HEIGHT:
        coin_y = random.randint(-800,-250)
        coin_x = random.choice(lanes) + 20
        
    #high score 

    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as f:
            f.write(str(high_score))
            
    # Road movement
    road_y+=speed

    if road_y>=HEIGHT:
        road_y=0

    tree_y+=speed*0.5

    if tree_y>=200:
        tree_y=0

    # Background
    screen.fill((8,10,30))

    pygame.draw.circle(screen,(240,240,200),(420,80),35)

    for s in stars:
        pygame.draw.circle(screen,(255,255,255),(s[0],s[1]),s[2])

    pygame.draw.rect(screen,(20,90,20),(0,0,70,HEIGHT))
    pygame.draw.rect(screen,(20,90,20),(430,0,70,HEIGHT))

    pygame.draw.rect(screen,(120,120,120),(70,0,15,HEIGHT))
    pygame.draw.rect(screen,(120,120,120),(415,0,15,HEIGHT))

    # Road
    screen.blit(road,(70,road_y-HEIGHT))
    screen.blit(road,(70,road_y))

    # Trees
    for y in range(-200,HEIGHT+200,200):
        screen.blit(tree,(0,y+tree_y))
        screen.blit(tree,(420,y+100+tree_y))

    # Cars
    screen.blit(player,(car_x,car_y))
    screen.blit(enemy,(enemy_x,enemy_y))
    
    pygame.draw.circle(screen,(255,215,0),(coin_x,coin_y),12)
    pygame.draw.circle(screen,(255,255,180),(coin_x,coin_y),12,2)
    pygame.draw.circle(screen,(255,245,120),(coin_x-3,coin_y-3),4)

    # Collision
    p=pygame.Rect(car_x+10,car_y+10,45,85)
    e=pygame.Rect(enemy_x+10,enemy_y+10,45,85)

    if p.colliderect(e):
        game_over=True
        
        coin_rect = pygame.Rect(coin_x-12,coin_y-12,24,24)

    if p.colliderect(coin_rect):

        coins += 1

        coin_y = random.randint(-800,-250)
        coin_x = random.choice(lanes) + 20

    # Score
    
    screen.blit(font.render(f"Score : {score}",True,(255,255,255)),(20,20))

    high_text = font.render(f"High : {high_score}",True,(0,255,0))
    screen.blit(high_text,(WIDTH - high_text.get_width() - 20,20))
    
    

    coin_glow = pygame.Surface((40,40),pygame.SRCALPHA)

    pygame.draw.circle(coin_glow,(255,220,0,70),(20,20),18)

    screen.blit(coin_glow,(445,50))

    screen.blit(coin_img,(452,57))

    coin_font = pygame.font.SysFont("Arial",16,True)

    screen.blit(
        coin_font.render(str(coins),True,(255,255,255)),
        (456,82)
    )
    
    coin_font = pygame.font.SysFont("Arial",18,True)
    
    # ===== Coin Icon =====

    ui_coin_x = 455
    ui_coin_y = 60

    pygame.draw.circle(screen,(255,215,0),(ui_coin_x,ui_coin_y),12)
    pygame.draw.circle(screen,(255,255,120),(ui_coin_x,ui_coin_y),12,2)

    coin_text = pygame.font.SysFont("Arial",16,True).render(
        str(coins),
        True,
        (255,255,255)
    )

    screen.blit(coin_text,(446,78))

    screen.blit(
        coin_font.render("Coins : "+str(coins),True,(255,215,0)),
        (20,95)
    )


    # ================= REAL SPEEDOMETER =================

    meter_x = 95
    meter_y = 150
    radius = 78


    # Transparent Background
    glass = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)

    pygame.draw.circle(
        glass,
        (10,10,10,35),   # Last value = transparency (0-255)
        (radius, radius),
        radius
    )

    screen.blit(glass,(meter_x-radius,meter_y-radius))

# Blue Glow Ring
    
    pygame.draw.circle(screen,(0,90,255),(meter_x,meter_y),radius+2,7)
    pygame.draw.circle(screen,(0,180,255),(meter_x,meter_y),radius,2)

# Silver Ring
    pygame.draw.circle(screen,(220,220,220),(meter_x,meter_y),radius-5,3)

    num_font = pygame.font.SysFont("Arial",12,True)

# White Ticks
    for i in range(41):

        angle = math.radians(160 + i*5)

        x1 = meter_x + math.cos(angle)*(radius-8)
        y1 = meter_y + math.sin(angle)*(radius-8)

        if i%2==0:
            x2 = meter_x + math.cos(angle)*(radius-22)
            y2 = meter_y + math.sin(angle)*(radius-22)
        else:
            x2 = meter_x + math.cos(angle)*(radius-16)
            y2 = meter_y + math.sin(angle)*(radius-16)

        pygame.draw.line(screen,(255,255,255),(x1,y1),(x2,y2),2)

    # Numbers 0-200
    for s in range(0,201,20):

        angle = math.radians(160 + s)

        tx = meter_x + math.cos(angle)*(radius-35)
        ty = meter_y + math.sin(angle)*(radius-35)

        txt = num_font.render(str(s),True,(255,255,255))
        screen.blit(txt,(tx-8,ty-8))

# Convert Game Speed to Meter
    meter_speed = int((speed-8)/12*200)
    meter_speed=max(0,min(200,meter_speed))

# Needle
    needle_angle = math.radians(160 + meter_speed)

    nx = meter_x + math.cos(needle_angle)*(radius-28)
    ny = meter_y + math.sin(needle_angle)*(radius-28)

    pygame.draw.line(
        screen,
        (255,0,0),
        (meter_x,meter_y),
        (nx,ny),
        4
    )

    pygame.draw.circle(screen,(255,255,255),(meter_x,meter_y),6)

# Center Display
    speed_font = pygame.font.SysFont("Arial",18,True)

    screen.blit(
        speed_font.render(str(meter_speed),True,(255,255,0)),
        (meter_x-12,meter_y+15)
)

    screen.blit(
        pygame.font.SysFont("Arial",11).render("KM/H",True,(180,180,180)),
        (meter_x-18,meter_y+35)
    )
    
    # Fuel

    pygame.draw.rect(screen,(70,70,70),(20,130,110,10))

    pygame.draw.rect(screen,(0,255,0),(20,130,int(fuel),10))

    fuel_txt=pygame.font.SysFont("Arial",14).render("FUEL",True,(255,255,255))

    screen.blit(fuel_txt,(20,112))


    # Engine Temp

    pygame.draw.rect(screen,(70,70,70),(20,160,110,10))

    color=(0,255,0)

    if engine_temp>60:
        color=(255,180,0)

    if engine_temp>85:
        color=(255,0,0)

    pygame.draw.rect(screen,color,(20,160,int(engine_temp),10))

    temp_txt=pygame.font.SysFont("Arial",14).render("TEMP",True,(255,255,255))

    screen.blit(temp_txt,(20,142))

# ================================================

# ===============================================

    pygame.display.update()

pygame.quit()