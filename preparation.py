import pygame, os, json


class BattlingPokemon(pygame.sprite.Sprite):
    def __init__(self, dataFile):
        pygame.sprite.Sprite.__init__(self)
        with open(dataFile, 'r') as file_object:
            js = file_object.read()
            dataDic = json.loads(js)
        self.rect = None
        self.image = None
        self.info = dataDic
        self.nameSur = None
        self.levelSur = None
        self.sexSur = None
        self.hpSur = None
        self.hpBar = None

    def update(self, screen):
        screen.blit(self.image, self.rect)


class TextSurface(pygame.sprite.Sprite):
    def __init__(self, content, font, fgColor=None, bgColor=None, Rotation=0, Size=0):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = font.render(content, fgcolor=fgColor, bgcolor=bgColor, rotation=Rotation, size=Size)

    def update(self, screen):
        screen.blit(self.image, self.rect)


class InfoSurface(pygame.sprite.Sprite):
    def __init__(self, file_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(file_path)
        self.rect = self.image.get_rect()

    def update(self, screen):
        screen.blit(self.image, self.rect)


def OrderedBlitLeft(screen, selfPanel, oppoPanel, selfPoke, oppoPoke):
    screen.blit(oppoPanel['lifePanel'].image, oppoPanel['lifePanel'].rect)
    screen.blit(oppoPoke.nameSur.image, oppoPoke.nameSur.rect)
    screen.blit(oppoPoke.levelSur.image, oppoPoke.levelSur.rect)
    screen.blit(oppoPoke.hpSur.image, oppoPoke.hpSur.rect)
    screen.blit(selfPanel['grass'].image, selfPanel['grass'].rect)
    screen.blit(oppoPoke.hpBar.image, oppoPoke.hpBar.rect)
    screen.blit(selfPoke.image, selfPoke.rect)
    if oppoPoke.sexSur:
        screen.blit(oppoPoke.sexSur.image, oppoPoke.sexSur.rect)


def OrderedBlitRight(screen, selfPanel, oppoPanel, selfPoke, oppoPoke):
    screen.blit(selfPanel['lifePanel'].image, selfPanel['lifePanel'].rect)
    screen.blit(selfPoke.nameSur.image, selfPoke.nameSur.rect)
    screen.blit(selfPoke.levelSur.image, selfPoke.levelSur.rect)
    screen.blit(selfPoke.hpSur.image, selfPoke.hpSur.rect)
    screen.blit(oppoPanel['grass'].image, oppoPanel['grass'].rect)
    screen.blit(selfPoke.hpBar.image, selfPoke.hpBar.rect)
    screen.blit(oppoPoke.image, oppoPoke.rect)
    if selfPoke.sexSur:
        screen.blit(selfPoke.sexSur.image, selfPoke.sexSur.rect)


def pokemonDataRead(txtFile, pokemonDataDir, pokemonPicDir, fontName, fontSex=None, fontLevel=None, fontHP=None):
    pokemon = BattlingPokemon(os.path.join(pokemonDataDir, txtFile))
    pokemon.image = pygame.image.load(os.path.join(pokemonPicDir, pokemon.info['image']))
    pokemon.rect = pokemon.image.get_rect()
    pokemon.nameSur = TextSurface(pokemon.info['name_C'], fontName)
    pokemon.sexSur = TextSurface(pokemon.info['sex'], fontName) if pokemon.info['sex'] else None
    pokemon.levelSur = TextSurface('Lv.' + str(pokemon.info['level']), fontName)
    pokemon.hpSur = TextSurface(str(pokemon.info['statsState']['hpChange']) + '/' + str(pokemon.info['stats']['hp']), fontHP)
    return pokemon


def panelHealthPicRead(fieldDir, side):
    grass = InfoSurface(os.path.join(fieldDir, 'grass_{}.png'.format(side)))
    lifePanel = InfoSurface(os.path.join(fieldDir, 'lifebar_{}.png'.format(side)))
    return dict(
        grass=grass,
        lifePanel=lifePanel
    )


def hp_bar_connect(pokemon, fieldDir=None):
    if fieldDir is None:
        cwd = os.getcwd()
        fieldDir = os.path.join(cwd, 'battle', 'field')

    hpBar = pygame.sprite.Sprite()
    hp = pokemon.info['statsState']['hpChange']
    hpMax = pokemon.info['stats']['hp']
    ratio = hp / hpMax

    if ratio >= 0.5:
        greenLife = InfoSurface(os.path.join(fieldDir, 'green.png'))
        hpBar.rect = greenLife.rect
        hpBar.image = pygame.transform.scale(greenLife.image, (int(greenLife.rect.width * ratio), greenLife.rect.height))
    elif 0.2 <= ratio < 0.5:
        yellowLife = InfoSurface(os.path.join(fieldDir, 'yellow.png'))
        hpBar.rect = yellowLife.rect
        hpBar.image = pygame.transform.scale(yellowLife.image, (int(yellowLife.rect.width * ratio), yellowLife.rect.height))
    elif ratio < 0.2:
        redLife = InfoSurface(os.path.join(fieldDir, 'red.png'))
        hpBar.rect = redLife.rect
        hpBar.image = pygame.transform.scale(redLife.image, (int(redLife.rect.width * ratio), redLife.rect.height))

    return hpBar


def panelSelectionPicRead(textboxDir):
    marker = InfoSurface(os.path.join(textboxDir, 'marker.png'))
    textbox = InfoSurface(os.path.join(textboxDir, 'textbox.png'))
    selection = InfoSurface(os.path.join(textboxDir, 'selection.png'))
    maneuver = InfoSurface(os.path.join(textboxDir, 'maneuver.png'))
    return dict(
        marker=marker,
        textbox=textbox,
        selection=selection,
        maneuver=maneuver
    )


def maneuvers_read(maneuverDataDir, selfPoke, oppoPoke):
    indexSelf = selfPoke.info['maneuvers']
    indexOppo = oppoPoke.info['maneuvers']

    maneuversSelf, maneuversOppo = [], []
    for index in indexSelf:
        with open(os.path.join(maneuverDataDir, 'Maneuver_{}.txt'.format(index[0]))) as file_object:
            js = file_object.read()
            dicData = json.loads(js)
            dicData['pp'] = index[1]
            maneuversSelf.append(dicData)

    for index in indexOppo:
        with open(os.path.join(maneuverDataDir, 'Maneuver_{}.txt'.format(index[0]))) as file_object:
            js = file_object.read()
            dicData = json.loads(js)
            dicData['pp'] = index[1]
            maneuversOppo.append(dicData)

    return maneuversSelf, maneuversOppo


def selection_panels_re_gen(screen, selectionPanels, maneuvers, fontText, filePath):
    selectionPanels['selection'].rect.bottomright = (240, 160)
    screen.blit(selectionPanels['selection'].image, selectionPanels['selection'].rect)

    fontText.render_to(selectionPanels['selection'].image, pygame.Rect(15, 11, 1, 1), '战斗')
    fontText.render_to(selectionPanels['selection'].image, pygame.Rect(15, 27, 1, 1), 'Pokemon')
    fontText.render_to(selectionPanels['selection'].image, pygame.Rect(70, 11, 1, 1), '背包')
    fontText.render_to(selectionPanels['selection'].image, pygame.Rect(70, 27, 1, 1), '逃跑')

    pygame.display.update()
    pygame.image.save(selectionPanels['selection'].image, os.path.join(filePath, 'major_selection.png'))

    selectionPanels['selection'] = InfoSurface(os.path.join(filePath, 'major_selection.png'))

    maneuverPanels = maneuver_panels_re_gen(screen, selectionPanels['maneuver'], maneuvers, fontText, filePath)
    selectionPanels['maneuverPanels'] = maneuverPanels

    return selectionPanels


def maneuver_panels_re_gen(screen, panel, maneuvers, fontText, filePath):
    panel.rect.topleft = (0, 112)
    screen.blit(panel.image, panel.rect)

    fontText.render_to(panel.image, pygame.Rect(18, 11, 1, 1), maneuvers[0]['name_C'])
    fontText.render_to(panel.image, pygame.Rect(82, 11, 1, 1), maneuvers[1]['name_C'])
    fontText.render_to(panel.image, pygame.Rect(18, 27, 1, 1), maneuvers[2]['name_C'])
    fontText.render_to(panel.image, pygame.Rect(82, 27, 1, 1), maneuvers[3]['name_C'])
    pygame.display.update()

    pygame.image.save(panel.image, os.path.join(filePath, 'temp_maneuver.png'))

    maneuverPanels = []
    for i in range(len(maneuvers)):
        temp_panel = InfoSurface(os.path.join(filePath, 'temp_maneuver.png'))
        screen.blit(temp_panel.image, pygame.Rect(0, 112, 1, 1))
        fontText.render_to(temp_panel.image, pygame.Rect(160, 12, 1, 1), 'PP')
        fontText.render_to(temp_panel.image, pygame.Rect(200, 12, 1, 1), '{}/{}'.format(maneuvers[i]['pp'], maneuvers[i]['ppMax']))
        fontText.render_to(temp_panel.image, pygame.Rect(160, 27, 1, 1), '属性/{}'.format(maneuvers[i]['type_C']))
        pygame.display.update()
        pygame.image.save(temp_panel.image, os.path.join(filePath, 'temp_maneuver_{}.png'.format(i + 1)))
        maneuverPanels.append(InfoSurface(os.path.join(filePath, 'temp_maneuver_{}.png'.format(i + 1))))

    return maneuverPanels


def bg_gen(screen, selfPoke, oppoPoke, selfPanel, oppoPanel, pureBG, fieldDir):
    selfPanel['lifePanel'].rect.topleft = (126, 74)
    oppoPanel['grass'].rect.topleft = (119, 44)
    selfPoke.hpBar.rect.topleft = (173, 91)
    selfPoke.nameSur.rect.topleft = (142, 79)
    selfPoke.levelSur.rect.bottomright = (221, 87)
    oppoPoke.rect.bottomleft = (135, 75)
    if selfPoke.sexSur:
        selfPoke.sexSur.rect.topleft = selfPoke.nameSur.rect.topright

    oppoPanel['lifePanel'].rect.topleft = (13, 14)
    selfPanel['grass'].rect.bottomleft = (0, 112)
    oppoPoke.hpBar.rect.topleft = (52, 31)
    oppoPoke.nameSur.rect.topleft = (21, 18)
    oppoPoke.levelSur.rect.bottomright = (99, 26)
    selfPoke.rect.bottomleft = (28, 120)
    if oppoPoke.sexSur:
        oppoPoke.sexSur.rect.bottomleft = (oppoPoke.nameSur.rect.right, oppoPoke.nameSur.rect.bottom - 1)

    screen.blit(pureBG, pygame.Rect(0, 0, 240, 160))
    pureBG.blit(oppoPanel['lifePanel'].image, oppoPanel['lifePanel'].rect)
    pureBG.blit(oppoPoke.nameSur.image, oppoPoke.nameSur.rect)
    pureBG.blit(oppoPoke.levelSur.image, oppoPoke.levelSur.rect)
    pureBG.blit(selfPanel['grass'].image, selfPanel['grass'].rect)
    if oppoPoke.sexSur:
        pureBG.blit(oppoPoke.sexSur.image, oppoPoke.sexSur.rect)

    pureBG.blit(selfPanel['lifePanel'].image, selfPanel['lifePanel'].rect)
    pureBG.blit(selfPoke.nameSur.image, selfPoke.nameSur.rect)
    pureBG.blit(selfPoke.levelSur.image, selfPoke.levelSur.rect)
    pureBG.blit(oppoPanel['grass'].image, oppoPanel['grass'].rect)
    if selfPoke.sexSur:
        pureBG.blit(selfPoke.sexSur.image, selfPoke.sexSur.rect)
    pygame.display.update()
    pygame.image.save(pureBG, os.path.join(fieldDir, 'temp_BG.png'))

    return InfoSurface(os.path.join(fieldDir, 'temp_BG.png'))
