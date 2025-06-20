import pygame


def load_alpha(path):
    """
    Загружает изображение и делает почти белые пиксели прозрачными.

    :param path: путь к файлу изображения
    :return: объект pygame.Surface с поддержкой альфа-канала
    """
    img = pygame.image.load(path).convert_alpha()
    width, height = img.get_size()
    # проходим по всем пикселям и делаем почти белые прозрачными
    for x in range(width):
        for y in range(height):
            r, g, b, a = img.get_at((x, y))
            if r > 240 and g > 240 and b > 240:
                img.set_at((x, y), (r, g, b, 0))
    return img
