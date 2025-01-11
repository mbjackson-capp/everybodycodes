from itertools import pairwise
from math import inf
import numpy as np
import networkx as nx
import time
from input_data import q13_input1, q13_input2, q13_input3


q13_input1 = np.array([[char for char in row] for row in q13_input1.split("\n")])
q13_input2 = np.array([[char for char in row] for row in q13_input2.split("\n")])
q13_input3 = np.array([[char for char in row] for row in q13_input3.split("\n")])


def neighbor_locs(arr, x, y, include_diag=False):
    """Returns the indices of neighbors of a location in a square array.
    TODO: Put this in a utils file"""
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


IMPASSABLE = ["#", " "]


def find_S_and_E(arr):
    """Find all starting spots and the single ending spot."""
    all_Sx, all_Sy = np.where(arr == "S")
    all_S = list(zip([int(i) for i in all_Sx], [int(j) for j in all_Sy]))
    spot_E = tuple(int(i[0]) for i in np.where(arr == "E"))
    return all_S, spot_E


def level_change_time(lvl_a: int, lvl_b: int) -> int:
    """Determine how long it takes to get from one spot to another, given rules
    in problem statement (including 'portal' above level 9 that wraps around to
    level 0), i.e. calculate weight of dge between two spots of these heights."""
    dist = abs(lvl_a - lvl_b)
    return min(dist, 10 - dist) + 1


def networkify(arr: np.array) -> nx.Graph:
    """Turn an array representation of a labyrinth into a graph representation.
    Also returns the list of all possible starting points and desired endpoint
    for path to the princess."""
    start, end = find_S_and_E(arr)
    arr[arr == "S"] = "0"
    arr[end] = "0"
    G = nx.Graph()
    q = [start[0]]

    while len(q) > 0:
        cur_spot = q.pop(0)

        x, y = cur_spot
        cur_lvl = 0 if arr[x][y] in ["S", "E"] else int(arr[x][y])
        if cur_spot not in G.nodes:
            G.add_node(cur_spot, ht=cur_lvl)

        neighbors = [
            spot for spot in neighbor_locs(arr, x, y) if arr[spot] not in IMPASSABLE
        ]

        for nbr in neighbors:
            x_nbr, y_nbr = nbr
            nbr_lvl = 0 if arr[x_nbr][y_nbr] in ["S", "E"] else int(arr[x_nbr][y_nbr])
            if nbr not in G.nodes:
                G.add_node(nbr, ht=nbr_lvl)
            if (cur_spot, nbr) not in G.edges:
                change_wt = level_change_time(int(arr[cur_spot]), int(arr[nbr]))
                G.add_edge(cur_spot, nbr, weight=change_wt)
            else:
                continue
            q.append(nbr)

    return G, start, end


def run(arr):
    """Calculate the length of the shortest possible path from a point labeled S
    to the princess at point labeled E on the map of a labyrinth, testing all
    possible start points as needed and returning the minimum length found.

    For parts 1 and 2, there is only one possible starting point, so it just
    calculates the desired (i.e. shortest) path from start to finish."""
    G, starts, end = networkify(arr)
    overall_ans = inf
    for start in starts:
        result = nx.shortest_path(G, start, end, weight="weight")
        this_ans = 0
        for pair in pairwise(result):
            spot_a, spot_b = pair
            this_ans += level_change_time(int(arr[spot_a]), int(arr[spot_b]))

        if this_ans < overall_ans:
            if overall_ans != inf:
                print(
                    f"Path from {start} has length {this_ans}, less than previous record {overall_ans}"
                )
            overall_ans = this_ans
        else:
            print(f"Path from {start} not shorter than {overall_ans}")
    return overall_ans


if __name__ == "__main__":
    p1_solution = run(q13_input1)
    print(f"Part 1 solution: {p1_solution}")

    p2_solution = run(q13_input2)
    print(f"Part 2 solution: {p2_solution}")

    print(f"Now running Part 3... This may take a few minutes...")
    time.sleep(3)
    p3_solution = run(q13_input3)
    print(f"Part 3 solution: {p3_solution}")
