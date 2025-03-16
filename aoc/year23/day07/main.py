"""Solves Advent of Code 2023 - Day 07."""

from typing import List

from aoc.utils.file import get_lines_from_file, get_path_to_input_data
from aoc.year23.day07.camelcard import CamelCardGame


def main():
    path_to_data_file = get_path_to_input_data(23, 7)
    lines: List[str] = get_lines_from_file(path_to_data_file)
    camel_card_game = CamelCardGame(lines)

    winnings = 0
    for rank, bet in enumerate(sorted(camel_card_game.bets), start=1):
        winnings += rank * bet[1]

    print(f"Total winnings (Part I): {winnings}")
    #print(f"Count of winning race conditions with bad kerning (Part II): {race_win_product_bad_kerning}")
