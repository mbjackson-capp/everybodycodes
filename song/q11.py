from input_data import q_11_p1, q_11_p2, q_11_p3
from typing import List, Tuple
from copy import deepcopy
from math import ceil
import numpy as np
import time

# Problem statement: https://everybody.codes/event/2025/quests/11

test1 = """9
1
1
4
9
6"""


def flockify(str) -> List[int]:
    return [int(i) for i in str.split("\n")]


def find_donors_and_recipients(flock: List[int]) -> Tuple[List[int], List[int]]:
    """Assuming that serial bird transfer steps within a round continue to push
    the same bird from one column to the next until that bird reaches a column
    of smaller size than the one to its right (or failing that, the last column),
    find the column indices from which a bird transfer must start (donors)
    and the column indices at which a bird transfer must end (recipients)."""
    donor_ixs = []
    recipient_ixs = []
    to_find_next = "donor"
    for i, col in enumerate(flock):
        try:
            if to_find_next == "donor" and col > flock[i + 1]:
                donor_ixs.append(i)
                to_find_next = "recipient"
            elif to_find_next == "recipient" and col < flock[i + 1]:
                recipient_ixs.append(i)
                to_find_next = "donor"
        except IndexError:  # very last index
            if to_find_next == "recipient":
                recipient_ixs.append(i)
    return donor_ixs, recipient_ixs


def run_round(flock: List[int]) -> np.array:
    """Do one round of the bird flock rearrangement, assuming left-to-right
    order as in Phase 1. (Rather than implement Phase 2 logic separately, we
    reverse the list once at the change of phase and then keep using this)"""
    flock = deepcopy(flock)  # to prevent list reference shenanigans
    donors, recipients = find_donors_and_recipients(flock)
    # TODO: consider replacing with numpy vectorized operation
    for d in donors:
        flock[d] -= 1
    for r in recipients:
        flock[r] += 1
    return flock


def checksum(flock: List[int], phase=1) -> int:
    checksum = 0
    if phase == 2:
        flock = list(reversed(flock))
    for ix, col_count in enumerate(flock):
        checksum += (ix + 1) * col_count
    return checksum


def run_simulation(flock: List[int], debug=False, is_part1: bool = False) -> int:

    def printv(x):
        if debug:
            print(x)

    target = int(sum(flock) / len(flock))
    round = 0
    phase = 1
    while True:
        new_flock = run_round(flock)
        if new_flock == flock and phase == 1:
            printv("No more moves possible in phase 1! Going to phase 2...")
            phase = 2
            # Reversing flock order and running "another phase 1" is numerically
            # equivalent to running phase 2 as described in problem spec.
            # Only catch is, you need to re-reverse to get a correct checksum
            # if you're in phase 2.
            flock = list(reversed(flock))
            continue
        elif new_flock == flock:
            break
        else:
            round += 1
            flock = new_flock
            printv(f"After round {round}: {flock}")
            if round == 10 and is_part1:
                return checksum(flock, phase=phase)
    printv(f"No more moves possible! Simulation over")
    return round


test2 = flockify(
    """805
706
179
48
158
150
232
885
598
524
423"""
)

my_test = [50, 2, 40, 90, 60]

test1 = flockify(test1)
q_11_p1 = flockify(q_11_p1)
q_11_p2 = flockify(q_11_p2)
q_11_p3 = flockify(q_11_p3)


def num_rounds_to_skip(flock: List[int]) -> int:
    gaps = []
    donors, recipients = find_donors_and_recipients(flock)
    # you have to do the logic both ways
    for r in recipients:
        if r - 1 in donors:
            # receiving from neighbor, so cut gap in half to find balancing point
            gaps.append(ceil((flock[r - 1] - flock[r]) / 2))
        else:
            # this stops being a donor when its size strictly exceeds left neighbor's
            gaps.append(flock[r - 1] - flock[r] + 1)  # the +1 might be wrong sometimes
    for d in donors:
        if (d - 1 >= 0) and flock[d - 1] == flock[d]:
            gaps.append(1)
        if d + 1 in recipients:
            # donating to neighbor, so cut gap in half to find balancing point
            gaps.append(ceil((flock[d] - flock[d + 1]) / 2))
        else:
            # this stops being a donor when its size diminishes to right neighbor's
            gaps.append(flock[d] - flock[d + 1])
    return 0 if not gaps else min(gaps)


def test_num_rounds_to_skip():
    assert num_rounds_to_skip([50, 2, 40, 90, 60]) == 15
    assert num_rounds_to_skip([35, 17, 40, 75, 75]) == 9
    assert num_rounds_to_skip([75, 75, 40, 26, 26]) == 1
    assert num_rounds_to_skip([5, 5, 5, 5, 5]) == 0
    assert num_rounds_to_skip([5, 4]) == 1
    assert num_rounds_to_skip([8, 2]) == 3
    assert num_rounds_to_skip([90, 87, 2]) == 3


def advance_simulation(old_round_num: int, flock: List[int]) -> Tuple[int, List[int]]:
    """"""
    # TODO: reorganize to prevent redundant call to find_donors_and_recipients()
    # TODO: you could do something in here to check if new_rds would take old_round_num
    # over 10. if it does, take it to exactly round 10 instead.
    flock = deepcopy(flock)
    new_rds = num_rounds_to_skip(flock)
    donors, recipients = find_donors_and_recipients(flock)
    for d in donors:
        flock[d] -= new_rds
    for r in recipients:
        flock[r] += new_rds
    new_round_num = old_round_num + new_rds
    return new_round_num, flock


def run_fast_simulation(flock: List[int], debug=False) -> int:

    def printv(x):
        if debug:
            print(x)

    round = 0
    phase = 1
    while True:
        new_round, new_flock = advance_simulation(round, flock)
        if new_flock == flock and phase == 1:
            printv("No more moves possible in phase 1! Going to phase 2...")
            phase = 2
            # Reversing flock order and running "another phase 1" is numerically
            # equivalent to running phase 2 as described in problem spec.
            # Only catch is, you need to re-reverse to get a correct checksum
            # if you're in phase 2.
            flock = list(reversed(flock))
            continue
        elif new_flock == flock:
            break
        else:
            round = new_round
            flock = new_flock
            printv(f"After round {round}: {flock}")
            # if round == 10 and is_part1:
            #     return checksum(flock, phase=phase)
    printv(f"No more moves possible! Simulation over")
    return round


def test_find_donors_and_recipients():
    assert find_donors_and_recipients([50, 2, 40, 90, 60]) == ([0, 3], [1, 4])


def test_advance_simiulation():
    assert advance_simulation(0, [50, 2, 40, 90, 60]) == (15, [35, 17, 40, 75, 75])


"""This lets you skip like 45 billion rounds of part 3 right of the bat --
without exaggerating, 45, billion -- but it's still nowhere near fast enough.
Almost all the time, the proper number of rounds to advance the simulation is 1.
Which means that you need to find some other way of predicting the end state
more directly from the start state.

The issue with *that* is that multiple bird transfers happen within the same
round. Even if it's possible to calculate pretty quickly how many transfers
it would take to achieve a completely non-decreasing end state, it's less clear
how to decrement the sum total of birds transferred until you get the number
of rounds of the game as it actually works.

It seems like there's some sort of sorting algorithm being hidden below the
flavor text here, but i'm not sure what. 'Do this transformation on an array of
integers n times until the integers are strictly non-decreasing' likely has a 
clear closed-form solution for all lists of integers but i'm not sure how to get
it. perhaps induct answers for a smaller list into a larger answer?"""

if __name__ == "__main__":
    test_num_rounds_to_skip()
    test_advance_simiulation()

    sim1 = run_simulation(q_11_p1, is_part1=True)
    print(f"Part 1 answer: {sim1}")

    simtest2 = run_simulation(test2)
    simtest2_fast = run_fast_simulation(test2)
    assert simtest2 == simtest2_fast == 1579, f"Expected 1579, got {simtest2}"

    # Warning: this will take several minutes
    sim2 = run_fast_simulation(q_11_p2, debug=True)
    print(f"Part 2 answer: {sim2}")

    # This will take too long and crash your computer
    # sim3 = run_fast_simulation(q_11_p3, debug=True)
