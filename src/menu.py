import os
import sys
import pygame

from settings import WIDTH, HEIGHT, SOUNDS_DIR


def main_menu(screen):
    """
    Отображает главное меню с кнопкой «ИГРАТЬ» и проигрывает фоновую музыку.
    """
    # Загрузка и запуск музыки меню
    music_path = os.path.join(SOUNDS_DIR, 'menu_music.mp3')
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)

    # Настройка шрифтов
    font_title = pygame.font.SysFont(None, 72)
    font_btn = pygame.font.SysFont(None, 48)

    title_surf = font_title.render(
        "Звёздные войны: выживание", True, (255, 255, 0)
    )
    btn_surf = font_btn.render("ИГРАТЬ", True, (255, 255, 255))
    btn_rect = pygame.Rect(
        (WIDTH - 200) // 2,
        (HEIGHT - 80) // 2,
        200,
        80,
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Клик по кнопке
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and btn_rect.collidepoint(event.pos)
            ):
                return 'play'

        # Отрисовка меню
        screen.fill((0, 0, 0))
        # Заголовок
        screen.blit(
            title_surf,
            (
                (WIDTH - title_surf.get_width()) // 2,
                100,
            ),
        )
        # Кнопка
        pygame.draw.rect(screen, (0, 0, 100), btn_rect)
        screen.blit(
            btn_surf,
            (
                btn_rect.x +
                (200 - btn_surf.get_width()) // 2,
                btn_rect.y +
                (80 - btn_surf.get_height()) // 2,
            ),
        )
        pygame.display.flip()
