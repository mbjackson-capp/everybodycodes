from input_data import q13_p1, q13_p2, q13_p3
from typing import List
from tqdm import tqdm


def wheelify(data: str) -> List[int]:
    if "-" in data:
        # Get the full range of integers represented by each line
        ranges = data.split("\n")
        ranges = [i.split("-") for i in ranges]
        ranges = [(int(i[0]), int(i[1])) for i in ranges]
        ranges = [list(range(i[0], i[1] + 1)) for i in ranges]
    else:
        ranges = [[int(i)] for i in data.split("\n")]

    clockwise = [1]
    ccw = []
    for i, rng in tqdm(enumerate(ranges)):
        if i % 2 == 0:
            clockwise = clockwise + rng
        else:
            ccw = list(reversed(rng)) + ccw
    wheel = clockwise + ccw
    return wheel


# TODO: create big_wheelify(), which preserves the ranges' starts-ends as the
# entries of the wheel. Then, when it's time to turn the dial, turn it by the
# sum of those ranges all at once, until what remains is too small to be a full
# turn, then turn it by each range one at a time, until what remains is small
# enough to be within a single range, then add what remains to starting number
# of range to get final answer. Should be much faster for part 3.


def turn_dial(data: str, turns: int = 2025):
    wheel = wheelify(data)
    dial_pos = turns % len(wheel)
    return wheel[dial_pos]


if __name__ == "__main__":
    print(f"Part 1 answer: {turn_dial(q13_p1)}")
    print(f"Part 2 answer: {turn_dial(q13_p2, turns=20252025)}")
    print(f"Now working on Part 3... This could take several minutes...")
    print(f"Part 3 answer: {turn_dial(q13_p3, turns=202520252025)}")
