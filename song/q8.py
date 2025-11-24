from input_data import q8_p1, q8_p2, q8_p3

from itertools import combinations, pairwise
from tqdm import tqdm
from typing import Tuple

test1 = "1,5,2,6,8,4,1,7,3"


def part1(seq: str, num_nails=32):
    center_crosses = 0
    seq = [int(i) for i in seq.split(",")]
    for i, this_pos in enumerate(seq):
        if i == 0:
            continue
        prev_pos = seq[i - 1]
        if abs(this_pos - prev_pos) == num_nails // 2:
            center_crosses += 1
    return center_crosses


def have_overlap(
    r1: Tuple[int, int], r2: Tuple[int, int], include_endpoints=True
) -> bool:
    """
    Determine if two ranges along the same axis/number line have overlap,
    without one range being entirely a subrange of the other.

    Motivation: If you treat the nail numbers that start and end each thread as
    a range, overlap in those ranges is sufficient to establish that their
    intersection must exist within the center of the circle, provided that one
    range is not entirely a subrange of the other. In other words, the problem of
    "whether threads intersect" around a circle reduces entirely to whether ranges
    intersect along a number line, so we don't need to convert nail numbers to
    coordinates, solve analytically for intersections, use shapely, or care about
    how many nails are in the circle in the first place, greatly reducing runtime.

    Special thanks to reddit user u/Horsdudoc for stating this insight succintly.
    """
    # put lower number first in both ranges
    r1_lb = min(r1)
    r1_ub = max(r1)

    r2_lb = min(r2)
    r2_ub = max(r2)

    # swap them so earlier range is always first
    if r2_ub < r1_ub:
        return have_overlap((r2_lb, r2_ub), (r1_lb, r1_ub))

    # make sure one range doesn't strictly contain the other
    if (r1_lb < r2_lb and r1_ub > r2_ub) or (r2_lb < r1_lb and r2_ub > r1_ub):
        return False

    # do proper comparison of greatest lower-bound with least upper-bound
    if r1_ub == r2_lb:
        return include_endpoints
    return r2_lb < r1_ub


def test_have_overlap():
    assert have_overlap((0, 3), (5, 10)) == False
    assert have_overlap((0, 6), (5, 10)) == True
    # should be order-invariant
    assert have_overlap((5, 10), (0, 3)) == False
    assert have_overlap((5, 10), (0, 6)) == True
    assert have_overlap((10, 5), (3, 0)) == False
    assert have_overlap((10, 5), (6, 0)) == True
    # check endpoint exclusion
    assert have_overlap((0, 5), (5, 10), include_endpoints=False) == False
    assert have_overlap((0, 5), (5, 10), include_endpoints=True) == True
    # check non-containment
    assert have_overlap((1, 4), (2, 3)) == False


def intersect_within_circle(
    old_thread: Tuple[int, int], new_thread: Tuple[int, int]
) -> bool:
    """Check whether threads strung between two pairs of start/end points of a
    circular artwork intersect in the circle.
    Note that if they share an endpoint, they can't intersect within circle proper."""
    all_endpoints = {new_thread[0], new_thread[1], old_thread[0], old_thread[1]}
    if len(all_endpoints) < 4:
        return False
    return have_overlap(new_thread, old_thread, include_endpoints=False)


def part2(seq: str):
    seq = list(pairwise([int(i) for i in seq.split(",")]))
    threads = []
    knots = 0
    for new_thread in tqdm(seq):
        for old_thread in threads:
            if intersect_within_circle(new_thread, old_thread):
                knots += 1
        threads.append(new_thread)
    return knots


def part3(seq, num_nails=256):
    threads = list(pairwise([int(i) for i in seq.split(",")]))
    strikes = list(combinations(range(1, num_nails + 1), 2))
    max_cuts = 0
    for strike in tqdm(strikes):
        # must account for, e.g., (3,5) and (5,3) being separate threads
        backward_strike = (strike[1], strike[0])
        # must also account for multiplicity of threads created in same direction
        # between same two nails by using list comprehension instead of set
        cuts = [t for t in threads if intersect_within_circle(strike, t)]
        if strike in threads or backward_strike in threads:
            threads_along_strike = [
                t for t in threads if t in (strike, backward_strike)
            ]
            cuts.append(threads_along_strike)
        if len(cuts) > max_cuts:
            max_cuts = len(cuts)
    return max_cuts


if __name__ == "__main__":
    test_have_overlap()
    print(f"Part 1 answer: {part1(q8_p1)}")
    print(f"Part 2 answer: {part2(q8_p2)}")
    print(f"Now computing Part 3 answer... This may take a few minutes...")
    print(f"Part 3 answer: {part3(q8_p3)}")
