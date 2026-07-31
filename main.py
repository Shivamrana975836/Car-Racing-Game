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
player_mask = pygame.mask.from_surface(player)
enemy_mask = pygame.mask.from_surface(enemy)

# Coin Icon
coin_img = pygame.image.load("coin.png").convert_alpha()
coin_img = pygame.transform.smoothscale(coin_img,(26,26))

fuel_img = pygame.image.load("fuel.png").convert_alpha()
fuel_img = pygame.transform.smoothscale(fuel_img,(34,40))


# ===== Explosion =====

explosion_sheet = pygame.image.load(
    "explosion effect.png"
).convert_alpha()


EXP_SIZE = 256

explosion_frames = []

for row in range(4):
    for col in range(4):

        frame = explosion_sheet.subsurface(
            (
                col*EXP_SIZE,
                row*EXP_SIZE,
                EXP_SIZE,
                EXP_SIZE
            )
        )

        frame = pygame.transform.smoothscale(
            frame,
            (150,150)
        )

        explosion_frames.append(frame)


explosion_index = 0
exploding = False
explosion_x = 0
explosion_y = 0
explosion_timer = 0

# Player
car_x=220
car_y=560
car_speed=7

# Enemy
lanes=[110,180,250,320]
# Multiple Enemies
enemies = []

for i in range(4):
    enemies.append({
        "x": random.choice(lanes),
        "y": -200 * (i + 1)
    })

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
score = 0
speed = 8

coins = 0
fuel = 100
engine_temp = 25
fuel_timer = pygame.time.get_ticks()
needle_speed = 0
overheat_timer = None
warning_timer = None
engine_warning = False

coin_x = random.choice(lanes) + 20
coin_y = -300
coin_angle = 0
#fuel variable
fuel_x = random.choice(lanes) + 15
fuel_y = -700


# ===========================
# DRAW BACKGROUND
# ===========================

def draw_background():

    screen.fill((8,10,30))

    pygame.draw.circle(
        screen,
        (240,240,200),
        (420,80),
        35
    )

    for s in stars:
        pygame.draw.circle(
            screen,
            (255,255,255),
            (s[0],s[1]),
            s[2]
        )

    pygame.draw.rect(
        screen,
        (20,90,20),
        (0,0,70,HEIGHT)
    )

    pygame.draw.rect(
        screen,
        (20,90,20),
        (430,0,70,HEIGHT)
    )

    pygame.draw.rect(
        screen,
        (120,120,120),
        (70,0,15,HEIGHT)
    )

    pygame.draw.rect(
        screen,
        (120,120,120),
        (415,0,15,HEIGHT)
    )

# ===========================
# DRAW OBJECTS
# ===========================

def draw_objects():

    global coin_angle

    # Road
    screen.blit(road,(70,road_y-HEIGHT))
    screen.blit(road,(70,road_y))

    # Trees
    for y in range(-200,HEIGHT+200,200):
        screen.blit(tree,(0,y+tree_y))
        screen.blit(tree,(420,y+100+tree_y))

    # Enemy
    for e in enemies:
        screen.blit(enemy, (e["x"], e["y"]))
    # Player
    if not exploding:
        screen.blit(player,(car_x,car_y))
    # Explosion Animation

    if exploding:

        screen.blit(
            explosion_frames[explosion_index],
            (explosion_x, explosion_y)
        )

    # Coin
    coin_angle += 8

    spin_coin = pygame.transform.rotozoom(
        coin_img,
        coin_angle,
        1
    )

    coin_rect_img = spin_coin.get_rect(
        center=(coin_x,coin_y)
    )

    screen.blit(spin_coin, coin_rect_img)
    screen.blit(fuel_img,(fuel_x,fuel_y))
    
# ===========================
# COLLISIONS
# ===========================

def check_collision():

    global game_over
    global exploding
    global explosion_index
    global explosion_x
    global explosion_y
    global explosion_timer
    global coins
    global coin_x
    global coin_y
    global fuel
    global fuel_x
    global fuel_y
    global overheat_timer
    global warning_timer
    global engine_warning
    if exploding:
        return

    # Coin ke liye player rectangle
    player_rect = pygame.Rect(
        car_x,
        car_y,
        player.get_width(),
        player.get_height()
    )

    # Car collision (Mask)
    for e in enemies:

        offset = (
            int(e["x"] - car_x),
            int(e["y"] - car_y)
        )

        if player_mask.overlap(enemy_mask, offset):
            
            exploding = True
            explosion_index = 0
            explosion_x = car_x - 58
            explosion_y = car_y - 35
            
            explosion_timer = pygame.time.get_ticks()
            return

    # Coin collision (Rectangle)
    coin_rect = pygame.Rect(
        coin_x - 12,
        coin_y - 12,
        24,
        24
    )

    if player_rect.colliderect(coin_rect):

        coins += 1

        coin_y = random.randint(-800,-250)
        coin_x = random.choice(lanes)+20
        
    fuel_rect = pygame.Rect(
    fuel_x,
    fuel_y,
    34,
    40
)

    if player_rect.colliderect(fuel_rect):

        fuel = min(fuel + 20, 100)

        fuel_y = random.randint(-1200, -500)
        fuel_x = random.choice(lanes) + 15
# ===========================
# DRAW DASHBOARD
# ===========================

def draw_dashboard():

    meter_x = 95
    meter_y = 150
    radius = 78

    glass = pygame.Surface((radius*2,radius*2),pygame.SRCALPHA)

    pygame.draw.circle(
        glass,
        (10,10,10,35),
        (radius,radius),
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

    # Numbers
    for s in range(0,201,20):

        angle = math.radians(160 + s)

        tx = meter_x + math.cos(angle)*(radius-35)
        ty = meter_y + math.sin(angle)*(radius-35)

        txt = num_font.render(str(s),True,(255,255,255))
        screen.blit(txt,(tx-8,ty-8))

    meter_speed = int((speed-8)/12*200)
    meter_speed = max(0,min(200,meter_speed))

    needle_angle = math.radians(160 + needle_speed)

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

    speed_font = pygame.font.SysFont("Arial",18,True)

    screen.blit(
        speed_font.render(str(meter_speed),True,(255,255,0)),
        (meter_x-12,meter_y+15)
    )

    screen.blit(
        pygame.font.SysFont("Arial",11).render("KM/H",True,(180,180,180)),
        (meter_x-18,meter_y+35)
    )

    # Fuel Bar
    pygame.draw.rect(screen,(70,70,70),(20,130,110,10))
    pygame.draw.rect(screen,(0,255,0),(20,130,int(fuel),10))

    # Engine Temp
    pygame.draw.rect(screen,(70,70,70),(20,160,110,10))

    color=(0,255,0)

    if engine_temp>60:
        color=(255,180,0)

    if engine_temp>85:
        color=(255,0,0)

    pygame.draw.rect(screen,color,(20,160,int(engine_temp),10))
    
# ===========================
# DRAW HUD
# ===========================

def draw_hud():

    # Score
    screen.blit(
        font.render(f"Score : {score}",True,(255,255,255)),
        (20,20)
    )

    # High Score
    high_text = font.render(
        f"High : {high_score}",
        True,
        (0,255,0)
    )

    screen.blit(
        high_text,
        (WIDTH-high_text.get_width()-20,20)
    )

    # Coin Glow
    coin_glow = pygame.Surface((40,40),pygame.SRCALPHA)

    pygame.draw.circle(
        coin_glow,
        (255,220,0,70),
        (20,20),
        18
    )

    screen.blit(coin_glow,(445,50))
    screen.blit(coin_img,(452,57))

    coin_font = pygame.font.SysFont(
        "Arial",
        16,
        True
    )

    screen.blit(
        coin_font.render(
            str(coins),
            True,
            (255,255,255)
        ),
        (456,82)
    )
    
    screen.blit(fuel_img,(448,110))

    screen.blit(
        coin_font.render(
            str(int(fuel)),
            True,
            (0,255,0)
        ),
        (456,145)
    )
    
# ===========================
# UPDATE GAME
# ===========================

def update_game():

    global speed
    global engine_temp
    global fuel
    global fuel_timer
    global needle_speed
    global coin_x
    global coin_y
    global score
    global high_score
    global road_y
    global tree_y
    global game_over
    global fuel_x
    global fuel_y

    global exploding
    global explosion_index
    global explosion_x
    global explosion_y
    global explosion_timer

    global overheat_timer
    global warning_timer
    global engine_warning

    if exploding:
        return

    # =========================
    # SPEED LIMIT
    # =========================

    speed = max(8, min(speed, 28))

    current_time = pygame.time.get_ticks()

    # =========================
    # ENGINE SYSTEM
    # =========================

    if speed >= 24:          # 160 KM/H+

        if overheat_timer is None:
            overheat_timer = current_time

        elapsed = current_time - overheat_timer

        # 20 sec me temp red
        engine_temp = min(100, 25 + (elapsed / 20000) * 75)

        if elapsed >= 20000:

            engine_warning = True

            if warning_timer is None:
                warning_timer = current_time

            # Warning ke 3 sec baad blast

            if current_time - warning_timer >= 3000:

                exploding = True
                explosion_index = 0
                explosion_x = car_x - 58
                explosion_y = car_y - 35
                explosion_timer = current_time

                return

    else:

        overheat_timer = None
        warning_timer = None
        engine_warning = False

        engine_temp = max(25, engine_temp - 0.5)

    # =========================
    # FUEL
    # =========================

    if current_time - fuel_timer > 400:

        fuel -= 0.15
        fuel_timer = current_time

    fuel = max(0, min(fuel, 100))

    if fuel <= 0:
        game_over = True
        return

    # =========================
    # SPEEDOMETER NEEDLE
    # =========================

    meter_speed = int((speed - 8) / 20 * 200)
    meter_speed = max(0, min(200, meter_speed))

    needle_speed += (meter_speed - needle_speed) * 0.08

    # =========================
    # ENEMIES
    # =========================

    for e in enemies:

        e["y"] += speed

        if e["y"] > HEIGHT:

            e["y"] = random.randint(-700, -150)
            e["x"] = random.choice(lanes)

            score += 1

    # =========================
    # COIN
    # =========================

    coin_y += speed

    if coin_y > HEIGHT:

        coin_y = random.randint(-800, -250)
        coin_x = random.choice(lanes) + 20

    # =========================
    # FUEL CAN
    # =========================

    fuel_y += speed

    if fuel_y > HEIGHT:

        fuel_y = random.randint(-1200, -500)
        fuel_x = random.choice(lanes) + 15

    # =========================
    # HIGH SCORE
    # =========================

    if score > high_score:

        high_score = score

        with open("highscore.txt", "w") as f:
            f.write(str(high_score))

    # =========================
    # ROAD
    # =========================

    road_y += speed

    if road_y >= HEIGHT:
        road_y = 0

    tree_y += speed * 0.5

    if tree_y >= 200:
        tree_y = 0
    
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

            car_x = 220

            enemies.clear()

            for i in range(4):
                enemies.append({
                    "x": random.choice(lanes),
                    "y": -200 * (i + 1)
                })

            score = 0
            speed = 8

            fuel = 100
            engine_temp = 25
            overheat_timer = None
            warning_timer = None
            engine_warning = False
            coins = 0

            coin_x = random.choice(lanes) + 20
            coin_y = -300

            fuel_x = random.choice(lanes) + 15
            fuel_y = -700
            
            exploding = False
            explosion_index = 0
            

            game_over = False

        continue

    keys=pygame.key.get_pressed()

    if (keys[pygame.K_LEFT] or move_left) and car_x > 80:
        car_x -= car_speed

    if (keys[pygame.K_RIGHT] or move_right) and car_x < 350:
        car_x += car_speed

    
    if keys[pygame.K_UP]:
        speed += 0.15

    if keys[pygame.K_DOWN]:
        speed -= 0.25

    if boost:
        speed += 0.25

    speed = max(8, min(speed, 28))
    
        
        
        
    # Background
    update_game()
    check_collision()
    draw_background()
    
    # Explosion Update

    if exploding:

        if pygame.time.get_ticks() - explosion_timer > 60:

            explosion_index += 1
            explosion_timer = pygame.time.get_ticks()


            if explosion_index >= len(explosion_frames):

                exploding = False
                game_over = True

                explosion_index = 0

    draw_objects()
    draw_dashboard()
    draw_hud()
    if engine_warning:

        warn = pygame.font.SysFont("Arial", 28, True)

        text = warn.render("⚠ ENGINE HOT", True, (255,0,0))

        screen.blit(text, (120, 90))
    
    
    pygame.display.update()
    # ===========================
# DRAW PLAYER ENEMY COIN
# ===========================
pygame.quit()