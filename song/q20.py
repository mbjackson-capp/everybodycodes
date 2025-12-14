from copy import deepcopy
import networkx as nx
from input_data import q20_p1, q20_p2, q20_p3
from typing import List, Tuple


# Problem statement: https://everybody.codes/event/2025/quests/20

TRAMPOLINES = ["T", "S", "E"]
START = "S"
END = "E"
VOID = "#"
OFFGRID = "."

# hacky Enum-esque setup
DOWN = 0
UP = 1
LEFT = 0


def parse_input(data: str) -> nx.Graph:
    """Model a triangular tile space using a network Graph, where each trampoline
    is represented as a node, and any place where two triangles' surfaces adjoin
    is represented as an edge between two of those nodes."""
    data = [[char for char in row] for row in data.split("\n")]
    G = nx.Graph()
    for i, row in enumerate(data):
        dir = DOWN if i % 2 == 0 else UP
        for j, char in enumerate(row):
            if char in TRAMPOLINES:
                G.add_node((i, j), row=i, col=j, dir=dir, type=char)
                # all triangles adjoin ones to their left and right, if any
                if (i, j - 1) in G.nodes:
                    G.add_edge((i, j - 1), (i, j))
                # down-pointing triangle adjoins triangle directly above it, if any
                if (
                    (i - 1, j) in G.nodes
                    and dir == DOWN
                    and G.nodes[(i - 1, j)]["dir"] == UP
                ):
                    G.add_edge((i - 1, j), (i, j))
            dir = (dir + 1) % 2
    return G


def part1(data: str):
    G = parse_input(data)
    return len(G.edges)


def part2(data: str):
    G = parse_input(data)
    start = [n for n, n_data in G.nodes(data=True) if n_data["type"] == START][0]
    end = [n for n, n_data in G.nodes(data=True) if n_data["type"] == END][0]
    return len(nx.shortest_path(G, start, end)) - 1


def rotated(floor_str: str) -> str:
    """Take a string representation of floor configuration and return a version
    of it rotated 120 degrees clockwise."""
    floor_old = [[char for char in row] for row in floor_str.split("\n")]
    n_rows = len(floor_old)
    row_width = len(floor_old[0])
    floor_new = [[OFFGRID for _ in range(row_width)] for _ in range(n_rows)]

    bottom_tip = (n_rows - 1, row_width // 2)
    tip_x, tip_y = bottom_tip
    for r in range(n_rows):
        to_fill_in = row_width - (2 * r)
        old_index_to_start = (tip_x - r, tip_y + r)
        old_value_indices = rotated_helper(old_index_to_start, to_fill_in)
        for ix, c in enumerate(range(r, r + to_fill_in)):
            old_x, old_y = old_value_indices[ix]
            # put value at old index into latest index along new row
            floor_new[r][c] = floor_old[old_x][old_y]
    new_floorstr = "\n".join(["".join(row) for row in floor_new])
    return new_floorstr


def rotated_helper(
    old_start: Tuple[int, int], num_points_to_get: int
) -> List[Tuple[int, int]]:
    """Helper function to get the list of points to update in the new triangle,
    given a starting cell of the old triangle and the number of points in the new row.
    Those points in the old array head in step-stair pattern up and to the left.

    For example, if the original diagram is 11-by-11, to populate the new
    rotated diagram, you need to look at these indices in the original:
    New row 0 (start index 0): [(5,5), (4,5), (4,4), (4,3), (3,3), (3,2), (2,2),
                                (2,1), (1,1), (1,0), (0,0)]
    New row 1 (start index 1): [(6,4), (6,3), (5,3), (5,2), (4,2), (4,1), (3,1),
                                (3,0), (2,0)]
    New row 2 (start index 2): [(7,3), (7,2), (6,2), (6,1), (5,1), (5,0), (4,0)]
    New row 3 (start index 3): [(8,2), (8,1), (7,1), (7,0), (6,0)]
    New row 4 (start index 4): [(9,1), (9,0), (8,0)]
    New row 5 (start index 5): [(10,0)]
    """
    dir = LEFT
    new_row = [old_start]
    cur_x, cur_y = old_start
    for _ in range(1, num_points_to_get):
        if dir == UP:
            cur_y -= 1
            dir = LEFT
        elif dir == LEFT:
            cur_x -= 1
            dir = UP
        new_row.append((cur_x, cur_y))
    return new_row


def parse_rotating_input(data0: str) -> nx.DiGraph:
    """Start with a string representation of floor configuration, then create
    a 'three-layered' graph in which every Trampoline has a directed edge to
    every potential landing spot in the layer representing the next time period.

    Workhorse method for part 3, which reduces the solution to a simple
    shortest-path algorithm on the graph returned."""
    layer0 = data0
    layer0 = [[char for char in row] for row in layer0.split("\n")]

    layer1 = rotated(deepcopy(data0))
    layer1 = [[char for char in row] for row in layer1.split("\n")]

    layer2 = rotated(rotated(deepcopy(data0)))
    layer2 = [[char for char in row] for row in layer2.split("\n")]

    G = nx.DiGraph()
    datas = [layer0, layer1, layer2]
    # create all the valid trampoline spots as nodes first
    for k, data in enumerate(datas):
        for i, row in enumerate(data):
            for j, char in enumerate(row):
                # Abuse Python type laziness and magic number aliases to set
                # the orientation of the triangle.
                # On even-index rows, the leftmost triangle should point DOWN (=0);
                # on odd-index rows, the leftmost triangle should point UP(=1).
                # Successive triangles within a row strictly alternate orientation.
                dir = ((i % 2 == 1) + j) % 2
                if char in TRAMPOLINES:  # treat everything else as void
                    G.add_node((i, j, k), row=i, col=j, layer=k, dir=dir, type=char)
    # Iterate through all nodes and create directed edges representing valid jumps.
    # TODO: make nested if-statements less hideous
    i_values = sorted(list(set([n_data["row"] for n, n_data in G.nodes(data=True)])))
    j_values = sorted(list(set([n_data["col"] for n, n_data in G.nodes(data=True)])))
    k_values = sorted(list(set([n_data["layer"] for n, n_data in G.nodes(data=True)])))
    for i in i_values:
        for j in j_values:
            for k in k_values:
                # all edges go from layer 0 to 1, or layer 1 to 2, or layer 2 to 0
                k_next = (k + 1) % len(k_values)
                index = (i, j, k)
                if index in G.nodes:
                    # because graph is now directed, welook left and right
                    if (i, j - 1, k_next) in G.nodes:
                        G.add_edge(index, (i, j - 1, k_next))
                    if (i, j + 1, k_next) in G.nodes:
                        G.add_edge(index, (i, j + 1, k_next))
                    # and we look up and down
                    if G.nodes[index]["dir"] == DOWN and (i - 1, j, k_next) in G.nodes:
                        G.add_edge(index, (i - 1, j, k_next))
                    elif G.nodes[index]["dir"] == UP and (i + 1, j, k_next) in G.nodes:
                        G.add_edge(index, (i + 1, j, k_next))
                    # and we can hop in place as the floor rotates under us!
                    if (i, j, k_next) in G.nodes:
                        G.add_edge(index, (i, j, k_next))
    return G


def part3(data: str) -> int:
    G = parse_rotating_input(data)
    start = [
        n
        for n, n_data in G.nodes(data=True)
        if n_data["type"] == START and n_data["layer"] == 0
    ][0]
    ends = [n for n, n_data in G.nodes(data=True) if n_data["type"] == END]
    short_paths = []
    for end in ends:
        if nx.has_path(G, start, end):
            short_paths.append(nx.shortest_path_length(G, start, end))
    return min(short_paths)


if __name__ == "__main__":
    print(f"Part 1 answer: {part1(q20_p1)}")
    print(f"Part 2 answer: {part2(q20_p2)}")
    print(f"Part 3 answer: {part3(q20_p3)}")
