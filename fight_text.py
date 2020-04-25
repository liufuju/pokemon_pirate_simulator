import pygame, os, sys
import time, json, random


def print_text(screen, content, font, line):
    text_clock = pygame.time.Clock()
    # beginning = [15, 133 - 5] if line == 1 else [15, 148 - 5]
    beginning = [15, 133] if line == 1 else [15, 148]
    for i in range(len(content)):
        character, characterRect = font.render(content[i])
        width = characterRect.width
        characterRect.bottomleft = beginning
        # characterRect.center = beginning
        # characterRect.left = beginning[0]
        screen.blit(character, characterRect)
        beginning[0] = beginning[0] + width
        pygame.display.update()
        text_clock.tick(10)
    time.sleep(0.3)


def quadrat_movement(screen, selectionPanels, markerState):
    pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])

    while True:
        pairs = xPair1, xPair2, yPair1, yPair2 = [1, 2], [3, 4], [1, 3], [2, 4]
        result = []
        for pair in pairs:
            if markerState[1] in pair:
                pair.remove(markerState[1])
                result.append(pair[0])

        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d or event.key == pygame.K_a:
                markerState[1] = result[0]
                blit_marker(screen, selectionPanels, markerState)
            if event.key == pygame.K_s or event.key == pygame.K_w:
                markerState[1] = result[1]
                blit_marker(screen, selectionPanels, markerState)
            if event.key == pygame.K_j:
                markerState[2] = 1
                break
            if event.key == pygame.K_k:
                markerState[2] = 0
                break

    return markerState


def blit_marker(screen, selectionPanels, markerState):
    if markerState[0] == 0:
        selectionPanels['selection'].rect.bottomright = (240, 160)
        screen.blit(selectionPanels['selection'].image, selectionPanels['selection'].rect)
        markerTLPos = ((129, 124), (184, 124), (129, 140), (184, 140))
        # markerTLPos = ((8, 12), (63, 12), (8, 28), (63, 28))
    elif markerState[0] == 1:
        selectionPanels['maneuverPanels'][markerState[1] - 1].rect.topleft = (0, 112)
        screen.blit(selectionPanels['maneuverPanels'][markerState[1] - 1].image, selectionPanels['maneuverPanels'][markerState[1] - 1].rect)
        markerTLPos = ((11, 124), (75, 124), (11, 140), (75, 140))

    selectionPanels['marker'].rect.topleft = markerTLPos[markerState[1] - 1]
    screen.blit(selectionPanels['marker'].image, selectionPanels['marker'].rect)
    pygame.display.update()


def major_selection(screen, textbox, selectionPanels, pokemon, fontText):
    screen.blit(textbox, pygame.Rect(0, 112, 240, 48))
    markerState = [0, 1, 1]
    blit_marker(screen, selectionPanels, markerState)

    print_text(screen, '{}做什么?'.format(pokemon), fontText, 1)
    markerState = quadrat_movement(screen, selectionPanels, markerState)
    return markerState


def maneuver_selection(screen, selectionPanels):
    markerState = [1, 1, 1]
    blit_marker(screen, selectionPanels, markerState)
    pygame.display.update()
    markerState = quadrat_movement(screen, selectionPanels, markerState)
    return markerState


def bag_selection(screen, selectionPanels, font):
    markerState = [2, 1, 1]
    screen.blit(selectionPanels['textbox'].image, pygame.Rect(0, 112, 1, 1))
    print_text(screen, '不行, 代码没写好, 背包锁住了!', font, 1)


def pokemon_selection(screen, selectionPanels, font):
    markerState = [3, 1, 1]
    screen.blit(selectionPanels['textbox'].image, pygame.Rect(0, 112, 1, 1))
    print_text(screen, '不行, 代码没写好, Pokemon查看不了!', font, 1)


def escape(screen, selectionPanels, font, escape_times, selfPoke, oppoPoke):
    markerState = [4, 1, 1]
    escape_times += 1
    screen.blit(selectionPanels['textbox'].image, pygame.Rect(0, 112, 1, 1))
    selfSpeed = selfPoke.info['stats']['speed'] * (1 + selfPoke.info['statsState']['speedChange'] * 0.5) \
        if selfPoke.info['statsState']['speedChange'] >= 0 else selfPoke.info['stats']['speed']
    oppoSpeed = oppoPoke.info['stats']['speed'] * (1 + oppoPoke.info['statsState']['speedChange'] * 0.5) \
        if oppoPoke.info['statsState']['speedChange'] >= 0 else oppoPoke.info['stats']['speed']

    success_rate = escape_success(selfSpeed, oppoSpeed, escape_times)
    if success_rate > 255 or success_rate > random.randint(0, 255):
        print_text(screen, '成功逃走了!', font, 1)
        return 1
    else:
        print_text(screen, '不行, 没能逃走', font, 1)
        return 0


def escape_success(selfSpeed, oppoSpeed, escape_times):
    A = selfSpeed
    B = (oppoSpeed / 4) % 255
    C = escape_times
    return 32 * A / B + 30 * C


def fight(maneuvers, markerState, typeAttackBonus, selfPoke, oppoPoke):
    selfSpeed = selfPoke.info['stats']['speed'] * (1 + selfPoke.info['statsState']['speedChange'] * 0.5) \
        if selfPoke.info['statsState']['speedChange'] >= 0 else selfPoke.info['stats']['speed']
    oppoSpeed = oppoPoke.info['stats']['speed'] * (1 + oppoPoke.info['statsState']['speedChange'] * 0.5) \
        if oppoPoke.info['statsState']['speedChange'] >= 0 else oppoPoke.info['stats']['speed']

    markerStateOppo = oppoAI()

    if selfSpeed > oppoSpeed or maneuvers[0][markerState[1] - 1]['priority'] > maneuvers[1][markerStateOppo[1] - 1]['priority']:
        priority = 1
    elif selfSpeed < oppoSpeed:
        priority = 0
    else:
        i = random.random()
        if i <= 0.5:
            priority = 1
        else:
            priority = 0

    if priority:
        maneuverSelf, arOppo = single_attack(maneuvers[0], selfPoke, oppoPoke, markerState, typeAttackBonus)
        maneuverOppo, arSelf = single_attack(maneuvers[1], oppoPoke, selfPoke, markerStateOppo, typeAttackBonus)
    else:
        maneuverOppo, arSelf = single_attack(maneuvers[1], oppoPoke, selfPoke, markerStateOppo, typeAttackBonus)
        maneuverSelf, arOppo = single_attack(maneuvers[0], selfPoke, oppoPoke, markerState, typeAttackBonus)

    return priority, dict(maneuverSelf=maneuverSelf, maneuverOppo=maneuverOppo), dict(arSelf=arSelf, arOppo=arOppo)


def single_attack(maneuvers, selfPoke, oppoPoke, markerState, typeAttackBonus):
    maneuver = maneuvers[markerState[1] - 1]
    power = maneuver['power']
    type = maneuver['type']
    accuracy = maneuver['accuracy']

    if maneuver['category'] != 'status':
        typeBonus, effective = type_judgement(type, selfPoke.info['type'], oppoPoke.info['type'], typeAttackBonus)

        hp = oppoPoke.info['statsState']['hpChange']
        level = selfPoke.info['level']
        attack = selfPoke.info['stats']['attack'] if maneuver['category'] == 'physical' else selfPoke.info['stats']['spa']
        defense = oppoPoke.info['stats']['defense'] if maneuver['category'] == 'physical' else oppoPoke.info['stats']['spd']

        damage, critical = damage_calculation(level, attack, defense, power, typeBonus)

        oppoPoke.info['statsState']['hpChange'] = max(oppoPoke.info['statsState']['hpChange'] - damage, 0)
        real_damage = hp - oppoPoke.info['statsState']['hpChange']

    return maneuver, dict(damage=damage, effective=effective, critical=critical, realdamage=real_damage)


def type_judgement(maneuType, selfType, oppoType, typeAttackBonus):
    typeBonusSelf = 1
    for type in oppoType:
        typeBonusSelf *= typeAttackBonus[maneuType][type]
    if typeBonusSelf > 1:
        effective = 1
    elif 0 < typeBonusSelf < 1:
        effective = -1
    elif typeBonusSelf == 0:
        effective = -2
    else:
        effective = 0
    typeBonusSelf *= 1.5 if maneuType in selfType else 1
    return typeBonusSelf, effective


def damage_calculation(level, attack, defense, power, typeBonus):
    levelFac = (2 * level + 10) / 250
    adFac = attack / defense
    bonus = typeBonus * random.randint(85, 100) * 0.01
    ran = random.random()
    bonus *= 1.5 if ran < 1 / 16 else 1
    critical = 1 if ran < 1 / 16else 0
    damage = int((levelFac * adFac * power + 2) * bonus)
    return damage, critical


def oppoAI():
    return [2, random.choice([1, 2, 3, 4])]