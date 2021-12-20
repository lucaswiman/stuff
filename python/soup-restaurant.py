#!/usr/bin/env python

import blessings
t = blessings.Terminal()

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

import subprocess
def say(string):
    subprocess.run(["say", string])

def input_say(string):
    say(string)
    return input(t.bright_red_on_white(string))

def say_print(string):
    say(string)
    print(t.bright_red_on_white(string))


def get_payment(soup_name):
    import decimal
    from decimal import Decimal
    random.seed(soup_name)
    if random.random() < 0.33:
        price = Decimal('100.00')
    else:
        price = (decimal.Decimal(random.randint(500, 1000)) / 100).quantize(Decimal('0.01'))
    amount_paid = input_say(f"That'll be ${price}. ").strip('$')
    change = (decimal.Decimal(amount_paid) - price).quantize(Decimal('0.01'))
    say_print(f"here's your change: ${change}")
    


import time
import random

if __name__ == "__main__":
    while True:
        soup = input_say("what soup would you like? ")
        get_payment(soup)
        say_print(f"I'm working on {soup}.")
        time.sleep(random.randint(10, 15))
        say(f"Here's your soup: ")
        print(f"Here's your soup: " + random.choice("🍜🥣🍲"))
        say_print("\nNext Customer!")
