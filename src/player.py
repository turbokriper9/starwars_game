import pygame
from utils import load_alpha
from settings import (
    XWING_IMG,
    LASER_SOUND,
    PLAYER_SPEED,
    SPRINT_MULTIPLIER,
    MAX_HEALTH,
    MAX_SUPER,
    SHIELD_HP,
    WIDTH,
    HEIGHT,
    MAX_AMMO,
)


class Player(pygame.sprite.Sprite):
    """
    Класс игрока. Отвечает за перемещение, стрельбу и управление здоровьем.
    """

    def __init__(self, pos):
        super().__init__()
        # загрузка и масштабирование изображения с прозрачностью
        img = load_alpha(XWING_IMG)
        img.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(img, (64, 64))
        self.rect = self.image.get_rect(center=pos)

        # параметры игрока
        self.speed = PLAYER_SPEED
        self.health = MAX_HEALTH
        self.max_health = MAX_HEALTH

        self.ammo = MAX_AMMO
        self.max_ammo = MAX_AMMO

        self.super_charge = 0
        self.max_super = MAX_SUPER

        self.start_pos = pos
        self.coins = 0

        self.shield_level = 0
        self.shield_hp = 0

        # звук выстрела
        self.laser_sfx = pygame.mixer.Sound(LASER_SOUND)

    def set_shield(self, lvl):
        """
        Устанавливает уровень щита и добавляет соответствующее здоровье.
        """
        self.shield_level = lvl
        self.shield_hp = SHIELD_HP.get(lvl, 0)

    def handle_input(self, keys):
        """
        Обрабатывает ввод (WASD и стрелки) и перемещает игрока.
        """
        vel = pygame.Vector2(0, 0)
        mult = (
            SPRINT_MULTIPLIER
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
            else 1
        )
        v = self.speed * mult

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            vel.y -= v
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            vel.y += v
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            vel.x -= v
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            vel.x += v

        self.rect.move_ip(vel)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def shoot(self, direction):
        """
        Стреляет в заданном направлении, если есть патроны.
        Возвращает объект Bullet или None.
        """
        if self.ammo > 0:
            self.laser_sfx.play()
            self.ammo -= 1
            from bullet import Bullet

            return Bullet(self.rect.center, direction)

        return None

    def reload(self):
        """
        Перезаряжает оружие до максимального запаса патронов.
        """
        self.ammo = self.max_ammo

    def take_damage(self, amt):
        """
        Получает урон: сначала учитывается щит, затем здоровье.
        """
        if self.shield_hp > 0:
            self.shield_hp -= amt
            overflow = -self.shield_hp
            if overflow > 0:
                self.health -= overflow
                self.shield_hp = 0
        else:
            self.health -= amt

        if self.health <= 0:
            self.health = 0

    def charge_super(self, amt):
        """
        Накаливает супер-атаку.
        """
        self.super_charge = min(self.super_charge + amt, self.max_super)

    def do_super(self, enemies):
        """
        Выполняет супер-атаку по всем врагам в группе.
        """
        if self.super_charge >= self.max_super:
            for e in enemies:
                e.take_damage(50)
            self.super_charge = 0

    def heal(self, amount):
        """
        Восстанавливает здоровье на указанную величину.
        """
        self.health += amount

    def update(self, *args):
        """
        Пустой update для соответствия интерфейсу pygame.sprite.Sprite.
        """
        pass
