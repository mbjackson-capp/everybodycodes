from input_data import q1_p1, q1_p2, q1_p3
import re
from typing import List, Tuple

# Problem statement: https://everybody.codes/event/2025/quests/1


def parse_data(data: str) -> Tuple[List[str], List[str]]:
    names, instructions = re.split(r"\n+", data)
    names = names.split(",")
    instructions = instructions.split(",")
    return names, instructions


def parse_instruction(instruction: str) -> Tuple[str, int]:
    assert len(instruction) >= 2 and instruction[0] in (
        "L",
        "R",
    ), f"Expected instruction of L or R followed bt integer, got {instruction}"
    dir = instruction[0]
    steps = int(instruction[1:])
    return dir, steps


def part1(data: str):
    names, instructions = parse_data(data)
    pos = 0
    LEFT_BOUND = 0
    RIGHT_BOUND = len(names) - 1
    for instruction in instructions:
        dir, steps = parse_instruction(instruction)
        if dir == "R":
            pos = min(pos + steps, RIGHT_BOUND)
        elif dir == "L":
            pos = max(pos - steps, LEFT_BOUND)
    return names[pos]


def part2(data: str):
    names, instructions = parse_data(data)
    pos = 0
    MODULUS = len(names)
    for instruction in instructions:
        dir, steps = parse_instruction(instruction)
        if dir == "R":
            pos = (pos + steps) % MODULUS
        elif dir == "L":
            pos = (pos - steps) % MODULUS
    return names[pos]


def part3(data: str):
    names, instructions = parse_data(data)
    # imagine position 0 is top of circle; higher indices go clockwise
    MODULUS = len(names)
    for instruction in instructions:
        dir, steps = parse_instruction(instruction)
        pos = (-steps % MODULUS) if dir == "L" else (steps % MODULUS)
        top_name = names[0]
        swap_with_name = names[pos]

        names[0] = swap_with_name
        names[pos] = top_name

    return names[0]


if __name__ == "__main__":
    print(f"Part 1 answer: Your name is {part1(q1_p1)}!")
    print(f"Part 2 answer: Your first parent's name is {part2(q1_p2)}!")
    print(f"Part 3 test: Your second parent's name is {part3(q1_p3)}!")
