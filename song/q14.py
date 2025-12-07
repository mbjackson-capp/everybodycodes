import numpy as np
from copy import deepcopy
from tqdm import tqdm
from utils import gridify, neighbors

from input_data import q14_p1, q14_p2, q14_p3


ON = "#"
OFF = "."


def num_active_diag_neighbors(arr, x, y) -> int:
    nbrs = neighbors(arr, x, y, include_diag=True, include_plus=False)
    return len([nbr for nbr in nbrs if nbr == ON])


def tile_next_round(arr, x, y) -> str:
    cur_state = arr[x][y]
    if cur_state == ON:
        return ON if num_active_diag_neighbors(arr, x, y) % 2 == 1 else OFF
    elif cur_state == OFF:
        return ON if num_active_diag_neighbors(arr, x, y) % 2 == 0 else OFF
    else:
        raise ValueError(
            f"Current state of array[x][y] must be active {ON} or inactive {OFF}"
        )


def next_round(arr: np.array) -> np.array:
    max_x, max_y = arr.shape
    next_arr = deepcopy(arr)
    # TODO: this in a less loopy manner
    for x in range(max_x):
        for y in range(max_y):
            next_arr[x][y] = tile_next_round(arr, x, y)
    return next_arr


def total_tiles_across_rounds(data: str, rounds: int = 10) -> int:
    arr = gridify(data)
    total = 0
    for _ in tqdm(range(rounds)):
        arr = next_round(arr)
        active_tiles = len(np.argwhere(arr == ON))
        total += active_tiles
    return total


def center_n_by_n(arr: np.array, n=8) -> np.array:
    max_x, max_y = arr.shape
    assert max_x > n and max_y > n, f"Grid too small to excerpt an {n}x{n} piece of!"
    assert max_x == max_y, "Grid not square!"
    assert n % 2 == 0, f"{n} is not even! Square will look bad and not be centered!"
    center_pt = max_x // 2
    lb = center_pt - (n // 2)
    ub = center_pt + (n // 2)
    center_square = deepcopy(arr[lb:ub, lb:ub])
    return center_square


ALL_OFF = """..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
..................................
.................................."""

P3_ROUNDS = 1_000_000_000


def part3(rounds: int = P3_ROUNDS, pattern: str = q14_p3):
    arr = gridify(ALL_OFF)
    pattern = gridify(pattern)
    center_pattern_states = {}
    intervals = []
    last_match_rd = None
    in_check_mode = False

    # Set things up as if to get the answer "the long way". But we'll stop early
    for r in tqdm(range(1, rounds + 1)):
        arr = next_round(arr)
        center = center_n_by_n(arr, n=8)
        if (center == pattern).all():
            # Ding ding! the pattern matches in the center.
            # Save how many intervals it took between the last round with a match
            # and this one
            interval = None if not intervals else (r - last_match_rd)
            intervals.append(interval)
            last_match_rd = r
            # Save a snapshot of what the whole floor looks like right now
            center_pattern_states[r] = deepcopy(arr)

            """Key insight: The floor will eventually reach a periodic oscillation
            of the same states, i.e. a cycle. We need to detect when that happens.
            When it does, we can calculate how many active tiles
            appear during all pattern-match rounds in one cycle, and multiply
            by how many cycles occur within the full number of rounds.
            That (plus some edge case stuff to account for pre-cycle rounds and
            a potentially incomplete cycle at the end) will be our answer."""
            # Cycle detection stage 1: see if the current interval list matches
            # any previous intervals
            if not in_check_mode:
                for i, old_interval in enumerate(intervals):
                    if interval == old_interval and i != len(intervals) - 1:
                        # Bingo! a repeat.
                        in_check_mode = True
                        # The length of the cycle, if this turns out to be a cycle,
                        # is the number of rounds (or intervals) between the first
                        # instance and this one.

                        potential_cycle_len = len(intervals) - 1 - i
                        potential_cycle_start_ix = i
                        length_to_check_until = len(intervals) + len(intervals) - 1 - i
            if in_check_mode and len(intervals) == length_to_check_until:
                # Cycle detection stage 2: check that many rounds ahead
                # and make sure the intervals all exactly match
                first_cycle_candidate = intervals[
                    potential_cycle_start_ix : potential_cycle_start_ix
                    + potential_cycle_len
                ]
                second_cycle_candidate = intervals[
                    potential_cycle_start_ix + potential_cycle_len : -1
                ]
                if first_cycle_candidate == second_cycle_candidate:
                    # Cycle detection stage 3: Check that the actual patterns
                    # at each stage of both sequences are the same
                    first_cycle_indices = list(center_pattern_states.keys())[
                        potential_cycle_start_ix : potential_cycle_start_ix
                        + potential_cycle_len
                    ]
                    second_cycle_indices = list(center_pattern_states.keys())[
                        potential_cycle_start_ix
                        + potential_cycle_len : potential_cycle_start_ix
                        + (2 * potential_cycle_len)
                    ]
                    for i in range(len(first_cycle_indices)):
                        assert (
                            center_pattern_states[first_cycle_indices[i]]
                            == center_pattern_states[second_cycle_indices[i]]
                        ).all()
                    # Okay, we're pretty confident now that this represents a
                    # real cycle of floor states.
                    # # TODO: I'm not convinced that this is
                    # provably true in all cases, though... say we find
                    # [3, 3, 6, 3, 3, 6] but the real cycle is [3, 3, 6, 3, 3, 6, 60]?
                    # prove that this approach actually works for all possible
                    # input patterns; doesn't just get lucky on test case & my input

                    # Calculate how long a cycle is and how many active tiles there
                    # are on pattern-matching rounds within a cycle
                    cycle_round_length = first_cycle_indices[-1] - min(
                        center_pattern_states.keys()
                    )
                    num_cycle_occurrences = rounds // cycle_round_length
                    patterns_in_cycle = [
                        center_pattern_states[rd] for rd in first_cycle_indices
                    ]
                    active_tiles_per_cycle = sum(
                        [len(np.argwhere(arr == ON)) for arr in patterns_in_cycle]
                    )
                    rough_answer = active_tiles_per_cycle * num_cycle_occurrences
                    # go through the pre-full-cycle rounds and count out how
                    # many active tiles show up in the pattern through that
                    # much of a cycle
                    remainder = rounds % num_cycle_occurrences

                    patterns_in_remainder = [
                        center_pattern_states[key]
                        for key in list(center_pattern_states.keys())
                        if key < remainder
                    ]
                    active_tiles_in_remainder = sum(
                        [len(np.argwhere(arr == ON)) for arr in patterns_in_remainder]
                    )
                    # Get your final answer
                    answer = rough_answer + active_tiles_in_remainder
                    return answer


if __name__ == "__main__":
    print(f"Part 1 answer: {total_tiles_across_rounds(q14_p1)}")
    print(f"Part 2 answer: {total_tiles_across_rounds(q14_p2, rounds=2025)}")
    print(
        f"Now doing Part 3... This could take a minute..."
        "(don't worry, it stops way before the last round)"
    )
    p3_ans = part3(rounds=P3_ROUNDS)
    print(f"Part 3 answer: {p3_ans}")
