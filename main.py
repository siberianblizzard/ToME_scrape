'''
ver 0.2
This is a simple parser for winning characters for Tales of Maj'Eyal 1.7.4
To change the version of the game you need to look up the patch id on the character vault website
Range of the page was calculated manually, because vault website is bare-bones and shows only 25 characters per page and
doesn't show you total amount of characters or pages, will try to find a way to fix it to optimize the script.
No exploration mode and easy difficulty because of my personal bias :)
TO-DO
optimize the counter algorithm
find a way to calculate amount of pages (check a page for next button if no button stop)
'''

import requests
import re
import pandas as pd
from time import sleep
from random import randint
from bs4 import BeautifulSoup


def get_winners(mode='roguelike', diff='normal'):
    winners_list = []
    tag_mode = {'adventure': '65',
                'roguelike': '66'}
    tag_diff = {'normal': '6',
                'nightmare': '26',
                'insane': '36',
                'madness': '227'}
    for i in range(0, 24):
        URL = 'https://te4.org/characters-vault?tag_name=&tag_level_min=&tag_level_max=&tag_winner=winner&tag_permadeath%5B%5D={0}&tag_difficulty%5B%5D={1}&tag_campaign%5B%5D=2&tag_game%5B%5D=699172&page={2}'.format(
            tag_mode[mode], tag_diff[diff], i)
        print(URL)
        page = requests.get(URL)
        sleep(randint(1, 3))
        soup = BeautifulSoup(page.content, "html.parser")
        char_table = soup.find(id="characters")
        my_table = char_table.find_all(style="color:#00FF00")
        for tag in my_table:
            winners_list.append(tag.get_text())
    return winners_list


def get_deaths(mode='roguelike', diff='normal'):
    deaths_list = []
    tag_mode = {'adventure': '65',
                'roguelike': '66'}
    tag_diff = {'normal': '6',
                'nightmare': '26',
                'insane': '36',
                'madness': '227'}
    for i in range(0, 3):
        #lvl 15+ deaths, maybe add custom value when range of pages will be automated
        URL = 'https://te4.org/characters-vault?tag_name=&tag_level_min=15&tag_level_max=&tag_dead=dead&tag_permadeath%5B%5D={0}&tag_difficulty%5B%5D={1}&tag_campaign%5B%5D=2&tag_game%5B%5D=699172&page={2}'.format(
            tag_mode[mode], tag_diff[diff], i)
        print(URL)
        page = requests.get(URL)
        sleep(randint(1, 3))
        soup = BeautifulSoup(page.content, "html.parser")
        char_table = soup.find(id="characters")
        my_table = char_table.find_all(style="color:#FF0000")
        for tag in my_table:
            deaths_list.append(tag.get_text())
    return deaths_list


def count_classes(mode='roguelike', diff='normal', status='win'):
    if status == 'win':
        characters_list = get_winners(mode, diff)
    elif status == 'dead':
        characters_list = get_deaths(mode, diff)
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
        if character is not None:
            characters_class = re.search(r'\s\d+\s\w+\s(.*)', character)
            if characters_class is not None:  # for broken non-unicode char sheets
                for class_name in class_list:
                    if class_name in characters_class[1]:
                        class_stats[class_name] += 1
                        break
    df = pd.DataFrame.from_dict(class_stats, orient='index')
    df.to_excel('characters_{0}_{1}_{2}.xlsx'.format(mode, diff, status), header=True)
    return df