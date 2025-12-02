from input_data import qten_p1, qten_p2, qten_p3


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

#### PART 1 & 2 ###############################################################


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
        # include starting space in result set
        return outer_hops | {this_space}
    return outer_hops


def get_edible_sheep_locs(
    dragon_spaces: Set[Tuple[int, int]],
    sheep_spaces: Set[Tuple[int, int]],
    hideout_spaces: Set[Tuple[int, int]],
) -> Set[Tuple[int, int]]:
    return dragon_spaces.intersection(sheep_spaces) - hideout_spaces


def part1(data: str, moves_allowed=4) -> int:
    b = make_board(data)
    dragon_space = find_dragon(b)
    sheep_spaces = find_symbol(b, SHEEP)
    x_max, y_max = b.shape
    dragon_range = dragon_move_range(dragon_space, x_max, y_max, moves_allowed)
    sheep_in_danger = get_edible_sheep_locs(dragon_range, sheep_spaces, set())
    return len(sheep_in_danger)


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


#### PART 3 HELPER FUNCTIONS ##################################################


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


def is_saved(
    sheep: Tuple[int, int], hideouts: Set[Tuple[int, int]], max_x: int
) -> bool:
    """Check if all spaces from this sheep to the bottom of the board, inclusive,
    are hideouts. If this is true of any sheep, the game is over and the sheep
    have won.
    Reddit thread: 'As soon as a sheep reaches a series of hiding spots that spans
    down to the end of the board, it is safe, and the ...branch can be pruned'"""
    x, y = sheep
    return all([(sx, y) in hideouts for sx in range(x, max_x)])


#### PART 3 ###################################################################


class DragonChessGame:
    def __init__(self, board_data: str):
        board = make_board(board_data)
        self.max_x, self.max_y = board.shape

        self.dragon = find_dragon(board)
        self.sheeps = find_symbol(board, SHEEP)
        self.hideouts = find_symbol(board, HIDEOUT)

        self.sequence = ""
        self.next_mover = "sheep"
        del board

        if len(set([i[1] for i in self.sheeps])) < len([i[1] for i in self.sheeps]):
            raise ValueError(
                "Invalid board state: each column can contain at max one sheep"
            )

    @property
    def winner(self):
        # Any sheep within a sequence of hideouts running all the way to the
        # end of the board can never be eaten
        if any([is_saved(s, self.hideouts, self.max_x) for s in self.sheeps]):
            return "sheep"
        # If any sheep has escaped the board, the dragon can't eat all of them
        if any([(s[0] >= self.max_x) for s in self.sheeps]):
            return "sheep"
        elif len(self.sheeps) == 0:  # dragon's goal: eat all sheep
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
            # sheep can advance to dragon's spot only if there's a hideout there too
            next_locs = [
                (s[0] + 1, s[1])
                for s in self.sheeps
                if (s[0] + 1, s[1]) != self.dragon or (s[0] + 1, s[1]) in self.hideouts
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
            # replace sheep on this column with a new one a step lower
            self.sheeps = {s for s in self.sheeps if s[1] != to_space[1]}
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
        """Check that two games have the same current board state, irrespective
        of previous game sequence."""
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
        """Hash the current board state, ignoring previous game sequence.
        This is necessary for memoization to work properly."""
        return hash(
            (
                self.max_x,
                self.max_y,
                self.dragon,
                frozenset(self.sheeps),
                frozenset(self.hideouts),
                self.next_mover,
                self.winner,
            )
        )


def simulate_move_sequence(game: DragonChessGame, move_seq: str) -> DragonChessGame:
    """For testing purposes. Run a game through a list of moves and return
    the game after those moves are performed"""
    moves = move_seq.split(" ")
    for move in moves:
        print(f"Performing move {move}")
        game.do_move(move)
    return game


"""
Initialize a dictionary where each key is a (hashed representation of) game 
state IRRESPECTIVE of previous game sequence, and each value is the number
of descendant states from that game in which the dragon has won.

The insight here is that the descendant game trees for a given game state
do not depend on the sequence of moves it took for the game state to be reached.
(Reddit user u/Grand-Sale-2343: 'if we see a state that has alredy been visited
... you could cache the result and avoid to re-explore that path, even if the 
sequence of moves that led to that point was different.')
We also only return the count of descendant sequences, and don't preserve what 
those sequences actually are, which makes the antecedent sequence truly 
irrelevant.
This gets emptied at the start of part3() execution and preserved/modified
as a global variable by the recursive function to avoid having to pass it in
as an argument.
"""
memo = {}


def num_dragon_win_seqs(game: DragonChessGame) -> int:
    """
    Consider the 'game tree' descending from this game's state, where this node
    is the root and each child of the root is a possible game state from one
    legal move played on this game. (And so on.)

    Return the number of descendant game states in which the dragon has eaten all
    the sheep (these will be a subset of the "leaf nodes" / base cases).

    Recursive function checks if the current game state has terminated.
    If it hasn't, generate every possible next move from the current game state as the
    next layer down of the  "game tree" and run again on each board created by
    doing one of those moves.
    """
    # Memoization: if descendant game tree will be the same as a descendant
    # game tree already seen, just retrieve the number of dragon wins we
    # saw when evaluating this game previously.
    global memo
    if game in memo:
        return memo[game]

    if game.winner == "sheep":  # Base case 1
        return 0
    elif game.winner == "dragon":  # Base case 2
        return 1
    elif game.winner is None:  # Recursive step
        nexts = []
        for move in game.legal_moves:
            this_next_game = game.copy()
            this_next_game.do_move(move)
            nexts.append(this_next_game)
        result = sum([num_dragon_win_seqs(next_game) for next_game in nexts])
        if game not in memo:
            memo[game] = result
        return result


def part3(data: str) -> int:
    global memo
    memo = {}  # wipe the memoization
    start_game = DragonChessGame(data)
    return num_dragon_win_seqs(start_game)


if __name__ == "__main__":
    print(f"Part 1 answer: {part1(qten_p1)}")
    print(f"Part 2 answer: {part2(qten_p2, n_turns=20)}")
    print("Now calculating Part 3 answer... This could take ~30-60 seconds...")
    print(f"Part 3 answer: {part3(qten_p3)}")
