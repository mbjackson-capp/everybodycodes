from input_data import q3_p1, q3_p2, q3_p3

from collections import Counter
import heapq
from typing import List

# Problem statement: https://everybody.codes/event/2025/quests/3


def parse_crates(crate_str: str) -> List[int]:
    return [int(i) for i in crate_str.split(",")]


p1_data = parse_crates(q3_p1)
p2_data = parse_crates(q3_p2)
p3_data = parse_crates(q3_p3)


def part1(data: List[int]):
    """If a crate must have a strictly smaller number to fit inside a larger one,
    the largest possible packing is just the sum of all distinct integer sizes."""
    return sum(set(data))


def part2(data: List[int], n_crates=20):
    """For the same reason, the solution to part 2 must be the twenty smallest unique integers.
    Implemented using a priority queue for quick repeated extraction of smallest remaining create size.
    """
    data_uniq = list(set(data))
    heapq.heapify(data_uniq)
    total_wt = 0
    for n in range(n_crates):
        smallest_remaining_crate = heapq.heappop(data_uniq)
        total_wt += smallest_remaining_crate
    return total_wt


def part3(data: List[int]):
    """Naively, since crates of equal size cannot be part of the same set, the
    smallest number of sets must be the maximum frequency of any particular size."""
    ctr = Counter(data)
    return max(ctr.values())


if __name__ == "__main__":
    print(f"Part 1 answer: {part1(p1_data)}")
    print(f"Part 2 answer: {part2(p2_data)}")
    print(f"Part 3 test: {part3(p3_data)}")
