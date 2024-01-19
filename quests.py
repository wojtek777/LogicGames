import random
from dataclasses import dataclass


@dataclass
class Quests:
    riddles = [
        ['77 > 7?', True],
        ['21 > 12?', True],
        ['123 > 321?', False],
        ['a + a + a = 15, then a = 5?', True],
        ['a > b > c, then c > a?', False],
        ['a > 5 then a > 3?', True],
        ['a = 1, b = 2, c = 3 then f = 7?', True],
        ['5 + 4 + 3 > 4 + 3 + 2 + 1?', True],
        ['7 + 8 + 9 > 9 + 10 + 5?', False],
        ['8 * 7 * 6 = 7 * 6 * 8?', True],
        ['2 + 2 = 2 * 2?', True],
        ['3 * 3 = 3 + 3?', False],
        ['3 * 3 > 3 + 3?', True],
        ['7 * 7 = 48?', False],
        ['7 * 7 > 48?', True],
        ['7 * 7 = 49?', True],
        ['6 * 4 = 5 * 5?', False],
        ['1 + 2 + 3 + 4 + 5 = 14?', False]
    ]
    last_riddle = len(riddles) - 1
    random.shuffle(riddles)
