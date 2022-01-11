from typing import *
from typing import NamedTuple
import random


def load_dictionary(n: int, words_file='/usr/share/dict/words') -> Set[str]:
    """
    Parse the words file and return a list of words of length n.
    """
    with open(words_file, 'r') as f:
        return {word for line in f if len(word := line.lower().strip()) == n}


class Fact(NamedTuple):
    letter: str
    pos: Optional[int]
    in_word: bool
    in_place: bool

    @property
    def color(self):
        if in_place:
            return "green"
        elif in_word:
            return "yellow"
        else:
            return "grey"

    def consistent_with(self, word) -> bool:
        if self.in_place:
            return word[self.pos] == self.letter
        elif self.in_word:
            return self.letter in word
        else:
            return self.letter not in word

    @classmethod
    def for_guess(cls, word, guess) -> List["Fact"]:
        if len(word) != len(guess):
            raise ValueError(f"{len(word)=} != {len(guess)=}")
        facts = []
        for i, (word_letter, guess_letter) in enumerate(zip(word, guess)):
            facts.append(Fact(
                letter=guess_letter,
                pos=i,
                in_word=guess_letter in word,
                in_place=guess_letter == word_letter,
            ))
        return facts


class Game:
    def __init__(self, n, word=None):
        self.n = n
        self.all_words = load_dictionary(n)
        self.words = sorted(list(self.all_words))
        self.facts = set()
        self.word = word or random.choice(list(self.words))
        if len(self.word) != n:
            raise ValueError("bad")

    def make_guess(self, guess):
        if len(guess) != self.n:
            return "bad word; wrong length"
        elif guess not in self.all_words:
            return "not in dictionary"
        if guess == self.word:
            print("Correct!")
            return
        new_facts = Fact.for_guess(word=self.word, guess=guess)
        self.facts.update(new_facts)
        self.words = [
            word for word in self.words
            if all(fact.consistent_with(word) for fact in new_facts)
        ]
        print(f"words remaining: {len(self.words)}")


g = Game(5, word="horse")
g.make_guess("blame")