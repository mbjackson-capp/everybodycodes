import numpy as np

np.set_printoptions(linewidth=10000)
from itertools import permutations
from math import lcm

from input_data import q7_input1, q7_input2, q7_input3, q7_track2, q7_track3


class Chariot:
    def __init__(self, name, plan, initial_power=10):
        self.name = name
        self.plan = plan
        self.power = initial_power
        self.essence = 0

    def execute_action(self, turn: int, terrain="=", v=False):
        action = self.plan[turn % len(self.plan)]
        # Action overridden by terrain
        if terrain == "+":
            self.power += 1
        elif terrain == "-":
            self.power = self.power - 1 if self.power > 0 else 0
        # Action proceeds as normal
        elif action == "+":
            self.power += 1
        elif action == "-":
            self.power = self.power - 1 if self.power > 0 else 0
        self.essence += self.power

    def __repr__(self):
        return f"Chariot(name: {self.name}, plan: {self.plan}, power: {self.power}, essence: {self.essence})"


def parse_chariots(data):
    chariots = []
    for row in data.split("\n"):
        name, plan = row.split(":")
        plan = plan.split(",")
        chariot = Chariot(name, plan)
        chariots.append(chariot)
    return chariots


def squire_race(chariots: list[Chariot], segments=10):
    for segment in range(segments):
        for c in chariots:
            c.execute_action(turn=segment)
    chariots = sorted(chariots, key=lambda c: c.essence, reverse=True)
    return "".join([c.name for c in chariots])


def parse_track(track: str) -> str:
    track = track.split("\n")
    width = len(track[0])
    track = [
        row.ljust(width) for row in track
    ]  # some rows of input don't have enough spaces
    arr = np.array([[char for char in row] for row in track])
    track_str = ""
    seen = set()
    row_cur = 0
    col_cur = 0
    while (0, 0) not in seen:
        neighbors = neighbor_locs(arr, row_cur, col_cur)
        dirs = {}
        for neighbor in neighbors:
            if neighbor == (row_cur - 1, col_cur):
                dirs["u"] = neighbor
            elif neighbor == (row_cur, col_cur + 1):
                dirs["r"] = neighbor
            elif neighbor == (row_cur + 1, col_cur):
                dirs["d"] = neighbor
            elif neighbor == (row_cur, col_cur - 1):
                dirs["l"] = neighbor
        # the proper path will always check right first, then down, then left, then up
        for char in "rdlu":
            if (
                char in dirs
                and dirs[char] not in seen
                and arr[dirs[char][0]][dirs[char][1]] != " "
            ):  # found new terrain in this direction
                row_new, col_new = dirs[char]
                break
        seen.add((row_new, col_new))
        track_str += arr[row_new][col_new]
        row_cur = row_new
        col_cur = col_new
    return track_str


def knight_race(chariots: list[Chariot], track, loops=1):
    turn = 0
    for _ in range(loops):
        for spot in track:
            for c in chariots:
                c.execute_action(turn=turn, terrain=spot)
            turn += 1
    chariots = sorted(chariots, key=lambda c: c.essence, reverse=True)
    order_of_finish = "".join([c.name for c in chariots])
    scores = [c.essence for c in chariots]
    return order_of_finish, scores


def neighbor_locs(arr, x, y, include_diag=False):
    """Returns the indices of neighbors of a location in an array."""
    neighbor_locs = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == dy == 0:
                continue
            if not include_diag and dx != 0 and dy != 0:
                continue
            else:
                this_x = x + dx
                this_y = y + dy
                if (
                    this_x >= 0
                    and this_y >= 0
                    and this_x < len(arr)
                    and this_y < len(arr[0])
                ):
                    neighbor_locs.append((this_x, this_y))
    return neighbor_locs


def part3(track):
    """Run the race repeatedly against the other knight to see how many action plans result in wins.

    There are 11! = 39916800 permutations of 11 elements, but given repetition, there are only 9240
    *unique* permutations needed. Producing them all and then keeping the unique ones (as here)
    hangs for several seconds. TODO: Is there a more efficient way?

    Speedup inspired by Reddit user u/maneatingape: If you know how many laps it takes for the ending
    of a lap and the ending of a plan to coincide, since essence can't go negative, you know that whoever
    is ahead at that point will be ahead after 2n laps, 3n laps, 4n laps... etc. And if 2024 / len(plan)
    is an integer, and thus a multiple of n, you can terminate the race early. Plan and track necessarily
    line up after 11 laps, since the plan is 11 items long and (len(track) * 11) % 11 == 0 for any length
    of track. And 2024 / 11 = 184, an integer. This trick reduces runtime from ~75 minutes to ~1 minute.
    """
    actions_to_plan = (
        ["+" for _ in range(5)] + ["-" for _ in range(3)] + ["=" for _ in range(3)]
    )
    all_action_plans = set(permutations(actions_to_plan))
    wins = 0
    # Chariot A does the same thing every time, so just run it once and compare your score to it.
    a = parse_chariots(q7_input3)[0]
    _, score_to_beat = knight_race([a], track, loops=11)
    for _, plan in enumerate(all_action_plans):
        u = Chariot(name="U", plan=plan)
        _, your_score = knight_race([u], track, loops=11)
        if your_score > score_to_beat:  # Python compares sole element for len-1 lists
            wins += 1
    return wins


if __name__ == "__main__":
    chariots1 = parse_chariots(q7_input1)
    part1 = squire_race(chariots1)
    print(f"Part 1 solution: {part1}")

    chariots2 = parse_chariots(q7_input2)
    track2 = parse_track(q7_track2)
    part2_solution, _ = knight_race(chariots2, track2, loops=10)
    print(f"Part 2 solution: {part2_solution}")

    track3 = parse_track(q7_track3)
    print("Now working on Part 3. This may take several seconds...")
    part3_solution = part3(track3)
    print(f"Part 3 solution: {part3_solution}")
