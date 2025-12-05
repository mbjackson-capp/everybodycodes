import numpy as np
from typing import List, Tuple

from input_data import q_12_p1, q_12_p2, q_12_p3
from utils import gridify, neighbor_locs

# Problem statement: https://everybody.codes/event/2025/quests/12

EMPTY = -1


def chain_reaction(
    arr: np.array, start: List[Tuple[int, int]] = [(0, 0)], actually_do_it: bool = False
) -> int:
    """Iterative breadth first search with a more explodey flavor to it.
    Returns the number of barrels that are within the chain reaction that begins
    by igniting the barrels at the locations in start list.
    If actually_do_it is set to True, arr is modified IN-PLACE to give each
    location where a barrel would explode a dummy variable indicating that the
    location is now empty (i.e. that the barrel has exploded).
    """
    ignited = start
    kaboomed = set()

    while ignited:
        barrel_loc = ignited.pop(0)
        x, y = barrel_loc
        barrel_size = arr[x][y]
        for neighbor_loc in neighbor_locs(arr, x, y):
            if (
                neighbor_loc not in ignited
                and neighbor_loc not in kaboomed
                and arr[neighbor_loc] != EMPTY
                and arr[neighbor_loc] <= barrel_size
            ):
                ignited.append(neighbor_loc)
        kaboomed.add(barrel_loc)

    if actually_do_it:
        for spot in kaboomed:
            arr[spot] = EMPTY

    return len(kaboomed)


def best_fireball_spot(arr: np.array):
    """"""
    max_kabooms = 0
    best_spot = None
    max_x, max_y = arr.shape
    for x in range(max_x):
        for y in range(max_y):
            spot = (x, y)
            if arr[spot] == EMPTY:
                continue
            kabooms_here = chain_reaction(arr, start=[spot])
            if kabooms_here > max_kabooms:
                print(f"New maximum: {kabooms_here} barrels explode if start at {spot}")
                max_kabooms = kabooms_here
                best_spot = spot
    return best_spot


def part3(arr: np.array) -> int:
    total_kaboomed = 0
    for round in range(3):
        print(f"\nRound {round+1} of 3... This may take a few minutes...")
        greedy_spot = best_fireball_spot(arr)
        this_kaboom = chain_reaction(arr, start=[greedy_spot], actually_do_it=True)
        total_kaboomed += this_kaboom
    return total_kaboomed


if __name__ == "__main__":
    q_12_p1 = gridify(q_12_p1, intify=True)
    q_12_p2 = gridify(q_12_p2, intify=True)
    q_12_p3 = gridify(q_12_p3, intify=True)

    print(f"Part 1 answer: {chain_reaction(q_12_p1)}")

    p2_bottom_right = tuple(i - 1 for i in q_12_p2.shape)
    print(f"Part 2 answer: {chain_reaction(q_12_p2, start=[(0,0), p2_bottom_right])}")

    print("Now doing Part 3...This could take a few minutes...")
    p3_ans = part3(q_12_p3)
    print(f"Part 3 answer: {p3_ans}")
