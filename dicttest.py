import os, json

infoG = {
    'name': 'Gyarados',
    'name_C': '暴鲤龙',
    'type': ['Water', 'Fly'],
    'sex': '♂',
    'level': 50,
    'ability': 'Intimidate',
    'stats': {
        'hp': 155,
        'attack': 177,
        'defense': 84,
        'spa': 58,
        'spd': 105,
        'speed': 117,
    },
    'statsState': {
        'hpChange': 155,
        'speedChange': 0,
        'spaChange': 0,
        'spdChange': 0,
        'defenseChange': 0,
        'attackChange': 0
    },
    'maneuvers': [[3, 10], [5, 15], [6, 15], [7, 15]],
    'state': None,
    'item': None,
    'exp': None,
    'image': 'Gyarados.png'
}

infoM = {
    'name': 'Metagross',
    'name_C': '巨金怪',
    'type': ['Metal', 'Psychic'],
    'sex': None,
    'level': 50,
    'ability': 'Clear Body',
    'stats': {
        'hp': 140,
        'attack': 188,
        'defense': 166,
        'spa': 100,
        'spd': 95,
        'speed': 67,
    },
    'statsState': {
        'hpChange': 140,
        'speedChange': 0,
        'spaChange': 0,
        'spdChange': 0,
        'defenseChange': 0,
        'attackChange': 0
    },
    'maneuvers': [[1, 15], [2, 30], [3, 10], [4, 10]],
    'state': None,
    'item': None,
    'exp': None,
    'image': 'Metagross.png'
}

infoMa1 = {
    'No': 1,
    'name': 'Thunder Punch',
    'name_C': '雷电拳',
    'type': 'Electric',
    'type_C': '电',
    'category': 'physical',
    'ppMax': 15,
    'power': 75,
    'accuracy': 100,
    'priority': 0
}

infoMa2 = {
    'No': 2,
    'name': 'Bullet Punch',
    'name_C': '子弹拳',
    'type': 'Metal',
    'type_C': '钢',
    'category': 'physical',
    'ppMax': 30,
    'power': 40,
    'accuracy': 100,
    'priority': 1
}

infoMa3 = {
    'No': 3,
    'name': 'Earthquake',
    'name_C': '地震',
    'type': 'Ground',
    'type_C': '地',
    'category': 'physical',
    'ppMax': 10,
    'power': 100,
    'accuracy': 100,
    'priority': 0
}

infoMa4 = {
    'No': 4,
    'name': 'Meteor Punch',
    'name_C': '彗星拳',
    'type': 'Metal',
    'type_C': '钢',
    'category': 'physical',
    'ppMax': 10,
    'power': 90,
    'accuracy': 90,
    'priority': 0
}

infoMa5 = {
    'No': 5,
    'name': 'Crunch',
    'name_C': '咬碎',
    'type': 'Dark',
    'type_C': '恶',
    'category': 'physical',
    'ppMax': 15,
    'power': 80,
    'accuracy': 100,
    'priority': 0
}

infoMa6 = {
    'No': 6,
    'name': 'Ice Fang',
    'name_C': '冰之牙',
    'type': 'Ice',
    'type_C': '冰',
    'category': 'physical',
    'ppMax': 15,
    'power': 65,
    'accuracy': 95,
    'priority': 0
}

infoMa7 = {
    'No': 7,
    'name': 'Waterfall',
    'name_C': '攀瀑',
    'type': 'Water',
    'type_C': '水',
    'category': 'physical',
    'ppMax': 15,
    'power': 80,
    'accuracy': 100,
    'priority': 0
}

typeAttackBonus = {
    'Electric': {
        'Normal': 1,
        'Fight': 1,
        'Fly': 2,
        'Poison': 1,
        'Ground': 0,
        'Rock': 1,
        'Bug': 1,
        'Ghost': 1,
        'Metal': 1,
        'Fire': 1,
        'Water': 2,
        'Grass': 0.5,
        'Electric': 0.5,
        'Psychic': 0.5,
        'Ice': 1,
        'Dragon': 0.5,
        'Fairy': 1
    },
    'Fly': {
        'Normal': 1,
        'Fight': 2,
        'Fly': 1,
        'Poison': 1,
        'Ground': 1,
        'Rock': 0.5,
        'Bug': 2,
        'Ghost': 1,
        'Metal': 0.5,
        'Fire': 1,
        'Water': 1,
        'Grass': 2,
        'Electric': 0.5,
        'Psychic': 1,
        'Ice': 1,
        'Dragon': 1,
        'Drak': 1,
        'Fairy': 1
    },
    'Normal': {
        'Normal': 1,
        'Fight': 1,
        'Fly': 1,
        'Poison': 1,
        'Ground': 1,
        'Rock': 0.5,
        'Bug': 2,
        'Ghost': 0,
        'Metal': 0.5,
        'Fire': 1,
        'Water': 1,
        'Grass': 2,
        'Electric': 1,
        'Psychic': 1,
        'Ice': 1,
        'Dragon': 1,
        'Drak': 1,
        'Fairy': 1
    },
    'Fight': {
        'Normal': 2,
        'Fight': 1,
        'Fly': 0.5,
        'Poison': 0.5,
        'Ground': 1,
        'Rock': 2,
        'Bug': 0.5,
        'Ghost': 0,
        'Metal': 2,
        'Fire': 1,
        'Water': 1,
        'Grass': 2,
        'Electric': 1,
        'Psychic': 0.5,
        'Ice': 2,
        'Dragon': 1,
        'Drak': 2,
        'Fairy': 0.5
    },
    'Poison': {
        'Normal': 1,
        'Fight': 1,
        'Fly': 1,
        'Poison': 0.5,
        'Ground': 0.5,
        'Rock': 0.5,
        'Bug': 2,
        'Ghost': 0.5,
        'Metal': 0,
        'Fire': 1,
        'Water': 1,
        'Grass': 2,
        'Electric': 1,
        'Psychic': 1,
        'Ice': 1,
        'Dragon': 1,
        'Dark': 1,
        'Fairy': 2
    },
    'Ground': {
        'Normal': 1,
        'Fight': 1,
        'Fly': 0,
        'Poison': 2,
        'Ground': 1,
        'Rock': 2,
        'Bug': 0.5,
        'Ghost': 1,
        'Metal': 2,
        'Fire': 2,
        'Water': 1,
        'Grass': 0.5,
        'Electric': 2,
        'Psychic': 1,
        'Ice': 1,
        'Dragon': 1,
        'Dark': 1,
        'Fairy': 1
    },
    'Rock': {
        'Normal': 1,
        'Fight': 0.5,
        'Fly': 2,
        'Poison': 1,
        'Ground': 0.5,
        'Rock': 1,
        'Bug': 2,
        'Ghost': 1,
        'Metal': 0.5,
        'Fire': 2,
        'Water': 1,
        'Grass': 2,
        'Electric': 1,
        'Psychic': 1,
        'Ice': 2,
        'Dragon': 1,
        "Dark": 1,
        'Fairy': 1
    },
    'Bug': {
        'Normal': 1,
        'Fight': 0.5,
        'Fly': 0.5,
        'Poison': 0.5,
        'Ground': 1,
        'Rock': 1,
        'Bug': 2,
        'Ghost': 0.5,
        'Metal': 0.5,
        'Fire': 0.5,
        'Water': 1,
        'Grass': 2,
        'Electric': 1,
        'Psychic': 2,
        'Ice': 1,
        'Dragon': 1,
        "Drak": 2,
        'Fairy': 0.5
    },
    'Ghost': {
        'Normal': 0,
        'Fight': 1,
        'Fly': 1,
        'Poison': 1,
        'Ground': 1,
        'Rock': 1,
        'Bug': 1,
        'Ghost': 2,
        'Metal': 1,
        'Fire': 1,
        'Water': 1,
        'Grass': 2,
        'Electric': 1,
        'Psychic': 2,
        'Ice': 1,
        'Dragon': 1,
        'Dark': 0.5,
        'Fairy': 1
    },
    'Metal': {
        'Normal': 1,
        'Fight': 1,
        'Fly': 1,
        'Poison': 1,
        'Ground': 1,
        'Rock': 2,
        'Bug': 1,
        'Ghost': 1,
        'Metal': 0.5,
        'Fire': 0.5,
        'Water': 0.5,
        'Grass': 1,
        'Electric': 0.5,
        'Psychic': 1,
        'Ice': 2,
        'Dragon': 1,
        'Dark': 1,
        'Fairy': 2
    },
    'Fire': {
        'Normal': 1,
        'Fight': 1,
        'Fly': 1,
        'Poison': 1,
        'Ground': 1,
        'Rock': 0.5,
        'Bug': 2,
        'Ghost': 1,
        'Metal': 2,
        'Fire': 0.5,
        'Water': 0.5,
        'Grass': 2,
        'Electric': 1,
        'Psychic': 1,
        'Ice': 2,
        'Dragon': 0.5,
        'Dark': 1,
        'Fairy': 1
    },
    'Water': {
        'Normal': 1,
        'Fight': 1,
        'Fly': 1,
        'Poison': 1,
        'Ground': 2,
        'Rock': 2,
        'Bug': 1,
        'Ghost': 1,
        'Metal': 1,
        'Fire': 2,
        'Water': 0.5,
        'Grass': 0.5,
        'Electric': 1,
        'Psychic': 1,
        'Ice': 1,
        'Dragon': 0.5,
        'Dark': 1,
        'Fairy': 1
    },
    'Grass': {
        'Normal': 1,
        'Fight': 1,
        'Fly': 0.5,
        'Poison': 0.5,
        'Ground': 2,
        'Rock': 2,
        'Bug': 0.5,
        'Ghost': 1,
        'Metal': 0.5,
        'Fire': 0.5,
        'Water': 2,
        'Grass': 0.5,
        'Electric': 1,
        'Psychic': 1,
        'Ice': 1,
        'Dragon': 0.5,
        'Dark': 1,
        'Fairy': 1
    },
    'Psychic': {
        'Normal': 1,
        'Fight': 2,
        'Fly': 1,
        'Poison': 2,
        'Ground': 1,
        'Rock': 1,
        'Bug': 1,
        'Ghost': 1,
        'Metal': 0.5,
        'Fire': 1,
        'Water': 1,
        'Grass': 1,
        'Electric': 1,
        'Psychic': 0.5,
        'Ice': 1,
        'Dragon': 1,
        'Dark': 0,
        'Fairy': 1
    },
    'Ice': {
        'Normal': 1,
        'Fight': 1,
        'Fly': 2,
        'Poison': 1,
        'Ground': 2,
        'Rock': 1,
        'Bug': 1,
        'Ghost': 1,
        'Metal': 0.5,
        'Fire': 0.5,
        'Water': 0.5,
        'Grass': 2,
        'Electric': 1,
        'Psychic': 1,
        'Ice': 0.5,
        'Dragon': 2,
        'Dark': 1,
        'Fairy': 1
    },
    'Dragon': {
        'Normal': 1,
        'Fight': 1,
        'Fly': 1,
        'Poison': 1,
        'Ground': 1,
        'Rock': 1,
        'Bug': 1,
        'Ghost': 1,
        'Metal': 0.5,
        'Fire': 1,
        'Water': 1,
        'Grass': 1,
        'Electric': 1,
        'Psychic': 1,
        'Ice': 1,
        'Dragon': 2,
        'Dark': 1,
        'Fairy': 0
    },
    'Dark': {
        'Normal': 1,
        'Fight': 0.5,
        'Fly': 1,
        'Poison': 1,
        'Ground': 1,
        'Rock': 1,
        'Bug': 1,
        'Ghost': 2,
        'Metal': 1,
        'Fire': 1,
        'Water': 1,
        'Grass': 1,
        'Electric': 1,
        'Psychic': 2,
        'Ice': 1,
        'Dragon': 1,
        'Dark': 0.5,
        'Fairy': 0.5
    },
    'Fairy': {
        'Normal': 1,
        'Fight': 2,
        'Fly': 1,
        'Poison': 0.5,
        'Ground': 1,
        'Rock': 1,
        'Bug': 1,
        'Ghost': 1,
        'Metal': 0.5,
        'Fire': 0.5,
        'Water': 1,
        'Grass': 1,
        'Electric': 1,
        'Psychic': 1,
        'Ice': 1,
        'Dragon': 2,
        'Dark': 2,
        'Fairy': 1
    }
}


with open(os.path.join(os.getcwd(), 'pokemonData', 'Gyarados.txt'), 'w') as file_object:
    js = json.dumps(infoG)
    file_object.write(js)

with open(os.path.join(os.getcwd(), 'pokemonData', 'Metagross.txt'), 'w') as file_object:
    js = json.dumps(infoM)
    file_object.write(js)

with open(os.path.join(os.getcwd(), 'maneuverData', 'Maneuver_1.txt'), 'w') as file_object:
    js = json.dumps(infoMa1)
    file_object.write(js)

with open(os.path.join(os.getcwd(), 'maneuverData', 'Maneuver_2.txt'), 'w') as file_object:
    js = json.dumps(infoMa2)
    file_object.write(js)

with open(os.path.join(os.getcwd(), 'maneuverData', 'Maneuver_3.txt'), 'w') as file_object:
    js = json.dumps(infoMa3)
    file_object.write(js)

with open(os.path.join(os.getcwd(), 'maneuverData', 'Maneuver_4.txt'), 'w') as file_object:
    js = json.dumps(infoMa4)
    file_object.write(js)

with open(os.path.join(os.getcwd(), 'maneuverData', 'Maneuver_5.txt'), 'w') as file_object:
    js = json.dumps(infoMa5)
    file_object.write(js)

with open(os.path.join(os.getcwd(), 'maneuverData', 'Maneuver_6.txt'), 'w') as file_object:
    js = json.dumps(infoMa6)
    file_object.write(js)

with open(os.path.join(os.getcwd(), 'maneuverData', 'Maneuver_7.txt'), 'w') as file_object:
    js = json.dumps(infoMa7)
    file_object.write(js)

with open(os.path.join(os.getcwd(), 'maneuverData', 'typeAttackBonus.txt'), 'w') as file_object:
    js = json.dumps(typeAttackBonus)
    file_object.write(js)


