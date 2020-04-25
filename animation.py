import pygame, os, sys, time
import preparation, fight_text


def battle_begin(screen, selfPoke, oppoPoke, selfPanel, oppoPanel, pureBG):
    clock = pygame.time.Clock()

    for i in range(101, -1, -1):
        selfPanel['lifePanel'].rect.topleft = (126 + i , 74)
        oppoPanel['grass'].rect.topleft = (119 + i, 44)
        selfPoke.hpBar.rect.topleft = (173 + i, 91)
        selfPoke.nameSur.rect.topleft = (142 + i, 79)
        selfPoke.levelSur.rect.bottomright = (221 + i, 87)
        selfPoke.hpSur.rect.bottomright = (221 + i, 104)
        oppoPoke.rect.bottomleft = (135 + i, 75)
        if selfPoke.sexSur:
            selfPoke.sexSur.rect.bottomleft = (selfPoke.nameSur.rect.right, selfPoke.nameSur.rect.bottom - 1)

        oppoPanel['lifePanel'].rect.topleft = (13 - i, 14)
        selfPanel['grass'].rect.bottomleft = (0 - i, 112)
        oppoPoke.hpBar.rect.topleft = (52 - i, 31)
        oppoPoke.nameSur.rect.topleft = (21 - i, 18)
        oppoPoke.levelSur.rect.bottomright = (99 - i, 26)
        oppoPoke.hpSur.rect.bottomright = (0 - i, 0)
        selfPoke.rect.bottomleft = (28 - i ,120)
        if oppoPoke.sexSur:
            oppoPoke.sexSur.rect.bottomleft = (oppoPoke.nameSur.rect.right, oppoPoke.nameSur.rect.bottom - 1)

        screen.blit(pureBG, pygame.Rect(0, 0, 240, 160))
        preparation.OrderedBlitLeft(screen, selfPanel, oppoPanel, selfPoke, oppoPoke)
        preparation.OrderedBlitRight(screen, selfPanel, oppoPanel, selfPoke, oppoPoke)
        pygame.display.update()
        clock.tick(130)


def attack_round(priority, maneuverUsed, attackResult, screen, selfPanel, oppoPanel, fightBG, selectionPanels, fontText, fontHP, selfPoke, oppoPoke):
    if priority == 1:
        attack_once(maneuverUsed['maneuverSelf'], attackResult['arOppo'], screen, oppoPanel, fightBG, selectionPanels, fontText, fontHP, oppoPoke, selfPoke)
        attack_once(maneuverUsed['maneuverOppo'], attackResult['arSelf'], screen, selfPanel, fightBG, selectionPanels, fontText, fontHP, selfPoke, oppoPoke)
    else:
        attack_once(maneuverUsed['maneuverOppo'], attackResult['arSelf'], screen, selfPanel, fightBG, selectionPanels, fontText, fontHP, selfPoke, oppoPoke)
        attack_once(maneuverUsed['maneuverSelf'], attackResult['arOppo'], screen, oppoPanel, fightBG, selectionPanels, fontText, fontHP, oppoPoke, selfPoke)

def attack_once(maneuver, attackResult, screen, defensePanel, fightBG, selectionPanels, fontText, fontHP, defensePoke, attackPoke):
    # 1. oppoPoke blinking
    print(screen.get_clip())
    screen.set_clip(defensePoke.rect)
    for i in range(6):
        circle_animation(screen, [fightBG, defensePoke], 20)

    # 2. description.
    screen.set_clip(screen.get_rect())
    print(screen.get_clip())
    if attackResult['critical']:
        rating = '击中了要害!'
    else:
        if attackResult['effective'] == 1:
            rating = '效果拔群!'
        elif attackResult['effective'] == -1:
            rating = '效果不好.'
        elif attackResult['effective'] == -2:
            rating = '没有效果.'
        else:
            rating = '效果一般.'
    screen.blit(selectionPanels['textbox'].image, pygame.Rect(0, 112, 1, 1))
    fight_text.print_text(screen, '{}使用了{}, {}'.format(attackPoke.info['name_C'], maneuver['name_C'], rating), fontText, 1)

    # 3. hp decrease
    screen.set_clip(defensePanel['lifePanel'].rect)
    print(screen.get_clip())
    hp_decrease_animation(attackResult, screen, fightBG, fontHP, defensePoke)

    screen.set_clip(screen.get_rect())
    print(screen.get_clip())

    hp = defensePoke.info['statsState']['hpChange']
    if hp == 0:
        screen.blit(selectionPanels['textbox'].image, pygame.Rect(0, 112, 1, 1))
        fight_text.print_text(screen, '{}倒下了.'.format(defensePoke.info['name_C']), fontText, 1)
        fight_text.print_text(screen, '{}获得了胜利.'.format(attackPoke.info['name_C']), fontText, 2)
        time.sleep(2)
        sys.exit()


def hp_decrease_animation(attackResult, screen, fightBG, fontHP, defensePoke, fieldDir=None):
    if fieldDir is None:
        cwd = os.getcwd()
        fieldDir = os.path.join(cwd, 'battle', 'field')

    real_damage = attackResult['realdamage']
    damage = attackResult['damage']
    hp = defensePoke.info['statsState']['hpChange']
    hpMax = defensePoke.info['stats']['hp']
    ratio = damage / hpMax
    originalHp = hp + real_damage
    fps = 60 if ratio >= 0.5 else 40

    hpBar = pygame.sprite.Sprite()
    hpBar.rect = defensePoke.hpBar.rect

    decreaseClock = pygame.time.Clock()

    while originalHp != hp:
        originalHp = max(originalHp - 1, 0)
        ratio = originalHp / hpMax
        if ratio >= 0.5:
            greenLife = preparation.InfoSurface(os.path.join(fieldDir, 'green.png'))
            hpBar.image = pygame.transform.scale(greenLife.image,
                                                 (int(greenLife.rect.width * ratio),
                                                  greenLife.rect.height))
        elif 0.2 <= ratio < 0.5:
            yellowLife = preparation.InfoSurface(os.path.join(fieldDir, 'yellow.png'))
            hpBar.image = pygame.transform.scale(yellowLife.image,
                                                 (int(yellowLife.rect.width * ratio),
                                                  yellowLife.rect.height))
        elif ratio < 0.2:
            redLife = preparation.InfoSurface(os.path.join(fieldDir, 'red.png'))
            hpBar.image = pygame.transform.scale(redLife.image,
                                                 (int(redLife.rect.width * ratio),
                                                  redLife.rect.height))

        screen.blit(fightBG.image, fightBG.rect)
        screen.blit(hpBar.image, hpBar.rect)

        if defensePoke.hpSur.rect.top >= 0 and defensePoke.hpSur.rect.left >= 0:
            hpRect = defensePoke.hpSur.rect
            fontHP.render_to(screen, hpRect, '{}/{}'.format(originalHp, hpMax))
        pygame.display.update()

        decreaseClock.tick(fps)


def circle_animation(screen, sprites, fps):
    durationClock = pygame.time.Clock()
    for sprite in sprites:
        screen.blit(sprite.image, sprite.rect)
        pygame.display.update()
        durationClock.tick(fps)


