import random, itertools
from collections import *
from operator import attrgetter


class Slot(object):
    def __init__(self, win_probability, random):
        self.win_probability = win_probability
        self.random = random
        self.wins = self.losses = 0

    @property
    def pulls(self):
        return self.wins + self.losses

    @property
    def win_ratio(self):
        return self.wins / self.pulls if self.pulls else float('nan')

    def draw(self):
        won = self.random() < self.win_probability
        if won:
            self.wins += 1
        else:
            self.losses += 1
        return won


class Casino(object):
    def __init__(self, remaining_turns, seed=0):
        self.win_probability_factory = random.Random(seed).random
        self.turn_probability_factory = random.Random(seed + 1).random
        self.slots = defaultdict(lambda: Slot(self.win_probability_factory(), self.turn_probability_factory))
        self.remaining_turns = remaining_turns

    def draw(self, slot_index):
        assert self.remaining_turns > 0
        self.remaining_turns -= 1
        return self.slots[slot_index].draw()

    @property
    def wins(self):
        return sum(map(attrgetter('wins'), self.slots.values()))

    @property
    def losses(self):
        return sum(map(attrgetter('losses'), self.slots.values()))

    @property
    def win_ratio(self):
        return self.wins / (self.wins + self.losses)

    @staticmethod
    def faceoff(*ais, num_pulls_per_round=1, seed=0):
        environments = []
        for ai in ais:
            casino = Casino(remaining_turns=num_pulls_per_round, seed=seed)
            environments.append((casino, ai(casino)))
        print ('----------------')
        for casino, ai in environments:
            slot_to_draw = next(ai)
            for i in range(num_pulls_per_round):
                slot = casino.slots[slot_to_draw]
                won = slot.draw()
                slot_to_draw = ai.send(won)
            print('{ai.__name__}: {casino.wins}'.format(**locals()))
        return {ai.__name__: casino for casino, ai in environments}


def apathetic(casino):
    slot_id = 0
    while True:
        won = yield slot_id


def adhd(casino):
    for i in itertools.count():
        won = yield i


def easily_discouraged(casino):
    for slot_num in itertools.count():
        won = True
        while won:
            won = yield slot_num


def nostalgic(casino):
    for slot_num in itertools.count():
        won = True
        while won:
            won = yield slot_num
        favorite_id, _ = max(casino.slots.items(), key=lambda x: x[1].win_ratio)
        won = True
        while won:
            won = yield favorite_id


AIS = adhd, apathetic, easily_discouraged, nostalgic

if __name__ == '__main__':
    import sys
    num_pulls_per_round = int(sys.argv[1])
    num_rounds = int(sys.argv[2])
    rounds = []
    for seed in range(num_rounds):
        rounds.append(Casino.faceoff(
            *AIS,
            seed=seed,
            num_pulls_per_round=num_pulls_per_round
        ))
    ai_to_wins = Counter()
    for round in rounds:
        max_wins = max(casino.wins for casino in round.values())
        winning_ais = [ai for ai, casino in round.items() if casino.wins == max_wins]
        for ai in winning_ais:
            ai_to_wins[ai] += 1
    for ai in AIS:
        wins = ai_to_wins[ai.__name__]
        print('{ai.__name__}:\n\twins={wins}\n\tlosses={losses}'.format(
            wins=wins,
            losses=num_rounds - wins,
            ai=ai
        ))
    print('{ai}, YOU ARE WINNER!'.format(ai=ai_to_wins.most_common(1)[0][0]))









