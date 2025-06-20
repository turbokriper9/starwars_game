# Ключи и названия планет + конфигурация врагов
LEVELS = [
    {
        'key': 'tatooine',
        'name': 'Татуин',
        'enemies': { 'tie': 1 },
        'boss_after': None,  # босс на 3-м уровне
    },
    {
        'key': 'hoth',
        'name': 'Хот',
        'enemies': { 'tie': 2 },
        'boss_after': None,
    },
    {
        'key': 'nal_hutta',
        'name': 'Нал-Хатта',
        'enemies': { 'tie': 3 },
        'boss_after': 3,     # после 3 убитых спавнится босс + 2
    },
]
