import pygame
import sys


pygame.init()
boost_active = False
boost_timer = 0
cooldown = 0
# -------------------------
# WINDOW
# -------------------------
width = 500
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Skin Shop")

clock = pygame.time.Clock()

# -------------------------
# COLORS
# -------------------------
white = (255, 255, 255)
yellow = (255, 220, 0)
red = (200, 40, 40)
dark = (30, 30, 40)
green = (40, 200, 80)
blue = (80, 120, 255)
gray = (120, 120, 120)

# -------------------------
# FONTS
# -------------------------
font_small = pygame.font.Font(None, 28)
font_big = pygame.font.Font(None, 50)

# -------------------------
# LOAD CAR IMAGES
# -------------------------
car_skins = [
    pygame.image.load("images/car.png"),
    pygame.image.load("images/car_red.png"),
    pygame.image.load("images/car_blue.png"),
]

# -------------------------
# SKIN DATA
# -------------------------
skins = [
    {"name": "Default", "price": 0, "owned": True},
    {"name": "Red Beast", "price": 5, "owned": False},
    {"name": "Blue Racer", "price": 10, "owned": False},
]

current_skin = 0
preview_skin = 0

# -------------------------
# NITRO SYSTEM
# -------------------------
nitro = 100
nitro_max = 100

boost_active = False
boost_timer = 0
boost_duration = 120
cooldown = 0


# -------------------------
# DRAW LOCK
# -------------------------
def draw_lock():

    txt = font_big.render("LOCKED", True, red)
    rect = txt.get_rect(center=(width / 2, height / 2 + 120))
    screen.blit(txt, rect)


# -------------------------
# DRAW NITRO BAR
# -------------------------
def draw_nitro():

    pygame.draw.rect(screen, gray, (20, 20, 150, 15))

    fill = (nitro / nitro_max) * 150

    pygame.draw.rect(screen, blue, (20, 20, fill, 15))

    txt = font_small.render("Nitro", True, white)
    screen.blit(txt, (20, 0))


# -------------------------
# BOOST EFFECT
# -------------------------
def boost_effect(x, y):

    pygame.draw.circle(screen, (255, 120, 0), (x, y), 10)
    pygame.draw.circle(screen, (255, 60, 0), (x, y), 5)


# -------------------------
# BUY ANIMATION
# -------------------------
def buy_animation():

    for i in range(20):

        screen.fill(dark)

        txt = font_big.render("PURCHASED!", True, green)
        rect = txt.get_rect(center=(width / 2, height / 2))

        screen.blit(txt, rect)

        pygame.display.update()
        pygame.time.delay(40)


# -------------------------
# SELECT ANIMATION
# -------------------------
def select_animation():

    for i in range(10):

        screen.fill((50, 50, 70))

        txt = font_big.render("SELECTED", True, yellow)
        rect = txt.get_rect(center=(width / 2, height / 2))

        screen.blit(txt, rect)

        pygame.display.update()
        pygame.time.delay(40)


# -------------------------
# SKIN SHOP
# -------------------------
def skin_shop(coins, current_skin):

    global preview_skin
    global nitro
    global boost_active
    global boost_timer
    global cooldown

    preview_skin = current_skin

    rotation = 0
    running = True

    while running:

        clock.tick(60)
        screen.fill(dark)

        # TITLE
        title = font_big.render("CAR SKIN SHOP", True, white)
        screen.blit(title, (width / 2 - title.get_width() / 2, 60))

        # COINS
        coin_text = font_small.render(f"Coins : {coins}", True, yellow)
        screen.blit(coin_text, (20, 50))

        # NITRO BAR
        draw_nitro()

        # ROTATION
        rotation = (rotation + 1) % 360

        img = pygame.transform.scale(car_skins[preview_skin], (120, 180))
        rot = pygame.transform.rotate(img, rotation)

        rect = rot.get_rect(center=(width / 2, height / 2))
        screen.blit(rot, rect)

        # NAME
        name = skins[preview_skin]["name"]
        name_txt = font_small.render(name, True, white)
        screen.blit(name_txt, (width / 2 - name_txt.get_width() / 2, height / 2 + 110))

        # PRICE
        if skins[preview_skin]["owned"]:

            owned = font_small.render("OWNED", True, green)
            screen.blit(owned, (width / 2 - owned.get_width() / 2, height / 2 + 140))

        else:

            price = skins[preview_skin]["price"]

            price_txt = font_small.render(f"PRICE : {price}", True, yellow)
            screen.blit(
                price_txt,
                (width / 2 - price_txt.get_width() / 2, height / 2 + 140),
            )

            draw_lock()

        # CONTROLS
        controls1 = font_small.render(
            "LEFT RIGHT = CHANGE | ENTER = BUY/SELECT", True, white
        )

        controls2 = font_small.render(
            "SPACE = BOOST | ESC = BACK", True, white
        )

        screen.blit(controls1, (width/2 - controls1.get_width()/2, height-90))
        screen.blit(controls2, (width/2 - controls2.get_width()/2, height-60))

        # -------------------------
        # BOOST SYSTEM
        # -------------------------
        if boost_active:

            boost_timer += 1
            nitro -= 0.7

            boost_effect(int(width / 2), int(height / 2 + 90))

            if boost_timer > boost_duration or nitro <= 0:

                boost_active = False
                boost_timer = 0
                cooldown = 120

        else:

            if cooldown > 0:
                cooldown -= 1
            else:
                if nitro < nitro_max:
                    nitro += 0.3
                    nitro = min(nitro, nitro_max)

        # -------------------------
        # EVENTS
        # -------------------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

                    skin = skins[preview_skin]

                    if skin["owned"]:

                        current_skin = preview_skin
                        select_animation()

                    else:

                        price = skin["price"]

                        if coins >= price:

                            coins -= price
                            skin["owned"] = True
                            current_skin = preview_skin 
                            buy_animation()

                if event.key == pygame.K_SPACE:

                    if nitro > 20 and cooldown == 0:
                        boost_active = True

                if event.key == pygame.K_ESCAPE:
                    return coins, current_skin

        pygame.display.update()
