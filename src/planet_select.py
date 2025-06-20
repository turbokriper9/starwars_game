import os
import sys
import pygame
from utils import load_alpha
from settings import WIDTH, HEIGHT, IMAGES_DIR, LOCK_IMG
from levels import LEVELS


def select_planet(screen, progress):
    """
    Экран выбора планеты. Показывает слоты с фоном планет,
    блокирует недоступные уровни и отображает замки.
    Возвращает ключ выбранной планеты.
    """
    # Настройка шрифта
    font = pygame.font.SysFont(None, 48)

    # Слоты: Coruscant + уровни
    slots = [('coruscant', 'Корусант')]
    slots += [(lvl['key'], lvl['name']) for lvl in LEVELS]
    count = len(slots)
    slot_width = WIDTH // count

    # Загрузка превью фонов
    previews = []
    for key, _ in slots:
        path = os.path.join(IMAGES_DIR, f'bg_{key}.png')
        img = pygame.image.load(path).convert()
        previews.append(pygame.transform.scale(img, (slot_width, HEIGHT)))

    # Геометрия слотов
    rects = [pygame.Rect(i * slot_width, 0, slot_width, HEIGHT)
             for i in range(count)]
    texts = []
    for _, name in slots:
        surf = font.render(name, True, (255, 255, 255))
        texts.append(surf)

    # Загрузка изображения замка
    lock_img = load_alpha(LOCK_IMG)
    lock_img = pygame.transform.scale(lock_img, (64, 64))

    while True:
        mx, my = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        # Отрисовка каждого слота
        for i, rect in enumerate(rects):
            key, _ = slots[i]
            screen.blit(previews[i], rect.topleft)

            # полупрозрачный затемняющий слой
            overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            screen.blit(overlay, rect.topleft)

            # определяем, заблокирована ли планета
            if key == 'coruscant':
                locked = False
            elif key == 'tatooine':
                locked = not progress['ship_bought']
            else:
                prev_key = slots[i - 1][0]
                locked = prev_key not in progress['completed']

            # рисуем замок, если заблокировано
            if locked:
                x = rect.x + (rect.width - lock_img.get_width()) // 2
                y = rect.y + (rect.height - lock_img.get_height()) // 2
                screen.blit(lock_img, (x, y))

            # рисуем название планеты
            text_surf = texts[i]
            tx = rect.x + (rect.width - text_surf.get_width()) // 2
            ty = HEIGHT - 80
            screen.blit(text_surf, (tx, ty))

        # обработка клика по слоту
        if click:
            idx = mx // slot_width
            key, _ = slots[idx]

            # всегда доступен Coruscant
            if key == 'coruscant':
                return key

            # проверка условий разблокировки
            if idx == 1 and not progress['ship_bought']:
                msg = font.render(
                    "Сначала купи корабль!",
                    True,
                    (255, 50, 50)
                )
            elif idx > 1 and slots[idx - 1][0] not in progress['completed']:
                msg = font.render(
                    "Нет ключа от планеты!",
                    True,
                    (255, 50, 50)
                )
            else:
                return key

            # показываем сообщение об ошибке
            screen.blit(
                msg,
                (
                    (WIDTH - msg.get_width()) // 2,
                    HEIGHT // 2,
                )
            )
            pygame.display.flip()
            pygame.time.delay(1000)

        pygame.display.flip()
