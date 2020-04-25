import pygame, sys, os
import json, time
import pygame.freetype
import preparation, fight_text, animation


# initiation
pygame.init()
cwd = os.getcwd()
fieldDir = os.path.join(cwd, 'battle', 'field')
pokemonPicDir = os.path.join(cwd, 'battle', 'pokemon')
pokemonDataDir = os.path.join(cwd, 'pokemonData')
maneuverDataDir = os.path.join(cwd, 'maneuverData')
textboxDir = os.path.join(cwd, 'battle', 'textboxes')
fontFile = os.path.join(cwd, 'fonts', 'NotoSansCJK-Medium.ttc')
fontName = pygame.freetype.Font(fontFile, 8)
fontHP = pygame.freetype.Font(fontFile, 8)
fontText = pygame.freetype.Font(fontFile, 10)

# stage building
screenSize = screenWidth, screenHeight = 240, 160
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption('D商汉化模拟器')
icon = pygame.image.load(os.path.join(cwd, 'icon.png'))
pygame.display.set_icon(icon)
pureBG = pygame.image.load(os.path.join(fieldDir, 'pure_bg.png'))
textbox = pygame.image.load(os.path.join(textboxDir, 'textbox.png'))
pygame.display.update()

# pokemon preparation
gyarados = preparation.pokemonDataRead('Gyarados.txt', pokemonDataDir, pokemonPicDir, fontName, fontHP=fontHP)
metagross = preparation.pokemonDataRead('Metagross.txt', pokemonDataDir, pokemonPicDir, fontName, fontHP=fontHP)
gyarados.hpBar = preparation.hp_bar_connect(gyarados, fieldDir)
metagross.hpBar = preparation.hp_bar_connect(metagross, fieldDir)
maneuvers = maneuversSelf, maneuversOppo = preparation.maneuvers_read(maneuverDataDir, selfPoke=metagross, oppoPoke=gyarados)
with open(os.path.join(maneuverDataDir, 'typeAttackBonus.txt'), 'r') as file_object:
    Data = file_object.read()
    typeAttackBonus = json.loads(Data)

# life panel preparation
selfPanel = preparation.panelHealthPicRead(fieldDir, 'self')
oppoPanel = preparation.panelHealthPicRead(fieldDir, 'oppo')

# background generation.
fightBG = preparation.bg_gen(screen, metagross, gyarados, selfPanel, oppoPanel, pureBG, fieldDir)
pureBG = pygame.image.load(os.path.join(fieldDir, 'pure_bg.png'))

# selection panel preparation
selectionPanels = preparation.panelSelectionPicRead(textboxDir)

# panel regeneration.
selectionPanels = preparation.selection_panels_re_gen(screen, selectionPanels, maneuversSelf, fontText, textboxDir)

# beginning animation
screen.blit(textbox, pygame.Rect(0, 112, 240, 48))
screen.blit(pureBG, pygame.Rect(0, 0, 240, 160))
animation.battle_begin(screen, metagross, gyarados, selfPanel, oppoPanel, pureBG)
fight_text.print_text(screen, '野生的暴鲤龙跳出来了!', fontText, 1)
fight_text.print_text(screen, '上吧, 巨金怪!', fontText, 2)

# major selection & fighting loop.
escape_times = 0
while True:
    markerState = fight_text.major_selection(screen, textbox, selectionPanels, metagross.info['name_C'], fontText)
    if markerState[1] == 1:
        markerState = fight_text.maneuver_selection(screen, selectionPanels)
        # whether to loop back to main selection, confirming maneuver or go back
        if markerState[2] == 1:
            screen.blit(textbox, pygame.Rect(0, 112, 240, 48))
            priority, maneuverUsed, attackResult = fight_text.fight(maneuvers, markerState, typeAttackBonus, selfPoke=metagross, oppoPoke=gyarados)
            animation.attack_round(priority, maneuverUsed, attackResult, screen, selfPanel, oppoPanel, fightBG, selectionPanels, fontText, fontHP, selfPoke=metagross, oppoPoke=gyarados)
        if markerState[2] == 0:
            continue
    elif markerState[1] == 2:
        fight_text.bag_selection(screen, selectionPanels, fontText)
        continue
    elif markerState[1] == 3:
        fight_text.pokemon_selection(screen, selectionPanels, fontText)
        continue
    elif markerState[1] == 4:
        success = fight_text.escape(screen, selectionPanels, fontText, escape_times, selfPoke=metagross, oppoPoke=gyarados)
        if success:
            sys.exit()
        else:
            continue
