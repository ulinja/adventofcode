"""Solves Advent of Code 2024 - Day 01."""
from aoc.utils.file import get_path_to_input_data, get_lines_from_file


def solve_part_1(lines: list[str]) -> int:
    left_list, right_list = [], []
    for line in lines:
        left_num, right_num = line.split()
        left_list.append(int(left_num))
        right_list.append(int(right_num))

    left_list = sorted(left_list)
    right_list = sorted(right_list)

    sum = 0
    for i in range(len(lines)):
        distance = abs(left_list[i] - right_list[i])
        sum += distance

    return sum


def solve_part_2(lines: list[str]) -> int:
    numbers_in_left_list: set[int] = set()
    count_by_number_in_right_list: dict[int, int] = dict()
    for line in lines:
        left_str, right_str = line.split()
        left_num, right_num = int(left_str), int(right_str)

        numbers_in_left_list.add(left_num)

        right_num_count = count_by_number_in_right_list.get(right_num)
        if right_num_count is None:
            count_by_number_in_right_list[right_num] = 1
        else:
            count_by_number_in_right_list[right_num] = right_num_count + 1

    similarity_score = 0
    for number in numbers_in_left_list:
        count = count_by_number_in_right_list.get(number) or 0
        similarity_score_increase = number * count
        similarity_score += similarity_score_increase

    return similarity_score


def main():
    lines = get_lines_from_file(get_path_to_input_data(24, 1))
    print(f"Solution to part 1: {solve_part_1(lines)}")
    print(f"Solution to part 2: {solve_part_2(lines)}")
