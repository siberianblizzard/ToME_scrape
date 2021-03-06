'''
ver 0.3.2
This is a simple parser for winning characters for Tales of Maj'Eyal 1.7.4
To change the version of the game you need to look up the patch id on the character vault website
No exploration mode and easy difficulty because of my personal bias :)
TODO
Make a proper pandas data frame from parsing
'''

import requests
import re
import pandas as pd
from time import sleep
from random import randint
from bs4 import BeautifulSoup


def get_characters(mode: str = 'roguelike', diff: str = 'normal', min_lvl: int = 15, status: str = 'win'):
    characters_list = []
    tag_mode = {'adventure': '65',
                'roguelike': '66'}
    tag_diff = {'normal': '6',
                'nightmare': '26',
                'insane': '36',
                'madness': '227'}
    tag_status = {'win': 'tag_winner=winner',
                  'dead': 'tag_dead=dead'}
    # color tags to exclude wins from dead characters
    if status == 'win':
        status_code = 'color:#00FF00'
    elif status == 'dead':
        status_code = 'color:#FF0000'
    else:
        return
    next_page_exists = True
    page_num = 0
    while next_page_exists:
        page_url = 'https://te4.org/characters-vault?tag_name=&tag_level_min={0}&tag_level_max=&{1}&tag_permadeath%5B%5D={2}&tag_difficulty%5B%5D={3}&tag_campaign%5B%5D=2&tag_game%5B%5D=699172&page={4}'.format(
            min_lvl, tag_status[status], tag_mode[mode], tag_diff[diff], page_num)
        print(page_url)  # for debugging purposes
        page = requests.get(page_url)
        sleep(randint(1, 3))
        page_content = BeautifulSoup(page.content, 'html.parser')
        char_table = page_content.find(id='characters')
        next_page_link = page_content.find(title='Go to next page')
        if next_page_link is None:
            next_page_exists = False
        else:
            page_num += 1
        res_table = char_table.find_all(style=status_code)
        for tag in res_table:
            characters_list.append(tag.get_text())
    return characters_list


def count_classes(mode: str = 'roguelike', diff: str = 'normal', min_lvl: int = 15, status: str = 'win'):
    if status == 'win' or status == 'dead':
        characters_list = get_characters(mode, diff, min_lvl, status)
    else:
        return 'Wrong status'
    class_stats = {'Berserker': 0, 'Bulwark': 0, 'Archer': 0, 'Arcane Blade': 0, 'Brawler': 0, 'Rogue': 0,
                   'Shadowblade': 0,
                   'Marauder': 0, 'Skirmisher': 0, 'Alchemist': 0, 'Archmage': 0, 'Necromancer': 0,
                   'Summoner': 0, 'Wyrmic': 0, 'Oozemancer': 0, 'Stone Warden': 0, 'Sun Paladin': 0, 'Anorithil': 0,
                   'Reaver': 0, 'Corruptor': 0, 'Doombringer': 0, 'Demonologist': 0, 'Cursed': 0, 'Doomed': 0,
                   'Paradox Mage': 0, 'Temporal Warden': 0, 'Mindslayer': 0, 'Solipsist': 0, 'Possessor': 0,
                   'Wanderer': 0, 'Sawbutcher': 0, 'Gunslinger': 0, 'Psyshot': 0, 'Annihilator': 0, 'Writhing One': 0,
                   'Adventurer': 0, 'Cultist of Entropy': 0}
    class_list = ['Berserker', 'Bulwark', 'Archer', 'Arcane Blade', 'Brawler', 'Rogue',
                  'Shadowblade', 'Marauder', 'Skirmisher', 'Alchemist', 'Archmage', 'Necromancer',
                  'Summoner', 'Wyrmic', 'Oozemancer', 'Stone Warden', 'Sun Paladin', 'Anorithil',
                  'Reaver', 'Corruptor', 'Doombringer', 'Demonologist', 'Cursed', 'Doomed',
                  'Paradox Mage', 'Temporal Warden', 'Mindslayer', 'Solipsist', 'Possessor', 'Adventurer',
                  'Wanderer', 'Sawbutcher', 'Gunslinger', 'Psyshot', 'Annihilator', 'Writhing One',
                  'Cultist of Entropy']
    for character in characters_list:
        if character is not None:  # for broken non-unicode char sheets
            characters_class = re.search(r'\s\d+\s\w+\s(.*)', character)
            if characters_class is not None:  # for broken non-unicode char sheets
                for class_name in class_list:
                    if class_name in characters_class[1]:
                        class_stats[class_name] += 1
                        break
    data_sheet = pd.DataFrame.from_dict(class_stats, orient='index')
    data_sheet.to_excel('characters_{0}_{1}_{2}.xlsx'.format(mode, diff, status), header=True)
    return data_sheet


print(count_classes('adventure', 'insane', 15, 'win'))
