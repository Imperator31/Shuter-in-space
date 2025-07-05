import pygame
import random
import time

pygame.init()

RED = (255, 0, 0)
GREEN = (0, 255, 51)
BlUE = (0, 0, 255)
ORANGE = (255, 123, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
LIGHT_GREEN = (200, 255, 200)
LIGHT_RED = (250, 128, 114)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 100)
LIGHT_BLUE = (80, 80, 255)

background = (174, 237, 232)
window = pygame.display.set_mode((500, 500))
fps = pygame.time.Clock()


class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)  # прямоугольник
        self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(window, self.fill_color, self.rect)

    def outline(self, frame_color, thickness):  # обводка существующего прямоугольника
        pygame.draw.rect(window, frame_color, self.rect, thickness)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def colliderect(self, rect):
        return self.rect.colliderect(rect)


class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


ball = Picture('police (1).png', 160, 200, 50, 50)
platform_x = 200
platform_y = 330
platform = Picture('vodka.png', platform_x, platform_y, 100, 30)

start_x = 5
start_y = 5

monster_count = 9
monsters = []
for i in range(3):
    y = start_y + 55 * i
    x = start_x + 27.5 * i
    for j in range(monster_count):
        monsters.append(Picture(random.choice(['bomj.png', 'bomj_1.png']), x, y, 50, 50))
        x += 55
    monster_count -= 1

move_left = False
move_right = False
game_over = False
ball_x = 3
ball_y = 3

while not game_over:
    window.fill(background)
    ball.draw()
    platform.draw()
    for monster in monsters:
        if monster.colliderect(ball.rect):
            monsters.remove(monster)
            ball_y = -ball_y
        else:
            monster.draw()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
        pass
    if move_right:
        platform.rect.x += 3
    if move_left:
        platform.rect.x -= 3
    ball.rect.x += ball_x
    ball.rect.y += ball_y
    if ball.colliderect(platform.rect):
        ball_y = -ball_y

    if ball.rect.y < 0:
        ball_y = -ball_y

    if ball.rect.x > 450 or ball.rect.x < 0:
        ball_x = -ball_x

    if ball.rect.y > (platform_y + 20):
        end_text = Label(150, 200, 50, 50, background)
        end_text.set_text('YOU LOSE', 60, (255, 0, 0))
        end_text.draw(10, 10)
        game_over = True
    if len(monsters) == 0:
        end_text = Label(150, 200, 50, 50, background)
        end_text.set_text('YOU WIN', 60, (0, 200, 0))
        end_text.draw(10, 10)
        game_over = True

    pygame.display.update()
    fps.tick(40)

pygame.display.update()

