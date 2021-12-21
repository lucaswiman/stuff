#!/usr/bin/env python

import blessings
t = blessings.Terminal()
import subprocess
from decimal import Decimal

INVENTORY = {
    "Dog treats for big dogs": Decimal('2.00'),
    "Dog treats for small dogs": Decimal('1.00'),
    "Dog treats for medium dogs": Decimal('3.00'),
}


def say(string):
    subprocess.run(["say", string])

def input_say(string):
    say(string)
    return input(t.bright_red_on_white(string))

def say_print(string):
    say(string)
    print(t.bright_red_on_white(string))


def get_payment(price: Decimal):
    import decimal
    from decimal import Decimal
    amount_paid = input_say(f"That'll be ${price}. ").strip('$')
    change = (decimal.Decimal(amount_paid) - price).quantize(Decimal('0.01'))
    say_print(f"here's your change: ${change}")


def say_inventory():
    inventory_string = "Here's what we've got in stock:\n"
    for i, (item, price) in enumerate(INVENTORY.items(), 1):
        inventory_string += f'({i}) {item} ${price}\n'
    say_print(inventory_string)

def get_next_item() -> str:
    item_number = int(input_say("Which item number would you like? ")) - 1
    item = list(INVENTORY.keys())[item_number]
    return item


def needs_another_item() -> bool:
    yesno = input_say("Do you need anything else? ").lower()
    if yesno in {"yes", "no"}:
        say_print("OK.")
        return yesno == "yes"
    else:
        say_print("I'm sorry I didn't understand that. Please say yes or no.")
        return needs_another_item()
    

def handle_customer():
    say_print("Welcome to the Dog Treat Store!")
    say_inventory()
    items = []
    items.append(get_next_item())
    while needs_another_item():
        items.append(get_next_item())
    price = sum(INVENTORY[item] for item in items)
    get_payment(price)
    say_print("Here are your dog treats! Thank you!")

if __name__ == "__main__":
    while True:
        handle_customer()
        say_print("Next customer!")
        print('\n')
        
    