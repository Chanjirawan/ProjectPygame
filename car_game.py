import pygame
import random
import os
import sys
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# -------------------------
# WINDOW SETTINGS
# -------------------------
width = 500
height = 600
fullscreen = False

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Racer Pro")

clock = pygame.time.Clock()
fps = 60

# -------------------------
# COLORS
# -------------------------
gray = (100, 100, 100)
green = (76, 208, 56)
white = (255, 255, 255)
yellow = (255, 232, 0)
red = (200, 0, 0)
dark_blue = (20, 20, 40)

# -------------------------
# GAME STATES
# -------------------------
night_mode = False
rain_mode = False

# -------------------------
# ROAD
# -------------------------
road_width = 300
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

marker_width = 10
marker_height = 50
lane_marker_move_y = 0

# -------------------------
# GAME VARIABLES
# -------------------------
speed = 3
score = 0
shield_count = 0

player_x = center_lane
player_y = 500

# -------------------------
# CAR TILT
# -------------------------
tilt_angle = 0
tilt_speed = 6
max_tilt = 15

# -------------------------
# FILES
# -------------------------
leaderboard_file = "leaderboard.txt"

if not os.path.exists(leaderboard_file):
    with open(leaderboard_file, "w") as f:
        f.write("0\n0\n0\n0\n0")

# -------------------------
# MUSIC
# -------------------------
try:
    pygame.mixer.music.load("sounds/music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except:
    print("music not found")

try:
    crash_sound = pygame.mixer.Sound("sounds/crash.wav")
except:
    crash_sound = None

# -------------------------
# FONTS
# -------------------------
font_small = pygame.font.Font(None, 28)
font_big = pygame.font.Font(None, 50)
# -------------------------
# MENU BACKGROUND
# -------------------------
try:
    menu_bg = pygame.image.load("images/menu_bg.png")
    menu_bg = pygame.transform.scale(menu_bg, (width, height))
except:
    menu_bg = None


def draw_gradient():

    for y in range(height):

        color = (30 + y // 6, 30 + y // 6, 70 + y // 4)

        pygame.draw.line(screen, color, (0, y), (width, y))


# -------------------------
# LOAD IMAGES
# -------------------------
car_skins = [
    pygame.image.load("images/car.png"),
    pygame.image.load("images/car_red.png"),
    pygame.image.load("images/car_blue.png"),
]
preview_skin = 0
current_skin = 0

vehicle_images = [
    pygame.image.load("images/pickup_truck.png"),
    pygame.image.load("images/semi_trailer.png"),
    pygame.image.load("images/taxi.png"),
    pygame.image.load("images/van.png"),
]

shield_img = pygame.image.load("images/shield.png")
shield_img = pygame.transform.scale(shield_img, (40, 40))
shield_icon = pygame.image.load("images/shield.png")
shield_icon = pygame.transform.scale(shield_icon, (30, 30))
# -------------------------
# CAR SIZE
# -------------------------
car_width = 75
car_height = 110

# -------------------------
# EXPLOSION FRAMES
# -------------------------
explosion_frames = []
for i in range(1, 6):
    img = pygame.image.load(f"images/explosion{i}.png")
    explosion_frames.append(img)

# -------------------------
# RAIN PARTICLES
# -------------------------
rain = []
for i in range(80):
    x = random.randint(0, width)
    y = random.randint(0, height)
    rain.append([x, y])


# -------------------------
# SPRITES
# -------------------------
class Vehicle(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        super().__init__()

        self.image = pygame.transform.scale(image, (car_width, car_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


class PlayerVehicle(Vehicle):

    def __init__(self, x, y):
        image = car_skins[current_skin]
        super().__init__(image, x, y)

        self.original_image = self.image
        self.angle = 0

    def update_skin(self):

        image = car_skins[current_skin]
        self.original_image = pygame.transform.scale(image, (car_width, car_height))
        self.image = self.original_image

    def tilt(self, angle):

        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)


class PowerUp(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = shield_img

        self.rect = self.image.get_rect()
        self.rect.center = [random.choice(lanes), -50]

    def update(self):
        self.rect.y += speed


# -------------------------
# GROUPS
# -------------------------
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()

player = PlayerVehicle(player_x, player_y)
player_group.add(player)


# -------------------------
# LEADERBOARD
# -------------------------
def load_scores():

    with open(leaderboard_file) as f:
        scores = [int(x.strip()) for x in f.readlines()]
    return scores


def save_score(new_score):

    scores = load_scores()
    scores.append(new_score)
    scores.sort(reverse=True)
    scores = scores[:5]

    with open(leaderboard_file, "w") as f:
        for s in scores:
            f.write(str(s) + "\n")


# -------------------------
# DRAW RAIN
# -------------------------
def draw_rain():

    for drop in rain:
        pygame.draw.line(
            screen, (180, 180, 255), (drop[0], drop[1]), (drop[0], drop[1] + 5)
        )
        drop[1] += 10
        if drop[1] > height:
            drop[1] = 0
            drop[0] = random.randint(0, width)


# -------------------------
# EXPLOSION ANIMATION
# -------------------------
def play_explosion(x, y):

    for frame in explosion_frames:

        screen.blit(frame, (x - 40, y - 40))
        pygame.display.update()
        pygame.time.delay(80)


# -------------------------
# SETTINGS MENU
# -------------------------
def settings_menu():

    global night_mode, rain_mode, fullscreen

    volume = pygame.mixer.music.get_volume()

    while True:

        screen.fill((40, 40, 40))

        screen.blit(font_big.render("SETTINGS", True, white), (150, 120))

        screen.blit(font_small.render("UP/DOWN : Volume", True, white), (150, 220))
        screen.blit(font_small.render("N : Toggle Night Mode", True, white), (150, 260))
        screen.blit(font_small.render("R : Toggle Rain", True, white), (150, 300))
        screen.blit(font_small.render("F : Fullscreen", True, white), (150, 340))
        screen.blit(font_small.render("ESC : Back", True, white), (150, 380))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    return

                if event.key == K_UP:
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)

                if event.key == K_DOWN:
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)

                if event.key == K_n:
                    night_mode = not night_mode

                if event.key == K_r:
                    rain_mode = not rain_mode

                if event.key == K_f:

                    fullscreen = not fullscreen

                    if fullscreen:
                        pygame.display.set_mode((width, height), FULLSCREEN)
                    else:
                        pygame.display.set_mode((width, height))


# -------------------------
# SKIN MENU
# -------------------------
def skin_menu():

    global preview_skin, current_skin

    running = True

    while running:

        screen.fill((30, 30, 40))

        title = font_big.render("SELECT CAR SKIN", True, white)
        screen.blit(title, (width / 2 - title.get_width() / 2, 80))

        # preview car
        preview_image = pygame.transform.scale(car_skins[preview_skin], (120, 180))
        preview_rect = preview_image.get_rect(center=(width / 2, height / 2))

        screen.blit(preview_image, preview_rect)

        txt = font_small.render(
            "LEFT/RIGHT = Change  ENTER = Select", True, (200, 200, 200)
        )
        screen.blit(txt, (width / 2 - txt.get_width() / 2, height - 150))

        back_txt = font_small.render("ESC = Back", True, (200, 200, 200))
        screen.blit(back_txt, (width / 2 - back_txt.get_width() / 2, height - 110))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:
                    preview_skin += 1
                    if preview_skin >= len(car_skins):
                        preview_skin = 0

                if event.key == pygame.K_LEFT:
                    preview_skin -= 1
                    if preview_skin < 0:
                        preview_skin = len(car_skins) - 1

                if event.key == pygame.K_RETURN:
                    current_skin = preview_skin
                    player.update_skin()

                if event.key == pygame.K_ESCAPE:
                    running = False


# -------------------------
# LEADERBOARD SCREEN
# -------------------------
def leaderboard_screen():

    scores = load_scores()

    while True:

        screen.fill(gray)

        screen.blit(font_big.render("LEADERBOARD", True, white), (120, 120))

        y = 220
        for i, s in enumerate(scores):

            text = font_small.render(f"{i+1}. {s}", True, white)
            screen.blit(text, (220, y))
            y += 40

        screen.blit(font_small.render("ESC to return", True, white), (170, 450))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return


# -------------------------
# ANIMATED BUTTON
# -------------------------
class AnimatedButton:

    def __init__(self, text, x, y, w, h):

        self.text = text
        self.base_rect = pygame.Rect(x, y, w, h)
        self.rect = self.base_rect.copy()

        self.scale = 1.0
        self.hover = False

    def update(self):

        mouse = pygame.mouse.get_pos()

        if self.base_rect.collidepoint(mouse):

            self.hover = True
            self.scale = min(1.1, self.scale + 0.05)

        else:

            self.hover = False
            self.scale = max(1.0, self.scale - 0.05)

        self.rect.width = int(self.base_rect.width * self.scale)
        self.rect.height = int(self.base_rect.height * self.scale)

        self.rect.center = self.base_rect.center

    def draw(self):

        if self.hover:
            color = (220, 220, 220)
        else:
            color = (180, 180, 180)

        pygame.draw.rect(screen, color, self.rect, border_radius=10)

        text = font_small.render(self.text, True, (20, 20, 20))
        text_rect = text.get_rect(center=self.rect.center)

        screen.blit(text, text_rect)

    def clicked(self, event):

        if event.type == MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos):
                return True

        return False


# -------------------------
# START MENU (PRO UI)
# -------------------------
def start_menu():

    title_y = 140
    direction = 1

    start_btn = AnimatedButton("Start Game", 170, 250, 160, 40)
    settings_btn = AnimatedButton("Settings", 170, 300, 160, 40)
    skin_btn = AnimatedButton("Car Skin", 170, 350, 160, 40)
    leader_btn = AnimatedButton("Leaderboard", 170, 400, 160, 40)
    quit_btn = AnimatedButton("Quit", 170, 450, 160, 40)

    buttons = [start_btn, settings_btn, skin_btn, leader_btn, quit_btn]

    while True:

        clock.tick(60)

        draw_gradient()

        if menu_bg:
            screen.blit(menu_bg, (0, 0))

        # animated title
        title = font_big.render("CAR RACER PRO", True, white)
        title_rect = title.get_rect(center=(width // 2, title_y))
        screen.blit(title, title_rect)

        title_y += direction * 0.4

        if title_y > 150 or title_y < 130:
            direction *= -1

        # buttons
        for b in buttons:
            b.update()
            b.draw()

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                quit()

            if start_btn.clicked(event):
                return

            if settings_btn.clicked(event):
                settings_menu()

            if skin_btn.clicked(event):
                skin_menu()

            if leader_btn.clicked(event):
                leaderboard_screen()

            if quit_btn.clicked(event):
                pygame.quit()
                quit()


# -------------------------
# HUD
# -------------------------
def draw_hud():

    screen.blit(font_small.render(f"Score: {score}", True, white), (10, 10))
    screen.blit(font_small.render(f"Speed: {speed}", True, white), (10, 40))

    for i in range(shield_count):
      screen.blit(shield_icon, (width - 40 - i*35, 10))


# -------------------------
# START GAME
# -------------------------
start_menu()

# -------------------------
# GAME LOOP
# -------------------------
running = True

while running:

    clock.tick(fps)

    for event in pygame.event.get():

        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:

            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
                player.tilt(max_tilt)

            if event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100
                player.tilt(-max_tilt)

    # background
    if night_mode:
        screen.fill(dark_blue)
    else:
        screen.fill(green)

    pygame.draw.rect(screen, gray, (100, 0, road_width, height))
    pygame.draw.rect(screen, yellow, (95, 0, 10, height))
    pygame.draw.rect(screen, yellow, (395, 0, 10, height))

    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0

    for y in range(-100, height, 100):

        pygame.draw.rect(
            screen, white, (left_lane + 45, y + lane_marker_move_y, 10, 50)
        )
        pygame.draw.rect(
            screen, white, (center_lane + 45, y + lane_marker_move_y, 10, 50)
        )

    # rain
    if rain_mode:
        draw_rain()

    # add vehicles
    if len(vehicle_group) < 2:

        lane = random.choice(lanes)
        img = random.choice(vehicle_images)

        vehicle = Vehicle(img, lane, -100)
        vehicle_group.add(vehicle)

    # powerup
    if random.randint(1, 500) == 1:
        powerup_group.add(PowerUp())

    # move vehicles
    for vehicle in vehicle_group:

        vehicle.rect.y += speed

        if vehicle.rect.top > height:

            vehicle.kill()
            score += 1

            if score % 5 == 0:
                speed += 1

    powerup_group.update()

    # collision
    if pygame.sprite.spritecollide(player, vehicle_group, True):

        if shield_count > 0:
            shield_count -= 1
        else:

            if crash_sound:
                crash_sound.play()

            play_explosion(player.rect.centerx, player.rect.centery)

            save_score(score)

            running = False

    if pygame.sprite.spritecollide(player, powerup_group, True):
        shield_count += 1

    player_group.draw(screen)
    vehicle_group.draw(screen)
    powerup_group.draw(screen)

    # smooth return tilt
    if player.angle > 0:
        player.angle -= tilt_speed
    elif player.angle < 0:
        player.angle += tilt_speed

    player.image = pygame.transform.rotate(player.original_image, player.angle)
    player.rect = player.image.get_rect(center=player.rect.center)
    
    draw_hud()

    pygame.display.update()

pygame.quit()
