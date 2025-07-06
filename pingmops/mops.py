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
WIDTH = 1000
HEIGHT = 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
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


ball = Picture('ball.png', WIDTH // 2, HEIGHT // 2, 50, 50)
platform_1 = Picture('vodochka.png', 0 + 50, HEIGHT // 2, 30, 100)
platform_2 = Picture('vodochka.png', WIDTH - 80, HEIGHT // 2, 30, 100)
platforms = tuple([platform_1,platform_2])

score = 0
move_left_1 = False
move_right_1 = False
move_left_2 = False
move_right_2 = False
game_over = False
ball_x = random.choice([-2,2])
ball_y = random.choice([-2,2])

while not game_over:
    window.fill(background)
    pygame.display.set_caption(f'Speed - {abs(ball_x)}, Score - {score}')
    ball.draw()
    for index, platform in enumerate(platforms):
        platform.draw()
        if ball.colliderect(platform.rect):
            ball_x = -ball_x
            if index == 0:
                score += -1
            else:
                score += 1
            if abs(score) >= 10:
                game_over = True
            if ball_x > 0:
                ball_x += 0.1
            else:
                ball_x += -0.1
            if ball_y > 0:
                ball_y += 0.1
            else:
                ball_y += - 0.1

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                move_left_1 = True
            if event.key == pygame.K_s:
                move_right_1 = True
            if event.key == pygame.K_UP:
                move_left_2 = True
            if event.key == pygame.K_DOWN:
                move_right_2 = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                move_left_1 = False
            if event.key == pygame.K_s:
                move_right_1 = False
            if event.key == pygame.K_UP:
                move_left_2 = False
            if event.key == pygame.K_DOWN:
                move_right_2 = False
        pass
    if move_right_1:
        platform_1.rect.y += 10
    if move_left_1:
        platform_1.rect.y -= 10
    if move_right_2:
        platform_2.rect.y += 10
    if move_left_2:
        platform_2.rect.y -= 10
    ball.rect.x += ball_x
    ball.rect.y += ball_y
    if ball.rect.y < 0 or ball.rect.y > HEIGHT - 50:
        ball_y = -ball_y

    if ball.rect.x > WIDTH - 50 or ball.rect.x < 0:
        ball_x = -ball_x
        game_over = True
    fps.tick(40)
    pygame.display.update()

class TextRenderer:
    def __init__(self, screen, font_name='arial', font_size=30, color=(255, 255, 255)):
        self.screen = screen
        self.font = pygame.font.SysFont(font_name, font_size)
        self.color = color

    def draw_text(self, text, x, y, center=True):
        rendered_text = self.font.render(text, True, self.color)
        text_rect = rendered_text.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        self.screen.blit(rendered_text, text_rect)

win = ''
if score > 0:
    win = 'Выиграл Игрок2'
elif score < 0:
    win = 'Выиграл Игрок1'
else:
    win = 'Ничья'
text = TextRenderer(window)
while True:
    window.fill(GREEN)
    text.draw_text(f'Исход игры - {win}', WIDTH // 2, HEIGHT // 2)
    fps.tick(1)
    pygame.display.update()


