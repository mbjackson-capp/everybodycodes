from input_data import q8_p1

from math import cos, sin, pi
from itertools import pairwise
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


# what tying a knot means: this new line segment intersects with a previous line segment
# how to check if two line segments intersect: represent them as linear equations and solve for the point where they are equal
# this requires constructing the outside of the artwork as points in a 2 dimensional space, such that slopes and intercepts can be calculated
# scale is sort of arbitrary, so we may as well treat it as the unit circle

# note: math.cos and math.sin take radians


def construct_frame(num_nails=8):
    CIRCUMFERENCE = 2 * pi
    THRESHOLD = 1e-15
    increment = CIRCUMFERENCE / num_nails
    nail_spots = {}
    for nail in range(num_nails):
        spot = nail + 1  # nails in problem spec increment from 1
        angle = increment * nail
        # NOTE: you'll need to use approximate intersection here
        # because you get values like 6.12e-17 instead of flat 0
        x = 0 if abs(sin(angle)) < THRESHOLD else sin(angle)
        y = 0 if abs(cos(angle)) < THRESHOLD else cos(angle)
        nail_spots[spot] = (x, y)
    return nail_spots


def string_slope(frame: dict, nail_a: int, nail_b: int) -> float:
    pt_a = frame[nail_a]
    pt_b = frame[nail_b]
    rise = pt_b[1] - pt_a[1]
    run = pt_b[0] - pt_a[0]
    try:
        return rise / run
    except ZeroDivisionError:
        return float("inf")


def have_overlap(
    r1: Tuple[int, int], r2: Tuple[int, int], include_endpoints=True
) -> bool:
    """Determine if two ranges along the same axis/number line have overlap"""
    # put lower number first in both ranges
    r1_lb = min(r1)
    r1_ub = max(r1)

    r2_lb = min(r2)
    r2_ub = max(r2)

    # swap them so earlier range is always first
    if r2_ub < r1_ub:
        return have_overlap((r2_lb, r2_ub), (r1_lb, r1_ub))

    # do proper comparison of greatest lower-bound with least upper-bound
    if r1_ub == r2_lb:
        return include_endpoints
    return r2_lb < r1_ub


def test_have_overlap():
    assert 5 > 3
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


def part2(seq: str, num_nails=256):
    pass


# intercept form will fail because vertical strings don't have an intercept

"""Okay, let's think some more. equation solvers in python are clunky and don't deal with approximates well.
So what does make sense.
You know that this is O(n^2) because each new string you add has to look at all previous strings
What does the comparison between two particular strings look like?
Say you have a string (1,5) and are adding a new one (5,2).
What do you know?
You know the endpoints, and thus the slope between them, and thus the range in
x covered by the previous string, and the range in y covered by the previous string.
In our 8-nail case, the string (1,5) has endpoints at Point(0, 1) and Point(0, -1)
This means its x-values range from 0 to 0, and its y-values range from 1 to -1.

The string (5,2) has endpoints at Point(0, -1) and Point(.707, .707).
Trivial overlap of the endpoints has to not count
Do any of the points between Point(0, -1) and Point(.707, .707) EXCLUSIVE of the endpoints
have an x value between 0 and 0? No they do not, so there cannot be an intersection

Now let's think about a comparison between (1,5) and (2,6)
The string (2,6) has endpoints at Point(.707, .707) and Point(-.707, -.707)
Do any of the point STRICTLY between those have an x value between 0 and 0? Yes
Do any of the points STRICTLY between those have a y value between 1 and -1? Yes
This is going to be way overinclusive I fear

Do we need to *find* the point at which the intersection occurs (at least in part 2)?
No! We just have to demonstrate THAT it exists


This overlap region approach is going to fail
consider a string art that starts with (5,2) and then goes to (2,6)
these are the only two strings on it
an overlap approach would verify that their x coordinates overlap from 0 to .707
and that their y coordinates overlap from .707 to -.707
it would find that there exists a bounding box containing some points from both strings
but it doesn't establish that that bounding box contains a genuine intersection

in other words, you can narrow down where an intersection must be *if* it exists

you may need to do some fuckass binary search to some acceptable level of tolerance
you could check each of the four quadrant of the box to see if both lines are still in it
then zoom in on the quadrant still containing both points
until you reach some acceptable level of tolerance (it would take 20 iterations to reach 1e-6, 30 to reach 1e-9)


if the two strings share exactly one endpoint, they don't intersect. this is a hard fast rule
so you don't need to check it
hold on it's simpler than this
if the two strings share two endpoints, you'd have to tie infinite knows, let's hope this never occurs

if the strings don't share either endpoint:
    -if they have the same slope: they're parallel, no knot
    -if they don't: they MUST intersect somewhere on this plane. Only question is whether that intersection is inside the artwork or outside it
        - find that intersection (x,y)
        - return (x ** 2 + y ** 2) < 1 # and therefore inside the unit circle
this can be done in roughly constant time 

Intersection formula resources:
https://en.wikipedia.org/wiki/Line–line_intersection#Given_two_points_on_each_line_segment
https://math.stackexchange.com/questions/3981356/check-if-two-lines-intersect 
https://docs.sympy.org/latest/modules/geometry/utils.html
https://shapely.readthedocs.io/en/2.1.1/manual.html (intersect with buffer)

"""

if __name__ == "__main__":
    print(f"Part 1 test: {part1(test1, num_nails=8)}")
    print(f"Part 1 answer: {part1(q8_p1)}")
    frame = construct_frame()
    print(frame)
    print(list(pairwise([i for i in test1.split(",")])))
    print(string_slope(frame, 1, 5))
    test_have_overlap()
