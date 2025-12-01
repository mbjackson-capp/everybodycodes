from input_data import qten_p1, qten_p2

import numpy as np
from functools import cache, reduce
from tqdm import tqdm
from typing import List, Tuple, Set


DRAGON = "D"
SHEEP = "S"
HIDEOUT = "#"
PLAIN = "."


def make_board(board_data: str) -> np.array:
    return np.array([[cell for cell in row] for row in board_data.split("\n")])


def find_dragon(board: np.array) -> Tuple[int, int]:
    dragon_locs = np.argwhere(board == DRAGON)
    assert len(dragon_locs) == 1, f"Should only be 1 dragon, found {len(dragon_locs)}"
    # for readability, turn list of lists of np.int into tuple of base-Python ints
    return tuple([int(i) for i in dragon_locs[0]])


def find_symbol(board: np.array, symbol: str) -> Tuple[np.array, Tuple[int, int]]:
    assert symbol in (SHEEP, HIDEOUT), f"Symbol {symbol} isn't meaningful"
    sym_locs = np.argwhere(board == symbol)
    return set([(int(i[0]), int(i[1])) for i in sym_locs])


@cache
def knight_moves(
    start_space: Tuple[int, int], x_max: int, y_max=int
) -> Set[Tuple[int, int]]:
    """Obtain all the squares to which it is possible to make a legal 'knight move'
    (2 squares forward, one square sideways, where 'forward' can be any direction)
    on a board of this size."""
    x, y = start_space
    # TODO: generate these more elegantly
    move_options = [
        (x + 2, y + 1),
        (x + 2, y - 1),
        (x + 1, y + 2),
        (x + 1, y - 2),
        (x - 1, y + 2),
        (x - 1, y - 2),
        (x - 2, y + 1),
        (x - 2, y - 1),
    ]
    result_set = set()
    for move in move_options:
        x_new, y_new = move
        # make sure only in-bounds moves are kept
        if x_new >= 0 and y_new >= 0 and x_new < x_max and y_new < y_max:
            result_set.add(move)
    return result_set


@cache
def dragon_move_range(
    this_space: Tuple[int, int],
    x_max: int,
    y_max: int,
    moves_left: int,
    strict: bool = False,
) -> List[Tuple[int, int]]:
    """Get the set of all spaces on a board of size (x_max, y_max) that a
    dragon piece starting on this_space can reach in up to n moves.
    (With strict flag, restrict to all pieces it can reach in exactly n moves.)"""
    if moves_left < 0:
        raise ValueError(f"moves_left argument must be non-negative; got {moves_left}")
    # Base case: no more moves to make -- full range is just the space you're on
    if moves_left == 0:
        return {this_space}
    # Recursive step: call function again for every space one knight's move away,
    # then decrement the moves remaining by 1 (until base case is reached)
    outer_hops = reduce(
        set.union,
        [
            dragon_move_range(new_space, x_max, y_max, moves_left - 1, strict=strict)
            for new_space in knight_moves(this_space, x_max, y_max)
        ],
    )
    if not strict:
        # To get all options within UP TO n hops, rather than EXACTLY n hops,
        # don't forget to include starting space in result set
        return outer_hops | {this_space}
    return outer_hops


def get_edible_sheep_locs(
    dragon_spaces: Set[Tuple[int, int]],
    sheep_spaces: Set[Tuple[int, int]],
    hideout_spaces: Set[Tuple[int, int]],
) -> Set[Tuple[int, int]]:
    return dragon_spaces.intersection(sheep_spaces) - hideout_spaces


def move_sheep(sheep_locs: List[Tuple[int, int]], b: np.array) -> Set[Tuple[int, int]]:
    """Move every surviving sheep in accordance with the rules for their turn."""
    x_max = b.shape[0]
    new_sheep_locs = set()
    for loc in sheep_locs:
        x, y = loc
        new_loc = (x + 1, y)
        if x + 1 < x_max:  # sheep that run 'off' the board 'escape'
            new_sheep_locs.add(new_loc)
    return new_sheep_locs


def part1(data: str, moves_allowed=4) -> int:
    b = make_board(data)
    dragon_space = find_dragon(b)
    sheep_spaces = find_symbol(b, SHEEP)
    x_max, y_max = b.shape
    dragon_range = dragon_move_range(dragon_space, x_max, y_max, moves_allowed)
    sheep_in_danger = get_edible_sheep_locs(dragon_range, sheep_spaces, set())
    return len(sheep_in_danger)


def part2(data: str, n_turns=20) -> int:
    b = make_board(data)
    dragon_space = find_dragon(b)
    sheep_spaces = find_symbol(b, SHEEP)
    hideout_spaces = find_symbol(b, HIDEOUT)
    x_max, y_max = b.shape
    total_edible_ever = 0

    for turn in tqdm(range(1, n_turns + 1)):
        # Dragon takes its move
        this_turn_dragon_range = dragon_move_range(
            dragon_space, x_max, y_max, turn, strict=True
        )
        # Check which sheep are edible after dragon has moved
        edible_check_a = get_edible_sheep_locs(
            this_turn_dragon_range, sheep_spaces, hideout_spaces
        )
        sheep_spaces = sheep_spaces - edible_check_a
        # Sheep take their move; survivors at edge of board exit
        sheep_spaces = move_sheep(sheep_spaces, b)
        # Check which sheep are edible after sheep have moved
        edible_check_b = get_edible_sheep_locs(
            this_turn_dragon_range, sheep_spaces, hideout_spaces
        )
        sheep_spaces = sheep_spaces - edible_check_b

        total_edible_this_turn = len(edible_check_a) + len(edible_check_b)
        total_edible_ever += total_edible_this_turn

    return total_edible_ever


if __name__ == "__main__":
    print(f"Part 1 answer: {part1(qten_p1)}")
    print(f"Part 2 answer: {part2(qten_p2, n_turns=20)}")
