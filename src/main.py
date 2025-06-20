# src/main.py

import pygame
import sys
import os
import random

from settings import (
    WIDTH, HEIGHT, IMAGES_DIR, SOUNDS_DIR,
    FPS, START_COINS, ASTEROID_DAMAGE, BULLET_SPEED, EXPLOSION_SOUND
)
from menu import main_menu
from planet_select import select_planet
from shop import shop
from player import Player
from enemy import Enemy
from asteroid import Asteroid
from key import Key
from levels import LEVELS


def draw_health_bar(screen, current, maximum):
    """
    Рисует полосу здоровья игрока в верхнем левом углу.
    Ширина подогнана, чтобы не перекрывать таймер.
    """
    bar_width = WIDTH - 220
    bar_height = 20
    x, y = 10, 10

    # фон (красный)
    pygame.draw.rect(screen, (100, 0, 0),
                     (x, y, bar_width, bar_height))
    # заполнение (зелёный)
    fill = int(bar_width * current / maximum)
    pygame.draw.rect(screen, (0, 200, 0),
                     (x, y, fill, bar_height))


def draw_enemy_hp(screen, enemy):
    """
    Рисует полосу здоровья над каждым врагом.
    """
    bar_w = enemy.rect.width
    x = enemy.rect.x
    y = enemy.rect.y - 8
    # сначала фон
    pygame.draw.rect(screen, (100, 0, 0), (x, y, bar_w, 5))
    # затем заполненная часть
    ratio = enemy.health / enemy.max_health if enemy.max_health > 0 else 0
    pygame.draw.rect(screen, (200, 0, 0),
                     (x, y, int(bar_w * ratio), 5))


def spawn_enemies(cfg, player, all_sprites, enemies_group):
    """
    Спавнит врагов по конфигурации уровня.
    Возвращает общее количество созданных врагов.
    """
    total = 0
    for count in cfg['enemies'].values():
        for _ in range(count):
            pos = (random.randint(50, WIDTH - 50),
                   random.randint(-100, -50))
            enemy = Enemy(pos, player, boss=False)
            all_sprites.add(enemy)
            enemies_group.add(enemy)
            total += 1
    return total


def run_battle(screen, level_key, player, progress, font, clock):
    """
    Основной цикл боя на выбранной планете.
    Возвращает True при подборе ключа (уровень пройден),
    False при смерти или истечении времени.
    """
    # загрузка фона и музыки
    bg = pygame.image.load(
        os.path.join(IMAGES_DIR, f'bg_{level_key}.png')
    ).convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    music_file = f'music_{level_key}.mp3'
    if level_key in ('hoth', 'nal_hutta'):
        music_file = 'music_tatooine.mp3'
    pygame.mixer.music.load(
        os.path.join(SOUNDS_DIR, music_file)
    )
    pygame.mixer.music.play(-1)

    # сброс патронов в начале боя
    player.reload()

    # предзагрузить звук взрыва астероида
    explosion_sfx = pygame.mixer.Sound(EXPLOSION_SOUND)

    # группы спрайтов
    all_sprites = pygame.sprite.Group(player)
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    e_bullets = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    keys_group = pygame.sprite.Group()

    cfg = next(l for l in LEVELS if l['key'] == level_key)
    total_enemies = spawn_enemies(cfg, player, all_sprites, enemies)

    kills = 0
    boss_spawned = False
    key_spawned = False
    reload_start = None
    RELOAD_TIME = 2000  # миллисекунд

    start_time = pygame.time.get_ticks()
    TIME_LIMIT = 3 * 60 * 1000  # 3 минуты

    while True:
        dt = clock.tick(FPS)
        shoot = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # пробел — выстрел
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                shoot = True

        # обработка управления игроком
        keys = pygame.key.get_pressed()
        player.handle_input(keys)

        # выстрел игрока
        if shoot and player.ammo > 0:
            bullet = player.shoot(pygame.Vector2(0, -1))
            if bullet:
                bullet.velocity = pygame.Vector2(0, -BULLET_SPEED)
                bullets.add(bullet)
                all_sprites.add(bullet)
            # если кончились патроны — запомнить время
            if player.ammo == 0 and reload_start is None:
                reload_start = pygame.time.get_ticks()

        # авто-перезарядка по таймеру
        if reload_start and pygame.time.get_ticks() - reload_start >= RELOAD_TIME:
            player.reload()
            reload_start = None

        # спавн астероидов
        if random.random() < 0.005:
            asteroid = Asteroid()
            asteroids.add(asteroid)
            all_sprites.add(asteroid)

        # столкновение астероид→игрок
        for a in pygame.sprite.spritecollide(
                player, asteroids, True):
            player.take_damage(ASTEROID_DAMAGE)
            explosion_sfx.play()

        # обновление врагов и получение их выстрелов
        new_shots = []
        for enemy in list(enemies):
            shot = enemy.update()
            if shot:
                new_shots.append(shot)

        for shot in new_shots:
            vel = (shot.velocity or
                   (pygame.Vector2(player.rect.center) -
                    pygame.Vector2(shot.rect.center)
                    ).normalize() * BULLET_SPEED)
            shot.velocity = vel
            all_sprites.add(shot)
            e_bullets.add(shot)

        # обновление остальных спрайтов
        for spr in all_sprites:
            if not isinstance(spr, Enemy):
                spr.update()

        # попадания пуль игрока по врагам
        hits = pygame.sprite.groupcollide(
            bullets, enemies, True, False
        )
        for _, hit_list in hits.items():
            for en in hit_list:
                en.take_damage(10)
                if en.health <= 0:
                    kills += 1
                    player.coins += 50

        # попадания пуль по астероидам (только звук и монеты)
        hits_ast = pygame.sprite.groupcollide(
            bullets, asteroids, True, True
        )
        for lst in hits_ast.values():
            for _ in lst:
                player.coins += 3
                explosion_sfx.play()

        # попадания пуль врагов по игроку
        if pygame.sprite.spritecollide(player, e_bullets, True):
            player.take_damage(10)

        # спавн босса (на nal_hutta после заданного кол-ва убийств)
        if (cfg.get('boss_after') and
                kills >= cfg['boss_after'] and
                not boss_spawned):
            # два обычных + один босс
            for _ in range(2):
                e = Enemy((random.randint(50, WIDTH - 50),
                           -50),
                          player,
                          boss=False)
                all_sprites.add(e)
                enemies.add(e)
            boss = Enemy((WIDTH // 2, -100), player, boss=True)
            all_sprites.add(boss)
            enemies.add(boss)
            boss_spawned = True

        # проверка смерти игрока
        if player.health <= 0:
            return False

        # спавн ключа:
        # на Nal-Hutta — после босса, на остальных — после всех врагов
        if not key_spawned:
            if level_key == 'nal_hutta':
                if boss_spawned and not any(e.boss for e in enemies):
                    key = Key((WIDTH // 2, HEIGHT // 2))
                    all_sprites.add(key)
                    keys_group.add(key)
                    key_spawned = True
            else:
                if kills >= total_enemies:
                    key = Key((WIDTH // 2, HEIGHT // 2))
                    all_sprites.add(key)
                    keys_group.add(key)
                    key_spawned = True

        # подбор ключа
        if key_spawned and pygame.sprite.spritecollide(
                player, keys_group, True):
            progress['completed'].add(level_key)
            return True

        # отрисовка
        screen.blit(bg, (0, 0))
        all_sprites.draw(screen)

        # полосы здоровья
        for en in enemies:
            draw_enemy_hp(screen, en)
        draw_health_bar(screen,
                        player.health,
                        player.max_health)

        # цифровой индикатор HP
        hp_text = font.render(
            f"{player.health}/{player.max_health}",
            True, (255, 255, 255)
        )
        text_x = 10 + ((WIDTH - 220 - hp_text.get_width()) // 2)
        screen.blit(hp_text, (text_x, 10))

        # HUD: монеты, убийства, таймер
        elapsed = pygame.time.get_ticks() - start_time
        remaining = max(0, TIME_LIMIT - elapsed)
        mins, secs = divmod(remaining // 1000, 60)
        screen.blit(font.render(
            f"Монеты: {player.coins}",
            True, (255, 255, 255)
        ), (10, 40))
        screen.blit(font.render(
            f"Убито: {kills}",
            True, (255, 255, 255)
        ), (10, 70))
        screen.blit(font.render(
            f"Время: {mins:01d}:{secs:02d}",
            True, (255, 255, 255)
        ), (WIDTH - 200, 10))

        pygame.display.flip()

        # тайм-аут боя
        if remaining <= 0:
            return False


def main():
    """
    Точка входа: главное меню → выбор планеты → бой.
    При провале возвращаемся в меню.
    """
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Звёздные войны: Выживание")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    while True:
        # Главное меню
        if main_menu(screen) != 'play':
            pygame.quit()
            sys.exit()

        # сброс прогресса и создание игрока
        progress = {'ship_bought': False, 'completed': set()}
        player = Player((WIDTH // 2, HEIGHT - 100))
        player.coins = START_COINS

        # выбор планеты и запуск боя
        while True:
            key = select_planet(screen, progress)

            if key == 'coruscant':
                shop(screen, font, player, progress)
                continue

            if key == 'tatooine' and not progress['ship_bought']:
                shop(screen, font, player, progress)
                if not progress['ship_bought']:
                    continue

            success = run_battle(
                screen, key, player, progress, font, clock
            )
            if not success:
                # при провале выходим в меню
                break

        # цикл меню → выбор → бой продолжается
        continue


if __name__ == "__main__":
    main()
