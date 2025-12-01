from input_data import qten_p1

import numpy as np
from functools import reduce
from typing import List, Tuple

test1 = """...SSS.......
.S......S.SS.
..S....S...S.
..........SS.
..SSSS...S...
.....SS..S..S
SS....D.S....
S.S..S..S....
....S.......S
.SSS..SS.....
.........S...
.......S....S
SS.....S..S.."""


def make_board(board_data: str) -> np.array:
    return np.array([[cell for cell in row] for row in board_data.split("\n")])


def find_dragon(board: np.array) -> Tuple[int, int]:
    dragon_locs = np.argwhere(board == "D")
    assert len(dragon_locs) == 1, f"Should only be 1 dragon, found {len(dragon_locs)}"
    # for readability, turn list of lists of np.int into tuple of base-Python ints
    return tuple([int(i) for i in dragon_locs[0]])


def knight_moves(
    start_space: Tuple[int, int], board: np.array
) -> List[Tuple[int, int]]:
    """Obtain all the squares to which it is possible to make a legal 'knight move'
    (2 squares forward, one square sideways, where 'forward' can be any direction)
    on a board of this size."""
    x_max, y_max = board.shape  # i think numpy indexing is backwards? fix if needed
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


def dragon_move_range(
    this_space: Tuple[int, int], board: np.array, moves_left: int, strict: bool = False
) -> List[Tuple[int, int]]:
    """Get the set of all spaces that a dragon piece starting on this_space can
    reach in up to n moves.
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
            dragon_move_range(new_space, board, moves_left - 1)
            for new_space in knight_moves(this_space, board)
        ],
    )
    if not strict:
        # To get all options within UP TO n hops, rather than EXACTLY n hops,
        # don't forget to include starting space in result set
        return outer_hops | {this_space}
    return outer_hops


def count_sheep(spaces_to_check: List[Tuple[int, int]], board: np.array) -> int:
    sheep_count = 0
    for space in spaces_to_check:
        x, y = space  # watch the numpy indexing again
        if board[x][y] == "S":
            sheep_count += 1

    return sheep_count


def part1(data: str, moves_allowed=4) -> int:
    b = make_board(data)
    dragon_space = find_dragon(b)
    dragon_range = dragon_move_range(dragon_space, b, moves_allowed)
    sheep_in_danger = count_sheep(sorted(list(dragon_range)), b)
    return sheep_in_danger


if __name__ == "__main__":
    print(f"Part 1 answer: {part1(qten_p1)}")
    # b = make_board(test1)
    # print(b)
    # dragon_space = find_dragon(b)
    # print(f"Dragon found at {dragon_space}")
    # for i in range(4):
    #     dragon_steps = sorted(list(dragon_move_range(dragon_space, b, moves_left=i)))
    #     sheep = count_sheep(dragon_steps, b)
    #     print(f"{i} : {sheep}")
