import networkx as nx
import numpy as np
from itertools import combinations
from input_data import q17_input1, q17_input2, q17_input3


STAR = "*"


def parse_star_chart(star_chart: str):
    chart = np.array([[spot for spot in row] for row in star_chart.split("\n")]).T
    star_dict = {}
    index = 1
    for x, row in enumerate(chart):
        for y, spot in enumerate(row):
            if spot == STAR:
                star_dict[index] = (int(x) + 1, int(y) + 1)
                index += 1
    return star_dict


def manhattan_dist(star1: tuple[int, int], star2: tuple[int, int]) -> int:
    return abs(star2[0] - star1[0]) + abs(star2[1] - star1[1])


BRIGHT_LIMIT = 6


def make_star_graph(star_dict: dict, is_part3: bool = False):
    G = nx.Graph()
    for k in star_dict.keys():
        G.add_node(k, spot=star_dict[k])
    for comb in combinations(star_dict.keys(), 2):
        star1, star2 = comb
        mdist = manhattan_dist(G.nodes[star1]["spot"], G.nodes[star2]["spot"])
        if (not is_part3) or (mdist < BRIGHT_LIMIT):
            G.add_edge(star1, star2, weight=mdist)
    return G


def constellation_size(T: nx.Graph) -> int:
    connection_sum = sum([e[2]["weight"] for e in T.edges(data=True)])
    size = connection_sum + len(T.nodes)
    return size


# Note: Due to numpy conventions, this adds stars in a different orientation
# (and thus, with different underlying corodinates) than problem statement,
# but Manhattan distances between each pair of stars will be the same.
def full_constellation_size(input: str) -> int:
    sd = parse_star_chart(input)
    sG = make_star_graph(sd)
    T = nx.minimum_spanning_tree(sG)
    return constellation_size(T)


def part3(input: str):
    sd = parse_star_chart(input)
    sG = make_star_graph(sd, is_part3=True)
    F = nx.minimum_spanning_tree(sG)  # will return a minimum spanning forest
    bright_constellations = sorted(
        [F.subgraph(c).copy() for c in nx.connected_components(F)],
        key=lambda c: constellation_size(c),
        reverse=True,
    )
    c0, c1, c2 = bright_constellations[:3]
    return constellation_size(c0) * constellation_size(c1) * constellation_size(c2)


part1_solution = full_constellation_size(q17_input1)
print(f"Part 1 solution: {part1_solution}")

part2_solution = full_constellation_size(q17_input2)
print(f"Part 2 solution: {part2_solution}")

print("Working on Part 3 solution. This may take a few seconds...")
part3_solution = part3(q17_input3)
print(f"Part 3 solution: {part3_solution}")
