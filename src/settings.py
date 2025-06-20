import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')

# Размеры экрана и FPS
WIDTH = 1280
HEIGHT = 720
FPS = 60

# Игрок
PLAYER_SPEED = 4
SPRINT_MULTIPLIER = 1.5
MAX_HEALTH = 100
MAX_SUPER = 100
START_COINS = 100

# Магазин
COST_SHIP = 100
SHIELD_HP = {1: 25, 2: 50, 3: 100}
COST_SHIELD = {1: 20, 2: 40, 3: 60}
COST_TORPEDO = 100

# Лечение
COST_HEALTH = {
    25: 30,
    50: 55,
    100: 100,
}

# Пули
BULLET_SPEED = 12
MAX_AMMO = 15

# Урон от астероидов
ASTEROID_DAMAGE = MAX_HEALTH // 5

# Враги
ENEMY_SPEED = 2
ENEMY_HP = 60
BOSS_HP = 180

# Пути к изображениям
XWING_IMG = os.path.join(IMAGES_DIR, 'xwing.png')
TIE_IMG = os.path.join(IMAGES_DIR, 'tie.png')
TIE_ADVANCED_IMG = os.path.join(
    IMAGES_DIR,
    'tie_advanced.png'
)
ASTEROID_IMG = os.path.join(IMAGES_DIR, 'asteroid.png')
LOCK_IMG = os.path.join(IMAGES_DIR, 'lock.png')
KEY_IMG = os.path.join(IMAGES_DIR, 'key.png')

# Звуки
LASER_SOUND = os.path.join(
    SOUNDS_DIR,
    'laser_shot.ogg'
)
EXPLOSION_SOUND = os.path.join(
    SOUNDS_DIR,
    'explosion.wav'
)
TIE_SOUND = os.path.join(
    SOUNDS_DIR,
    'tie_fighter_sound.mp3'
)
MUSIC_CORUSCANT = os.path.join(
    SOUNDS_DIR,
    'music_coruscant.mp3'
)
MUSIC_TATOOINE = os.path.join(
    SOUNDS_DIR,
    'music_tatooine.mp3'
)
