"""Classes representing the poker-like camel cards game."""

from typing import List, Tuple
from functools import total_ordering

from aoc.utils import assertions


@total_ordering
class Card:
    """Represents a Card in a game of camel cards.

    Attributes
    ----------
    rank : str
        Alphanumeric rank of the Card, which represents its value relative to another Card.
    """

    _RANK_ORDER = {
        "2": 1,
        "3": 2,
        "4": 3,
        "5": 4,
        "6": 5,
        "7": 6,
        "8": 7,
        "9": 8,
        "T": 9,
        "J": 10,
        "Q": 11,
        "K": 12,
        "A": 13,
    }

    def __init__(self, rank: str):
        assertions.is_string_non_empty(rank)
        if rank not in Card._RANK_ORDER:
            raise ValueError(f"Expected Rank to be one of '{Card._RANK_ORDER.keys()}' but got '{rank}'.")

        self.rank = rank

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(rank={self.rank})"

    def __str__(self) -> str:
        return f"<{self.rank}>"

    def __eq__(self, other: "Card") -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return Card._RANK_ORDER[self.rank] == Card._RANK_ORDER[other.rank]

    def __lt__(self, other: "Card") -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return Card._RANK_ORDER[self.rank] < Card._RANK_ORDER[other.rank]


@total_ordering
class Hand:
    """A Hand is a combination of five cards.

    Hands have a strength which depends on the combination of its Card's ranks.

    Attributes
    ----------
    cards : List[Card]
        The list of Cards making up this Hand.
    strength : int
        An integer value representing the strength of this hand, with the lowest combination (high-card) being 0
        and the highest combination (five-of-a-kind) being 6. Note that this value does not take into account the
        alphanumeric ordering of its card ranks, so this value alone should not be used to compare two hands with
        equally strong combinations (e.g. five-of-a-kind and five-of-a-kind).
    """

    @staticmethod
    def _get_hand_strength(input_str: str) -> int:
        """Determines the strength value of a given input string."""

        assertions.is_string_non_empty(input_str)
        if not len(input_str) == 5:
            raise ValueError(f"Expected input string for Hand to be of length 5.")
        for char in input_str:
            if char not in Card._RANK_ORDER:
                raise ValueError(f"Invalid card rank in input string: '{char}'.")

        rank_set = {rank for rank in input_str}

        if len(rank_set) == 5:
            # high-card
            return 0
        elif len(rank_set) == 4:
            # one-pair
            return 1
        elif len(rank_set) == 3:
            # two-pair or three-of-a-kind
            max_same_card_count = 0
            for rank in rank_set:
                same_card_count = list(input_str).count(rank)
                if same_card_count > max_same_card_count:
                    max_same_card_count = same_card_count
            if max_same_card_count == 2:
                # two-pair
                return 2
            # three-of-a-kind
            return 3
        elif len(rank_set) == 2:
            # full-house or four-of-a-kind
            max_same_card_count = 0
            for rank in rank_set:
                same_card_count = list(input_str).count(rank)
                if same_card_count > max_same_card_count:
                    max_same_card_count = same_card_count
            if max_same_card_count == 4:
                # four-of-a-kind
                return 5
            # full-house
            return 4
        else:
            # five-of-a-kind
            return 6

    def __init__(self, input_str: str):
        """Constructs a Hand from an input string.

        The input string is expected to be of the following format: "564QKA".
        """

        assertions.is_string_non_empty(input_str)
        if not len(input_str) == 5:
            raise ValueError(f"Expected input string for Hand to be of length 5.")

        self.cards: List[Card] = []
        for char in input_str:
            self.cards.append(Card(rank=char))

        self.strength = Hand._get_hand_strength(input_str)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(cards={self.cards})"

    def __str__(self) -> str:
        return f"<{''.join([card.rank for card in self.cards])}>"

    def __eq__(self, other: "Hand") -> bool:
        if not isinstance(other, Hand):
            return NotImplemented
        if self.strength != other.strength:
            return False

        return self.cards == other.cards

    def __lt__(self, other: "Hand") -> bool:
        if not isinstance(other, Hand):
            return NotImplemented
        if self.strength != other.strength:
            return self.strength < other.strength

        for self_card, other_card in zip(self.cards, other.cards):
            if self_card == other_card:
                continue
            return self_card < other_card
        return False


class CamelCardGame:
    """Represents a Game of Camel Cards, consisting of a list of hands, each with a corresponding bid.

    Attributes
    ----------
    bets : List[Tuple[Hand, int]]
        A List of Hand/Bid pairs.
    """

    def __init__(self, input_lines: List[str]):
        """Constructs a CamelCardGame from the lines of an input data file.

        The input data lines are expected to have the following format:
        [
            '32T3K 765\n',
            'T55J5 684\n',
            'KK677 28\n',
            'KTJJT 220\n',
            'QQQJA 483'
        ]
        """

        self.bets: List[Tuple[Hand, int]] = []
        for line in input_lines:
            if line.endswith("\n"):
                line = line[:-1]
            hand_str, bid_str = line.split(" ")
            self.bets.append((Hand(hand_str), int(bid_str)))
