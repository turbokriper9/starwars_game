import pygame, sys
from settings import (
    WIDTH, HEIGHT,
    COST_SHIP,
    MUSIC_CORUSCANT, FPS,
    COST_HEALTH
)

def shop(screen, font, player, progress):
    """
    Магазин: покупка корабля и лечение.
    """
    pygame.mixer.music.load(MUSIC_CORUSCANT)
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()

    items = []
    # 1) Купить корабль
    if not progress['ship_bought']:
        items.append({
            'label': 'Купить истребитель джедая',
            'cost': COST_SHIP,
            'action': lambda: progress.update({'ship_bought': True})
        })
    # 2) Лечение — несколько пакетов
    for hp_amt, cost in COST_HEALTH.items():
        items.append({
            'label': f"Здоровье +{hp_amt} ХП",
            'cost': cost,
            'action': lambda a=hp_amt: player.heal(a)
        })

    msg, msg_t = "", 0
    while True:
        dt = clock.tick(FPS)
        mx, my = pygame.mouse.get_pos()
        click = False
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                click = True

        screen.fill((10, 10, 40))
        # ← Назад
        back_rect = pygame.Rect(10, 10, 30, 30)
        pygame.draw.polygon(screen, (255,255,255), [(10,25),(40,10),(40,40)])
        if back_rect.collidepoint(mx, my) and click:
            return

        # Отрисовка списка товаров
        y0, h, w, x = 120, 50, WIDTH - 100, 50
        for i, it in enumerate(items):
            r = pygame.Rect(x, y0 + i*(h+15), w, h)
            col = (80,80,150) if r.collidepoint(mx, my) else (50,50,100)
            pygame.draw.rect(screen, col, r)
            text = font.render(f"{it['label']} — {it['cost']} coins", True, (255,255,255))
            screen.blit(text, (r.x+10, r.y + (h-text.get_height())//2))
            if click and r.collidepoint(mx, my):
                if player.coins >= it['cost']:
                    player.coins -= it['cost']
                    it['action']()
                else:
                    msg, msg_t = "Нехватает монет", FPS * 2

        # Баланс и сообщение об ошибке
        bal = font.render(f"Coins: {player.coins}", True, (255,255,255))
        screen.blit(bal, (x, y0 + len(items)*(h+15) + 20))
        if msg_t > 0:
            err = font.render(msg, True, (255,50,50))
            screen.blit(err, ((WIDTH - err.get_width())//2, HEIGHT - 100))
            msg_t -= 1

        pygame.display.flip()
