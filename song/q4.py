from input_data import q4_p1, q4_p2, q4_p3

from typing import List
from math import floor, ceil


# Problem statement: https://everybody.codes/event/2025/quests/4


def parse_gears(gear_str: str) -> List[int]:
    gear_str_lst = gear_str.split("\n")
    gear_lst = []
    for item in gear_str_lst:
        if "|" in item:
            gear_lst.append([int(i) for i in item.split("|")])
        else:
            gear_lst.append(int(item))
    return gear_lst


data_p1 = parse_gears(q4_p1)
data_p2 = parse_gears(q4_p2)
data_p3 = parse_gears(q4_p3)


def part1(gears: List[int], start_rotations: int = 2025) -> int:
    return floor((gears[0] * start_rotations) / gears[-1])


def part2(gears: List[int], end_rotations: int = 10_000_000_000_000) -> int:
    return ceil((gears[-1] * end_rotations) / gears[0])


def part3(gears: List[int | List], start_rotations: int = 100) -> int:
    cur_rotations = start_rotations
    for i in range(1, len(gears)):
        # rightmost number in previous entry interfaces with leftmost number in this one
        old_gear = gears[i - 1][1] if isinstance(gears[i - 1], list) else gears[i - 1]
        new_gear = gears[i][0] if isinstance(gears[i], list) else gears[i]
        new_rotations = (old_gear * cur_rotations) / new_gear
        cur_rotations = new_rotations
    return floor(cur_rotations)


if __name__ == "__main__":
    print(f"Part 1 answer: {part1(data_p1)}")
    print(f"Part 2 answer: {part2(data_p2)}")
    print(f"Part 3 answer: {part3(data_p3)}")
