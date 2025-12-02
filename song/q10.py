from input_data import qten_p1, qten_p2


from copy import deepcopy
from functools import cache, reduce
import numpy as np
from tqdm import tqdm
from typing import List, Tuple, Set


# Problem statement: https://everybody.codes/event/2025/quests/10

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


def move_all_sheep(
    sheep_locs: List[Tuple[int, int]], b: np.array
) -> Set[Tuple[int, int]]:
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
        sheep_spaces = move_all_sheep(sheep_spaces, b)
        # Check which sheep are edible after sheep have moved
        edible_check_b = get_edible_sheep_locs(
            this_turn_dragon_range, sheep_spaces, hideout_spaces
        )
        sheep_spaces = sheep_spaces - edible_check_b

        total_edible_this_turn = len(edible_check_a) + len(edible_check_b)
        total_edible_ever += total_edible_this_turn

    return total_edible_ever


"""
PART 3 BRAINSTORM NOTES
This is going to be a more complicated version of the "possible complete
tic-tac-toe games" practice problem from 121.
Think about termination conditions:
    - If *even one* sheep moves off the grid such that it escapes, it becomes
    impossible for the dragon to eat *all* the sheep and thus the game ends
    (the sheep "win")
    - Elif there are *no* sheep on the board, the dragon must have eaten them
    all and thus the game ends (the dragon "wins")
    - Else keep playing turns 
So you want a recursive function that will check if a termination (base) case
has been reached in the current game state, then if none has, generate every 
possible next move from the current game state as the next layer down of the 
"game tree"

This might be a good use of a dataclass that includes: 
    -the move sequence this far (can be a string or list)
    -who moves next (may not be necessary to preserve; can be inferred from board state)
        (might also be easier to do who moved last)
    -where all the sheep currently are (with max 1 per column and all possible
    moves being straight down, you can preserve a row number or None for each column)
    -where the dragon currently is
    -where all the hideouts are
you may also want some way of reconstructing paste game states from a sequence

You can use ord() minus a constant to interconvert from column letters to integers
None of the example or real inputs have more than 26 columns and you could just
keep going into the range of basic ASCII symbols if you wanted after that

it would really be nice to be able to cache stuff, so avoid unhashable types
as input if possible
"""


def to_alphanum(loc: Tuple[int, int]) -> str:
    """Convert a zero-based numpy-compatible (x,y) index into the alphanumeric
    syntax used in problem statement."""
    x, y = loc
    ASCII_A_VALUE = 65
    return f"{chr(ASCII_A_VALUE+y)}{x+1}"


def to_loc(alphanum: str) -> Tuple[int, int]:
    """Convert an alphanumeric representation such as L8 into a numpy-compatible
    location tuple.
    Assumes that column indicator will be a single letter, and that column
    names will continue with single-character ASCII symbols in numerical order
    as defined in the standard if there are columns past Z. (This will not
    be an issue with the sizes of input in the problem.)"""
    ASCII_A_VALUE = 65
    y = ord(alphanum[0]) - ASCII_A_VALUE
    x = int(alphanum[1:]) - 1
    return (x, y)


def test_to_alphanum():
    assert to_alphanum((0, 0)) == "A1", f"Expected 'A1', got {to_alphanum((0, 0))}"
    assert to_alphanum((4, 6)) == "G5", f"Expected 'G5', got {to_alphanum((4, 6))}"


def test_to_loc():
    assert to_loc("A1") == (0, 0), f"Expected (0,0), got {to_loc("A1")}"
    assert to_loc("G5") == (4, 6), f"Expected (4,6), got {to_loc("G5")}"


class DragonChessGame:
    def __init__(self, board_data: str):
        board = make_board(board_data)
        self.max_x, self.max_y = board.shape

        self.dragon = find_dragon(board)
        self.sheeps = find_symbol(board, SHEEP)
        self.hideouts = find_symbol(board, HIDEOUT)

        self.sequence = ""
        self.next_mover = "sheep"  # TODO: consider using an Enum
        del board

        if len(set([i[1] for i in self.sheeps])) < len([i[1] for i in self.sheeps]):
            raise ValueError(
                "Invalid board state: each column can contain at max one sheep"
            )

    @property
    def winner(self):
        if any([(s[0] >= self.max_x) for s in self.sheeps]):
            return "sheep"
        elif len(self.sheeps) == 0:
            return "dragon"
        else:
            return None

    def __repr__(self):
        return (
            f"Sequence so far: {self.sequence}\n"
            f"Board size: {self.max_x} * {self.max_y}\n"
            f"Dragon at: {to_alphanum(self.dragon)}\n"
            f"Sheep at: {[to_alphanum(s) for s in sorted(list(self.sheeps))]}\n"
            f"Hideouts at: {[to_alphanum(h) for h in sorted(list(self.hideouts))]}\n"
            f"Next to attempt move: {self.next_mover}\n"
            f"Winner: {self.winner}"
        )

    @property
    def legal_moves(self):
        if self.winner:
            return None
        elif self.next_mover == "sheep":
            next_locs = [
                (s[0] + 1, s[1]) for s in self.sheeps if (s[0] + 1, s[1]) != self.dragon
            ]
            if next_locs:
                return sorted([f"S>{to_alphanum(loc)}" for loc in next_locs])
            else:
                return ["PASS"]
        elif self.next_mover == "dragon":
            next_locs = knight_moves(self.dragon, self.max_x, self.max_y)
            return [f"D>{to_alphanum(loc)}" for loc in next_locs]

    def do_move(self, move_spec: str) -> None:
        if self.winner:
            raise Exception(f"Game over: {self.winner} won, no further moves allowed")

        if move_spec not in self.legal_moves:
            raise ValueError(
                f"Illegal move: {move_spec} not in valid set {self.legal_moves}"
            )
        if move_spec == "PASS":
            self.next_mover = "dragon"
            return None

        mover = move_spec[0]
        to_space = to_loc(move_spec[2:])

        if mover == SHEEP:
            # take out the sheep already on this column
            self.sheeps = {s for s in self.sheeps if s[1] != to_space[1]}
            # replace it with a new one, a step lower
            self.sheeps.add(to_space)
            if to_space[0] < self.max_x:
                self.sequence += f" {move_spec}"
            self.next_mover = "dragon"
        elif mover == DRAGON:
            self.dragon = to_space
            if to_space in (self.sheeps - self.hideouts):
                self.sheeps.remove(to_space)  # chomp chomp
            self.sequence += f" {move_spec}"
            self.next_mover = "sheep"

    def copy(self):
        return deepcopy(self)

    def __eq__(self, other):
        return (
            isinstance(other, DragonChessGame)
            and self.sequence == other.sequence
            and self.max_x == other.max_x
            and self.max_y == other.max_y
            and self.dragon == other.dragon
            and self.sheeps == other.sheeps
            and self.hideouts == other.hideouts
            and self.next_mover == other.next_mover
            and self.winner == other.winner
        )

    def matches(self, other):
        """Check that two games have the same current board state, irrespective
        of whether a different sequence of events generated that state on each"""
        return (
            isinstance(other, DragonChessGame)
            and self.max_x == other.max_x
            and self.max_y == other.max_y
            and self.dragon == other.dragon
            and self.sheeps == other.sheeps
            and self.hideouts == other.hideouts
            and self.next_mover == other.next_mover
            and self.winner == other.winner
        )

    def __hash__(self):
        return hash(
            (
                self.sequence,
                self.max_x,
                self.max_y,
                self.dragon,
                frozenset(self.sheeps),
                frozenset(self.hideouts),
                self.next_mover,
                self.winner,
            )
        )


test_3a = """SSS
..#
#.#
#D."""


def mock_game():
    game = DragonChessGame(test_3a)
    print(game, "\n", game.legal_moves)
    # turn cycle 1
    game.do_move("S>A2")
    print(game, "\n", game.legal_moves)

    game.do_move("D>A2")
    print(game, "\n", game.legal_moves)
    assert len(game.sheeps) == 2
    # turn cycle 2
    game.do_move("S>B2")
    print(game, "\n", game.legal_moves)

    game.do_move("D>C1")
    print(game, "\n", game.legal_moves)
    assert len(game.sheeps) == 1

    # turn cycle 3
    game.do_move("S>B3")
    print(game, "\n", game.legal_moves)

    game.do_move("D>B3")
    print(game, "\n", game.legal_moves)
    assert game.winner == "dragon"

    return game


def test_game_copy():
    game_3a = DragonChessGame(test_3a)
    game_3a_2 = game_3a.copy()
    game_3a_3 = mock_game()
    game_3a_4 = game_3a_3.copy()
    assert game_3a == game_3a_2
    assert game_3a is not game_3a_2
    assert game_3a_3 == game_3a_4
    assert game_3a_3 is not game_3a_4


"""
Okay, now that I have a working game object that can be mocked through a game,
let's figure out the recursive structure for the branching game tree that will 
play every possible game from the start.

Ultimate goal: get a list of game.sequence objects from every board the dragon
can win in the game tree descended from this one.
Then return the length of that list of sequences to user.

Input type: DragonChessGame of length 1
Output type: List[List[str]]

Start with a game
initialize empty list next_boards = []
if the game has a winner and the winner is "dragon":
    - return [game.sequence] # base case 1: single winner found
elif the board has a winner and the winner is "sheep":
    - return [] # base case 2: no winner possible
else:
    - create next_games = [game.do_move(move) for move in game.next_moves]
    - concatenate together proc(game) for game in next_games # recursive step

Unfortunately, this produces a combinatorially explosive number of possible game states
and even with @cache decorator it takes several minutes to get through an example
And even then, a macbook can run out of memory and crash midway through

May want to "prune" some branches where it's pretty clear the dragon can't get everything.
if all the sheep are on the bottom row, for example, and the dragon is above that row,
the game is over and no possible victories could happen after that. because
no matter where the dragon goes, one sheep will get out. you don't need to simulate
every possible action after that
and you can "backward induct" a variety of cases similar to that one which don't
need evaluation

You need to preserve the sequence as part of game state to get the correct answer,
but maybe some infra-equality operator could check if this board has been seen before
and/or cache no-win boards independent of the sequence used to reach them
if the sheep and dragon are in a particular configuration it shoulnd't matter if the dragon
circled around a couple of times failing to get them.
(Confirmed, u/Grand-Sale-2343: 'if we see a state that has alredy been visited 
(dragon, sheep, turn) you could cache the result and avoid to re-explore that path,
even if the sequence of moves that led to that point was different.')
^ would need to create a custom decorator or wrapper function to store that cache 
outside the recursive function body, so it can be looked up for a particular run
without bleeding over into other runs on other boards 

Reddit solutions thread: 'As soon as a sheep reaches a series of hiding spots that 
spans down to the end of the board, it is safe, and the ...branch can be pruned'

You can also just return 1 for dragon win board, 0 for sheep win board,
and do numeric addition rather than set union of big strings, that could be faster
"""


@cache
def all_dragon_win_seqs(game: DragonChessGame, depth=0) -> Set[str]:
    """
    Recursive function that serves as the heart of Part 3.

    Consider the game tree descending from this game's state, where this node
    is the root and each possible game state after one possible move
    directly following this one is a child of the root. (And so on.)

    Return a set of sequences from every descendant game state in which the
    dragon has eaten all the sheep (these will be a subset of the "leaf nodes"
    / base cases).
    """
    print("\n")
    print(game.sequence)
    print(f"\nNext moves: {game.legal_moves}")
    if game.winner == "sheep":  # Base case 1:
        print(f"SHEEP WINNER GAME BASE CASE HIT AT DEPTH {depth}. RETURN NOTHING")
        return set()
    elif game.winner == "dragon":
        print(f"DRAGON WINNER GAME BASE CASE HIT AT DEPTH {depth}. RETURN ITS SEQUENCE")
        return {game.sequence}
    elif game.winner is None:  # Recursive step
        nexts = []
        for move in game.legal_moves:
            this_next_game = game.copy()
            this_next_game.do_move(move)
            nexts.append(this_next_game)
        # get the list of lists of sequences for each game, then flatten that
        # into a single list
        # win_seqs_set = set()
        # for next in nexts:
        #     these_win_seqs = set(all_dragon_win_seqs(next, depth=depth + 1))
        #     win_seqs_set = win_seqs_set | these_win_seqs
        # return win_seqs_set
        return reduce(
            set.union, [all_dragon_win_seqs(next_game) for next_game in nexts]
        )


test_3b = """SSS
..#
..#
.##
.D#"""

if __name__ == "__main__":
    print(f"Part 1 answer: {part1(qten_p1)}")
    print(f"Part 2 answer: {part2(qten_p2, n_turns=20)}")
    test_to_alphanum()
    test_to_loc()
    game_3b = DragonChessGame(test_3b)
    test3b_result = all_dragon_win_seqs(game_3b)
    print(f"TEST 3B RESULTS:")
    print(sorted(test3b_result))
    print(len(test3b_result))
    # test 3a should have length 15 but it's giving me 14. god dammit

    # print(game_3a)
    # print(len(game_3a))
    # mock_3a = mock_game()
    # mock3a_result = all_dragon_win_seqs(mock_3a)
    # print(mock3a_result)
