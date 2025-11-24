from input_data import q8_p1, q8_p2
from tqdm import tqdm

from math import cos, sin, pi
from itertools import pairwise
from shapely import LineString
from typing import Tuple, List


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


def construct_frame(num_nails=8) -> dict:
    CIRCUMFERENCE = 2 * pi
    TOL = 1e-15
    increment = CIRCUMFERENCE / num_nails
    nail_spots = {}
    for nail in range(num_nails):
        spot = nail + 1  # nails in problem spec increment from 1
        angle = increment * nail
        x = 0 if abs(sin(angle)) < TOL else sin(angle)
        y = 0 if abs(cos(angle)) < TOL else cos(angle)
        nail_spots[spot] = (x, y)
    return nail_spots


def make_artwork(seq: str, num_nails=256) -> Tuple[List[LineString], int]:
    nails = construct_frame(num_nails=num_nails)
    string_specs = list(pairwise([int(i) for i in seq.split(",")]))
    strings = []
    knot_count = 0
    for spec in tqdm(string_specs):
        start, end = spec
        start_xy = nails[start]
        end_xy = nails[end]
        new_string = LineString([start_xy, end_xy])
        for string in strings:
            # make sure they don't have a start or end point in common
            all_termina = {
                string.coords[0],
                string.coords[1],
                new_string.coords[0],
                new_string.coords[1],
            }
            if len(all_termina) < 4:
                continue
            if string.intersects(new_string):
                knot_count += 1
        strings.append(new_string)
    print(f"Total knots: {knot_count}")
    return strings, knot_count


if __name__ == "__main__":
    print(f"Part 1 answer: {part1(q8_p1)}")
    print(f"Now calculating Part 2...this could take a few minutes...")
    _, p2_ans = make_artwork(q8_p2)
    print(f"Part 2 answer: {p2_ans}")
