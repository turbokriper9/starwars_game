import pygame
from utils import load_alpha
from settings import KEY_IMG


class Key(pygame.sprite.Sprite):
    """Класс ключа, который появляется после победы на уровне."""
    def __init__(self, pos):
        """Инициализация ключа по заданным координатам."""
        super().__init__()
        img = load_alpha(KEY_IMG)
        self.image = pygame.transform.scale(img, (32, 32))
        self.rect = self.image.get_rect(center=pos)