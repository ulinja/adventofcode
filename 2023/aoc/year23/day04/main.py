"""Solves Advent of Code 2023 - Day 04."""

from typing import List

from aoc.utils.file import get_lines_from_file, get_path_to_input_data
from aoc.year23.day04.card import Card, CardCopier


def main():
    path_to_data_file = get_path_to_input_data(23, 4)
    lines: List[str] = get_lines_from_file(path_to_data_file)

    scores_sum = 0
    for line in lines:
        card = Card(line)
        scores_sum += card.total_score

    card_copier = CardCopier(path_to_data_file)
    stacks_sum = 0
    for stack in card_copier.stacks:
        stacks_sum += stack.stack_count

    print(f"Sum of all card scores (Part I): {scores_sum}")
    print(f"Total number of scratchcards after copying (Part II): {stacks_sum}")
