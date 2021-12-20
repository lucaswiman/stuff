#!/usr/bin/env python

VEGETABLES = """\
carrots
potatoes
onions
tomatoes
eggplant
cilantro
mushrooms
cabbage
chilis
peppers
broccoli
squash
pumpkin
green beans
peas
corn
turnips
radishes
spinach
watercress
""".strip().split("\n")

assert len(VEGETABLES) == 20

from itertools import product
recipes = sorted({tuple(sorted(ingredients)) for ingredients in product(VEGETABLES, VEGETABLES, VEGETABLES)})
# print(f"Number of recipes {len(recipes)}")
# for recipe in recipes:
#     print(recipe)

import random
from io import StringIO

def random_recipe(recipes=recipes, say=True):
    recipe = ', '.join(random.choice(recipes))
    print(recipe)
    import subprocess
    subprocess.call(['say', recipe])


random_recipe()