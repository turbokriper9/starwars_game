import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("starwars_game")

clock = pygame.time.Clock()

# Игрок
player = pygame.Rect(100, 100, 50, 50)
player_speed = 5
sprint_multiplier = 2
color = (0, 255, 0)

# Основной цикл
running = True
while running:
    dt = clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление
    speed = player_speed * (sprint_multiplier if keys[pygame.K_LSHIFT] else 1)
    if keys[pygame.K_w]: player.y -= speed
    if keys[pygame.K_s]: player.y += speed
    if keys[pygame.K_a]: player.x -= speed
    if keys[pygame.K_d]: player.x += speed

    # Отрисовка
    screen.fill((20, 20, 30))
    pygame.draw.rect(screen, color, player)
    pygame.display.flip()

pygame.quit()
sys.exit()
