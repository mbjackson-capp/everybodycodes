from input_data import q_11_p1, q_11_p2, q_11_p3
from typing import List, Tuple
from copy import deepcopy
from math import ceil
import numpy as np

# Problem statement: https://everybody.codes/event/2025/quests/11


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
    """Do one round of bird flock rearrangement, assuming left-to-right
    order as in Phase 1."""
    flock = deepcopy(flock)  # to prevent list reference shenanigans
    donors, recipients = find_donors_and_recipients(flock)
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


def run_full_simulation(flock: List[int], debug=False, is_part1: bool = False) -> int:
    """Run a full simuation of flock rebalancing, one round at a time.
    Appropriate for when a specific round needs to be checked irrespective of input.

    For Part 1, returns (int): the checksum after Round 10.
    Otherwise, returns (int): number of rounds that the full simulation
    takes to complete."""

    def printv(x):
        if debug:
            print(x)

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


def advance_fast_simulation(
    old_round_num: int, flock: List[int]
) -> Tuple[int, List[int]]:
    """Helper method used in place of run_round() to run a faster simulation.
    If consecutive rounds would result in transfers from the same donor columns
    to the same recipient columns, simulate all those rounds in one step"""
    # TODO: reorganize to prevent redundant call to find_donors_and_recipients()
    # TODO: check if adding new_rds would take old_round_num over 10; if so,
    # advance to exactly round 10 instead, to replace full_simulation outright
    flock = deepcopy(flock)
    new_rds = num_rounds_to_skip(flock)
    donors, recipients = find_donors_and_recipients(flock)
    for d in donors:
        flock[d] -= new_rds
    for r in recipients:
        flock[r] += new_rds
    new_round_num = old_round_num + new_rds
    return new_round_num, flock


def is_nondecreasing(lst: List[int]) -> bool:
    for i in range(1, len(lst)):
        if lst[i] < lst[i - 1]:
            return False
    return True


def phase_2_num_rounds(sorted_list: List[int]) -> int:
    """When list is non-decreasing, at most one bird transfer goes from the
    leftmost column tied for largest, to the leftmost column tied for smallest.
    Exactly 1 donor, exactly 1 recipient. The recipients will fill up until every
    column is balanced. So all you need to do to count the number of rounds in
    Phase 2 is to count the number of bird transfers. This, in turn, is equal to
    the sum of the differences, across all columns, between the target (mean)
    and that column's value if the column is less than the target mean.
    Credit to Reddit user r/runarmod for inspiring this logic."""
    assert is_nondecreasing(sorted_list), "Can't do phase 2 until phase 1 is done!"
    phase_2_rounds = 0
    target_mean = sum(sorted_list) / len(sorted_list)
    for col in sorted_list:
        if col < target_mean:
            phase_2_rounds += target_mean - col
    return int(phase_2_rounds)


def run_fast_simulation(flock: List[int], debug=False) -> int:
    """Run a simulation of flock rebalancing. In Phase 1, it does this without
    checking each individual round when successive rounds would transfer from
    the same donor columns to the same recipient columns. In Phase 2, it skips
    round-by-round simulation entirely to calculate in one step how many
    remaining rounds are needed.

    Returns (int): number of rounds that a full simulation would take to complete."""

    def printv(x):
        if debug:
            print(x)

    round = 0
    phase = 1
    while phase == 1:
        new_round, new_flock = advance_fast_simulation(round, flock)
        if new_flock == flock and phase == 1:
            printv("No more moves possible in phase 1! Going to phase 2...")
            phase = 2
            break
        else:
            round = new_round
            flock = new_flock
            printv(f"After round {round}: {flock}")
    printv(f"Now quick-calculating number of rounds in Phase 2...")
    p2_rounds = phase_2_num_rounds(flock)
    round += p2_rounds

    printv(f"No more moves possible! Simulation over")
    return round


if __name__ == "__main__":
    q_11_p1 = flockify(q_11_p1)
    q_11_p2 = flockify(q_11_p2)
    q_11_p3 = flockify(q_11_p3)

    sim1 = run_full_simulation(q_11_p1, is_part1=True)
    print(f"Part 1 answer: {sim1}")

    print(f"Now running Part 2..This will take several minutes...")
    sim2 = run_fast_simulation(q_11_p2)
    print(f"Part 2 answer: {sim2}")

    # NOTE: will be fast since Part 3 input is already sorted for all known users
    sim3 = run_fast_simulation(q_11_p3)
    print(f"Part 3 answer: {sim3}")
