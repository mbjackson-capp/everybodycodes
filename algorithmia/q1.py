from collections import Counter
from textwrap import wrap
from input_data import q1_input1, q1_input2, q1_input3

potions_needed = {"A": 0, "B": 1, "C": 3, "D": 5}


def potions(fight: str) -> int:
    needed = 0
    if len(fight) == 3:
        needed += 6
    elif len(fight) == 2:
        needed += 2
    for creature in fight:
        needed += potions_needed[creature]
    return needed


def fight_all(data: str, fight_size: int = 1):
    """Get number of potions needed for all fights in given input."""
    fights = [i.replace("x", "") for i in wrap(data, fight_size)]
    potions_by_fight = [potions(fight) for fight in fights]
    return sum(potions_by_fight)


print(f"Part 1 solution: {fight_all(q1_input1, fight_size=1)}")
print(f"Part 2 solution: {fight_all(q1_input2, fight_size=2)}")
print(f"Part 3 solution: {fight_all(q1_input3, fight_size=3)}")
