import pygame
from utils import load_alpha
from settings import (
    ENEMY_SPEED,
    ENEMY_HP,
    BOSS_HP,
    BULLET_SPEED,
    FPS,
    TIE_IMG,
    TIE_ADVANCED_IMG,
    WIDTH,
    HEIGHT,
    TIE_SOUND,
)
from bullet import Bullet


class Enemy(pygame.sprite.Sprite):
    """
    Класс врага (TIE-истребитель). Может быть обычным или боссом.
    Обрабатывает движение к игроку и стрельбу по таймеру.
    """

    def __init__(self, pos, target, boss=False):
        super().__init__()
        self.boss = boss

        # Загрузка и настройка спрайта
        sprite_path = (
            TIE_ADVANCED_IMG if boss else TIE_IMG
        )
        img = load_alpha(sprite_path)
        img.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(img, (64, 64))
        self.rect = self.image.get_rect(center=pos)

        # Параметры врага
        self.speed = ENEMY_SPEED * (1.5 if boss else 1.0)
        self.target = target
        self.health = BOSS_HP if boss else ENEMY_HP
        self.max_health = self.health

        # Параметры стрельбы
        self.shoot_interval = 1.0  # секунды между выстрелами
        self.shoot_cooldown = 0.0
        self.sfx = pygame.mixer.Sound(TIE_SOUND)

    def take_damage(self, amount):
        """
        Наносит урон врагу, убивает, если здоровье <= 0.
        """
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def update(self):
        """
        Обновляет позицию и таймер выстрела.
        Возвращает Bullet при выходе стрельбы, иначе None.
        """
        # Движение к игроку
        vec = (
            pygame.Vector2(self.target.rect.center)
            - pygame.Vector2(self.rect.center)
        )
        if vec.length() > 0:
            vec.normalize_ip()
            self.rect.move_ip(vec * self.speed)
        self.rect.clamp_ip(
            pygame.Rect(0, 0, WIDTH, HEIGHT)
        )

        # Стрельба по интервалу
        self.shoot_cooldown -= 1 / FPS
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = self.shoot_interval
            return self.shoot()
        return None

    def shoot(self):
        """
        Создаёт пулю в направлении игрока.
        Цвет и длина пули жёстко заданы.
        """
        self.sfx.play()
        direction = (
            pygame.Vector2(self.target.rect.center)
            - pygame.Vector2(self.rect.center)
        )
        if direction.length() == 0:
            return None
        direction.normalize_ip()

        bullet = Bullet(
            pos=self.rect.center,
            direction=direction,
            color=(255, 50, 50),
            length=14,
        )
        bullet.velocity = direction * BULLET_SPEED
        return bullet
