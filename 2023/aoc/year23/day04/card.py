"""Classes representing scratch cards."""

from math import floor
from typing import List, Tuple
from pathlib import Path
from dataclasses import dataclass


class Card:
    """Represents a scratch card.

    A scratch card has an ID, a set of winning numbers, and a set of owned numbers.

    Let W be the set of winning numbers, and O be the set of owned numbers.
    Then, the total score of a scratch card is calculated as s = ⌊2^(|W ∩ O| - 1)⌋

    Attributes
    ----------
    id : int
        The id of the Card.
    winning_numbers : set(int)
        The scratchcard's set of winning numbers.
    owned_numbers : set(int)
        The scratchcard's set of owned numbers.
    total_score : int
        The total point score of this scratchcard.
    winning_matches : int
        The number of matches between owned and winning numbers on this card.
    """

    def __init__(self, input_str: str):
        """Parses a line of input text to construct a Card.

        The input line is expected to be of the following format:
        `Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53`
        whereby the card id is `1`, the set of winning numbers is `41 48 83 86 17`, and
        the set of owned numbers is `83 86  6 31 17  9 48 53`.

        Parameters
        ----------
        input_str : str
            The input line to parse as a Card.

        Raises
        ------
        TypeError
            If `input_str` is not of type 'str'.
        """

        if not isinstance(input_str, str):
            raise TypeError(f"Expected input line to be of type 'str', but got '{type(input_str)}'.")

        if input_str.endswith("\n"):
            input_str = input_str[:-1]

        _card_id_str, _number_sets_str = input_str.split(": ")
        self.id = int(_card_id_str[5:])

        _winning_numbers_str, _owned_numbers_str = _number_sets_str.split(" | ")
        self.winning_numbers = {int(n) for n in _winning_numbers_str.split(" ") if n != ""}
        self.owned_numbers = {int(n) for n in _owned_numbers_str.split(" ") if n != ""}

        self.winning_matches = len(self.winning_numbers.intersection(self.owned_numbers))
        self.total_score = floor(2**(self.winning_matches) - 1)


@dataclass
class CardStack:
    card: Card
    stack_count: int = 1


class CardCopier:
    """Represents the card copying game, where card copies of subsequent cards are awarded based on winning matches.

    In a card copier, a (virtual) stack is created for each Card ID. Initially, each stack contains a single copy of the
    card with that ID.
    Beginning with the first stack, its card is evaluated, and copies of subsequent cards are added to their respective
    stacks as necessary. Then, the next stack is examined and for each copy of the card present in it, copies are created
    in subsequent stacks. This process is repeated until there are no more stacks left to examine. Finally, the combined
    number of cards across all stacks is calculated.

    Attributes
    ----------
    stacks : List[CardStack]
        A list containing the virtual stacks of Cards.
    """

    def __init__(self, input_file_path: str | Path):
        """Parses a data file containing rows of Card data, and constructs a CardCopier from it.

        Parameters
        ----------
        input_file_path : str | Path
            Path to the data file describing the Cards.

        Raises
        ------
        FileNotFoundError
            If the file pointed to by `input_file_path` does not exist.
        """

        if not isinstance(input_file_path, (str, Path)):
            raise TypeError(f"Expected input file path to be of type 'str' or 'pathlib.Path', but got '{type(input_file_path)}'.")

        input_file_path = Path(input_file_path).resolve().absolute()
        if not input_file_path.is_file():
            raise FileNotFoundError(f"File does not exist: '{input_file_path}'.")

        self.stacks: List[CardStack] = []

        with open(input_file_path) as input_file:
            for line in input_file.readlines():
                self.stacks.append(CardStack(Card(line)))

        for stack in self.stacks:
            current_card = stack.card
            current_card_id = current_card.id
            next_card_id = current_card_id + 1
            ids_to_be_copied = range(next_card_id, next_card_id + current_card.winning_matches)
            for n in range(stack.stack_count):
                for id in ids_to_be_copied:
                    self.stacks[id - 1].stack_count += 1
