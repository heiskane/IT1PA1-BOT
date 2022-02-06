from enum import Enum
from itertools import product
import random
from os import urandom


class Suits(Enum):
    diamond = "♦"
    club = "♣"
    heart = "♥"
    spade = "♠"


class Ranks(Enum):
    ace = "A"
    king = "K"
    queen = "Q"
    jack = "J"
    ten = "10"
    nine = "9"
    eight = "8"
    seven = "7"
    six = "6"
    five = "5"
    four = "4"
    three = "3"
    two = "2"


class Card:
    def __init__(self, rank: Ranks, suit: Suits):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        lines = []
        lines.append("╔═════════╗")
        lines.append(f"║{self.rank.value}".ljust(10) + "║")
        lines.append("║         ║")
        lines.append("║         ║")
        lines.append(f"║    {self.suit.value}    ║")
        lines.append("║         ║")
        lines.append("║         ║")
        lines.append("║" + f"{self.rank.value}║".rjust(10))
        lines.append("╚═════════╝")

        return "\n".join(["".join(line) for line in lines])


class Deck:
    def __init__(self, ranks: Ranks, suits: Suits):
        self.ranks = ranks
        self.suits = suits
        self.cards = self.__generate_deck()

    def __generate_deck(self):
        cards = []
        # https://www.geeksforgeeks.org/python-itertools-product/
        for rank, suit in product(self.ranks, self.suits):
            cards.append(Card(rank, suit))

        random.seed(urandom(16))
        random.shuffle(cards)
        return cards

    def reset(self):
        self.cards = self.__generate_deck()

    def draw(self):
        return self.cards.pop() if len(self.cards) != 0 else None


deck = Deck(Ranks, Suits)
