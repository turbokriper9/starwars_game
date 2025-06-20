import random
import pygame
from settings import ASTEROID_IMG, WIDTH, HEIGHT, ASTEROID_DAMAGE
from utils import load_alpha


class Asteroid(pygame.sprite.Sprite):
    """
    Класс астероида. Спускается сверху вниз с
    случайной скоростью и исчезает за пределами экрана.
    """

    def __init__(self):
        super().__init__()
        # загрузка и масштабирование спрайта
        img = load_alpha(ASTEROID_IMG)
        self.image = pygame.transform.scale(img, (48, 48))

        # стартовые координаты (сверху экрана)
        x = random.randint(0, WIDTH)
        y = -self.image.get_height()
        self.rect = self.image.get_rect(center=(x, y))

        # случайная скорость падения
        self.speed = random.uniform(1.0, 3.0)

    def update(self, *args):
        """
        Обновляет позицию астероида;
        если он ушёл за нижнюю границу, удаляется.
        """
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()
