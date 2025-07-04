import pygame
import random
import sys
import json, os

class DataBase:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            self.set_data(data={
                'money': 0,
                'selected_ship': 0,
                'purchased_ships': [0]
            })

    def get_data(self) -> dict:
        with open(self.path, "r", encoding='utf-8') as file:
            return json.load(fp=file)

    def set_data(self, data: dict):
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False, sort_keys=True)

db = DataBase('data.json')
db_data = db.get_data()

selected_player_index = db_data.get("selected_ship", 0)
purchased_ships = db_data.get("purchased_ships", [0])
money = db_data['money']

pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Загрузка изображений
def load_image(path, width, height):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, (width, height))
    return img

PLAYER_SIZE = (50, 80)
PLAYER1_SIZE = (75, 80)
ENEMY_SIZE = (60, 40)
BULLET_SIZE = (5, 15)

BACKGROUND = pygame.image.load("background.png")
PLAYER_IMAGES = [
    load_image("player.png", *PLAYER_SIZE),
    load_image("player1.png", *PLAYER_SIZE),
    load_image("player2.png", *PLAYER1_SIZE)
]
ENEMY_IMG = load_image("enemy.png", *ENEMY_SIZE)
BULLET_IMG = pygame.Surface(BULLET_SIZE)
BULLET_IMG.fill((255, 255, 0))

FONT = pygame.font.SysFont("arial", 30)

player_img = PLAYER_IMAGES[selected_player_index]
player_rect = player_img.get_rect(center=(WIDTH//2, HEIGHT - PLAYER_SIZE[1]))

bullets = []
enemies = []

score = 0
missed = 0

shop_prices = [0, 100, 200]

ENEMY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMY_EVENT, 1000)

clock = pygame.time.Clock()

# Состояния игры
STATE_MENU = "menu"
STATE_GAME = "game"
STATE_SHOP = "shop"
STATE_WIN = "win"
STATE_LOSE = "lose"

state = STATE_MENU

def draw_button(text, x, y, w, h):
    pygame.draw.rect(WINDOW, (0, 128, 255), (x, y, w, h))
    label = FONT.render(text, True, (255, 255, 255))
    label_x = x + (w - label.get_width()) // 2
    label_y = y + (h - label.get_height()) // 2
    WINDOW.blit(label, (label_x, label_y))
    return pygame.Rect(x, y, w, h)

def reset_game():
    global player_img, player_rect, bullets, enemies, score, missed
    player_img = PLAYER_IMAGES[db_data.get('selected_ship', 0)]
    player_rect = player_img.get_rect(center=(WIDTH//2, HEIGHT - PLAYER_SIZE[1]))
    bullets.clear()
    enemies.clear()
    score = 0
    missed = 0

def menu_screen():
    global play_button, shop_button

    WINDOW.blit(BACKGROUND, (0, 0))
    title = FONT.render("Space Shooter", True, (255, 255, 255))
    WINDOW.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    play_button = draw_button("Играть", WIDTH//2 - 100, 250, 200, 50)
    shop_button = draw_button("Магазин", WIDTH//2 - 100, 320, 200, 50)
    money_text = FONT.render(f"Баланс: {money}", True, (255, 255, 0))
    WINDOW.blit(money_text, (10, 10))

def shop_screen():
    global shop_buttons, back_button

    WINDOW.blit(BACKGROUND, (0, 0))
    shop_text = FONT.render("Магазин космических кораблей", True, (255, 255, 255))
    WINDOW.blit(shop_text, (WIDTH//2 - shop_text.get_width()//2, 50))
    shop_buttons = []
    for i, img in enumerate(PLAYER_IMAGES):
        WINDOW.blit(img, (100 + i*200, 150))
        if i in purchased_ships:
            text = FONT.render("Есть", True, (0, 255, 0))
        else:
            text = FONT.render(f"{shop_prices[i]} $", True, (255, 255, 0))
        WINDOW.blit(text, (100 + i*200, 250))
        rect = pygame.Rect(100 + i*200, 150, PLAYER_SIZE[0], PLAYER_SIZE[1])
        shop_buttons.append(rect)
    back_button = draw_button("Назад", 10, HEIGHT - 60, 120, 40)
    money_text = FONT.render(f"Баланс: {money}", True, (255, 255, 0))
    WINDOW.blit(money_text, (10, 10))

def game_screen():
    global missed, score, money, state

    WINDOW.blit(BACKGROUND, (0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_rect.left > 0:
        player_rect.x -= 10
    if keys[pygame.K_d] and player_rect.right < WIDTH:
        player_rect.x += 10
    if keys[pygame.K_w] and player_rect.y > 0:
        player_rect.y -= 5
    if keys[pygame.K_s] and player_rect.y < HEIGHT - 85:
        player_rect.y += 5

    for bullet in bullets[:]:
        bullet.y -= 7
        if bullet.bottom < 0:
            bullets.remove(bullet)

    for enemy in enemies[:]:
        enemy.y += 3
        if enemy.top > HEIGHT:
            enemies.remove(enemy)
            missed += 1

    for enemy in enemies[:]:
        for bullet in bullets[:]:
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
                money += 1
                db_data['money'] += 1
                db.set_data(db_data)

    WINDOW.blit(player_img, player_rect)
    for bullet in bullets:
        WINDOW.blit(BULLET_IMG, bullet)
    for enemy in enemies:
        WINDOW.blit(ENEMY_IMG, enemy)

    score_text = FONT.render(f"Счет: {score}", True, (255, 255, 255))
    missed_text = FONT.render(f"Пропущено: {missed}", True, (255, 255, 255))
    money_text = FONT.render(f"Деньги: {money}", True, (255, 255, 0))
    WINDOW.blit(score_text, (10, 10))
    WINDOW.blit(missed_text, (10, 40))
    WINDOW.blit(money_text, (10, 70))

    if missed >= 10:
        state = STATE_LOSE
    elif score >= 50:
        state = STATE_WIN

def win_screen():
    win_text = FONT.render("Вы выиграли! Нажмите ENTER", True, (0, 255, 0))
    WINDOW.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2))

def lose_screen():
    lose_text = FONT.render("Вы проиграли! Нажмите ENTER", True, (255, 0, 0))
    WINDOW.blit(lose_text, (WIDTH//2 - lose_text.get_width()//2, HEIGHT//2))

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == STATE_GAME:
            if event.type == ENEMY_EVENT:
                enemy_rect = ENEMY_IMG.get_rect(midtop=(random.randint(50, WIDTH-50), 0))
                enemies.append(enemy_rect)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_rect = BULLET_IMG.get_rect(midbottom=player_rect.midtop)
                    bullets.append(bullet_rect)

        elif state == STATE_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if play_button.collidepoint(mx, my):
                    reset_game()
                    state = STATE_GAME
                elif shop_button.collidepoint(mx, my):
                    state = STATE_SHOP

        elif state == STATE_SHOP:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for i, rect in enumerate(shop_buttons):
                    if rect.collidepoint(mx, my):
                        if i in purchased_ships:
                            selected_player_index = i
                            db_data['selected_ship'] = i
                            db.set_data(db_data)
                        elif money >= shop_prices[i]:
                            money -= shop_prices[i]
                            db_data['money'] -= shop_prices[i]
                            purchased_ships.append(i)
                            db_data['purchased_ships'] = purchased_ships
                            selected_player_index = i
                            db_data['selected_ship'] = i
                            db.set_data(db_data)
                if back_button.collidepoint(mx, my):
                    state = STATE_MENU

        elif state in [STATE_WIN, STATE_LOSE]:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                state = STATE_MENU

    if state == STATE_MENU:
        menu_screen()
    elif state == STATE_SHOP:
        shop_screen()
    elif state == STATE_GAME:
        game_screen()
    elif state == STATE_WIN:
        win_screen()
    elif state == STATE_LOSE:
        lose_screen()

    pygame.display.flip()

pygame.quit()
sys.exit()
