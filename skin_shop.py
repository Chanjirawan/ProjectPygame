import pygame
import sys

pygame.init()

# -------------------------
# WINDOW
# -------------------------
width = 500
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Skin Shop")

clock = pygame.time.Clock()

# -------------------------
# COLORS
# -------------------------
white = (255, 255, 255)
yellow = (255, 220, 0)
red = (200, 40, 40)
dark = (30, 30, 40)
green = (40, 200, 80)

# -------------------------
# FONTS
# -------------------------
font_small = pygame.font.Font(None, 28)
font_big = pygame.font.Font(None, 50)

# -------------------------
# COINS
# -------------------------
coins = 7

# -------------------------
# LOAD CAR IMAGES
# -------------------------
car_skins = [
    pygame.image.load("images/car.png"),
    pygame.image.load("images/car_blue.png"),
    pygame.image.load("images/car_red.png"),
]

# -------------------------
# SKIN DATA
# -------------------------
skins = [
    {"name": "Default", "price": 0, "owned": True},
    {"name": "Blue Racer", "price": 5, "owned": False},
    {"name": "Red Beast", "price": 10, "owned": False},
]

current_skin = 0
preview_skin = 0

# -------------------------
# ANIMATION
# -------------------------
rotation = 0
select_flash = 0


# -------------------------
# DRAW LOCK ICON
# -------------------------
def draw_lock():

    lock_text = font_big.render("LOCKED", True, red)
    rect = lock_text.get_rect(center=(width / 2, height / 2 + 120))
    screen.blit(lock_text, rect)


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
def skin_shop():

    global preview_skin
    global coins
    global rotation
    global select_flash
    global current_skin

    running = True

    while running:

        clock.tick(60)

        screen.fill(dark)

        # title
        title = font_big.render("CAR SKIN SHOP", True, white)
        screen.blit(title, (width / 2 - title.get_width() / 2, 60))

        # coins
        coin_text = font_small.render(f"Coins : {coins}", True, yellow)
        screen.blit(coin_text, (20, 20))

        # rotation preview
        rotation += 1

        image = pygame.transform.scale(car_skins[preview_skin], (120, 180))
        image = pygame.transform.rotate(image, rotation)

        rect = image.get_rect(center=(width / 2, height / 2))

        screen.blit(image, rect)

        # skin name
        name = skins[preview_skin]["name"]
        name_txt = font_small.render(name, True, white)
        screen.blit(name_txt, (width / 2 - name_txt.get_width() / 2, height / 2 + 110))

        # price / owned
        if skins[preview_skin]["owned"]:

            owned = font_small.render("OWNED", True, green)
            screen.blit(owned, (width / 2 - owned.get_width() / 2, height / 2 + 140))

        else:

            price = skins[preview_skin]["price"]
            price_txt = font_small.render(f"PRICE : {price}", True, yellow)

            screen.blit(
                price_txt, (width / 2 - price_txt.get_width() / 2, height / 2 + 140)
            )

            draw_lock()

        # controls
        controls = font_small.render(
            "LEFT RIGHT = CHANGE | ENTER = BUY/SELECT | ESC = BACK", True, white
        )
        screen.blit(controls, (width / 2 - controls.get_width() / 2, height - 80))

        pygame.display.update()

        # -------------------------
        # EVENTS
        # -------------------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # next skin
                if event.key == pygame.K_RIGHT:

                    preview_skin += 1

                    if preview_skin >= len(car_skins):
                        preview_skin = 0

                # previous skin
                if event.key == pygame.K_LEFT:

                    preview_skin -= 1

                    if preview_skin < 0:
                        preview_skin = len(car_skins) - 1

                # buy / select
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

                            buy_animation()

                # exit
                if event.key == pygame.K_ESCAPE:

                    running = False


# -------------------------
# RUN TEST
# -------------------------
if __name__ == "__main__":
    skin_shop()
