from input_data import q16_p1, q16_p2, q16_p3
from typing import List
from functools import reduce

# Problem statement: https://everybody.codes/event/2025/quests/16


def wall_block_count(spell: str, width: int = 90) -> int:
    """Compute how many blocks must be in a wall of a particular width,
    given the spell used to build the wall as described in problem statement."""
    spell = [int(i) for i in spell.split(",")]
    total_blocks = 0
    for interval in spell:
        total_blocks += width // interval
    return total_blocks


def reverse_engineer_spell(fragment: str) -> List[int]:
    """Determine what spell must have been used to create a wall whose leftmost
    columns have numbers of blocks as depicted in the inputted fragment."""
    # pad with a 0 to keep 1-based indexing for simplicity
    fragment = [0] + [int(i) for i in fragment.split(",")]
    spell = []
    number = 1
    while set(fragment) != {0}:
        if fragment[number] > 0:
            for i in range(number, len(fragment), number):
                fragment[i] -= 1
            spell.append(number)
        number += 1
    return spell


def part2(fragment: str) -> int:
    spell = reverse_engineer_spell(fragment)
    return reduce(lambda a, b: a * b, spell)


BUILDER_BLOCKS_COUNT = 202_520_252_025_000


def part3(fragment: str, num_blocks: int = BUILDER_BLOCKS_COUNT) -> int:
    """Given a fragment representing the columns at the left end of a wall,
    reverse engineer the spell that generated the wall fragment, then
    determine the largest width of wall that spell can construct from a given
    number of blocks."""
    spell = reverse_engineer_spell(fragment)
    spell_str = str(spell)[1:-1]
    poss_width = 1
    widths_considered = []
    # try powers of 2 for widths, until we reach a width that is too wide
    while True:
        # get how many blocks a wall of this width would take (extras discarded)
        wbc = wall_block_count(spell_str, width=poss_width)
        widths_considered.append(poss_width)
        if wbc > num_blocks:
            break
        else:
            poss_width *= 2
    # switch into binary search mode with last two widths attempted as bounds
    lb, ub = widths_considered[-2:]
    while abs(ub - lb) > 1:
        poss_width = (lb + ub) // 2
        wbc = wall_block_count(spell_str, width=poss_width)
        if wbc > BUILDER_BLOCKS_COUNT:
            ub = poss_width
        else:
            lb = poss_width
    # If lower bound and upper bound differ by 1, the upper bound wall length
    # is a smidge too long and you should keep the lower one.
    # If they are the same, it doesn't matter anyway!
    return lb


if __name__ == "__main__":
    print(f"Part 1 answer: {wall_block_count(q16_p1)}")
    print(f"Part 2 answer: {part2(q16_p2)}")
    print(f"Part 3 answer: {part3(q16_p3)}")
