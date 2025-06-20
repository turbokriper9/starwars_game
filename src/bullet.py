import pygame
from settings import BULLET_SPEED


class Bullet(pygame.sprite.Sprite):
    """
    Класс пули. Движется в заданном направлении и удаляется,
    когда выходит за границы экрана.
    """

    def __init__(self, pos, direction, color=(0, 255, 0), length=10):
        super().__init__()
        # создаём прозрачную поверхность и рисуем прямоугольник
        self.image = pygame.Surface((4, length), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, 4, length))
        self.rect = self.image.get_rect(center=pos)

        # устанавливаем вектор скорости пули
        self.velocity = direction * BULLET_SPEED

    def update(self, *args):
        """
        Обновляет позицию пули и удаляет её,
        если она вышла за границы экрана.
        """
        # перемещаем пулю
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # проверяем, не вышла ли пуля за экран
        surface = pygame.display.get_surface()
        screen_width = surface.get_width()
        screen_height = surface.get_height()

        if (
            self.rect.bottom < 0 or
            self.rect.top > screen_height or
            self.rect.right < 0 or
            self.rect.left > screen_width
        ):
            self.kill()
