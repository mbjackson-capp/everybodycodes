import networkx as nx
from input_data import q20_p1, q20_p2

# Problem statement: https://everybody.codes/event/2025/quests/20

VOID = "#"
TRAMPOLINES = ["T", "S", "E"]
START = "S"
END = "E"
OFFGRID = "."

# hacky Enum-esque setup
DOWN = 0
UP = 1


# Big idea: Model a triangular tile space using a network Graph, where each
# triangle is represented a node, and any place where two triangles' surfaces
# adjoin modeled as an edge between two of those nodes.


def parse_input(data: str, tramp_edges_only: bool = False) -> nx.Graph:
    data = [[char for char in row] for row in data.split("\n")]
    G = nx.Graph()
    for i, row in enumerate(data):
        dir = DOWN if i % 2 == 0 else UP
        for j, char in enumerate(row):
            if char != OFFGRID:
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
    for e in G.edges:
        u, v = e
        if G.nodes[u]["type"] in TRAMPOLINES and G.nodes[v]["type"] in TRAMPOLINES:
            nx.set_edge_attributes(G, {e: {"T-to-T": True}})
        elif tramp_edges_only:
            G.remove_edge(u, v)
        else:
            nx.set_edge_attributes(G, {e: {"T-to-T": False}})
    return G


def part1(data: str):
    G = parse_input(data)
    return len([e for e in G.edges if G.edges[e]["T-to-T"]])


def part2(data: str):
    G = parse_input(data, tramp_edges_only=True)
    start = [n for n, n_data in G.nodes(data=True) if n_data["type"] == START][0]
    end = [n for n, n_data in G.nodes(data=True) if n_data["type"] == END][0]
    print(start)
    print(end)
    return len(nx.shortest_path(G, start, end)) - 1


test2 = """TTTTTTTTTTTTTTTTT
.TTTT#T#T#TTTTTT.
..TT#TTTETT#TTT..
...TT#T#TTT#TT...
....TTT#T#TTT....
.....TTTTTT#.....
......TT#TT......
.......#TT.......
........S........"""

"""For Part 3, how on earth do I rotate the entire graph between every hop?
I could change the type attribute of each node every period...but then
how would I recalculate the shortest path after ever step? I don't have any
guarantee that the greedy approach is correct

Oh, I have an idea
Instead of rotating the graph, instantiate a new (directed?) graph that has three 
subgraphs "layered on top" of each other. You can add a third dimension to the
node names, call the initial position (i,j,0), the position every second period 
as (i,j,1), and the position every third period (i,j,2). Then recreate new edges: 
if a jump would be valid between periods 0 and 1, say, make an edge from the position
in layer 0 to the position in layer 1. (Edges from 2 go back to 0). 
Pivotally, no edges will exist *aside* from those connecting one layer to the
temporally next layer.
This allows us to run a standard shortest path algorithm
"""


def rotated(floor_str: str) -> str:
    """Take a string representation of floor configuration and return a version
    of it rotated 120 degrees clockwise."""
    # gonna need some crazy indexing lol
    pass


def parse_for_part3(data: str) -> nx.DiGraph:
    """Start with a string representation of floor configuration, then create
    a 'three-layered' graph in which every Trampoline has a directed edge to
    every potential landing spot in the layer representing the next time period."""
    # TODO: figure out whether this strictly has to be directed. I think yes,
    # because otherwise the shortest path could go backwards across layers
    # in a way that violates time's arrow
    # TODO: create deepcopies in both rotated states
    G_prime = nx.DiGraph()
    # TODO: turn each of those into a set of nodes representing its triangles
    # (NOTE: the S in layers 1 and 2 cannot be treated as an actual start!
    # Consider converting those to 'T's)
    # TODO: figure out logic for creating directed edges between layers
    return G_prime


def part3(data: str) -> int:
    G_prime = parse_for_part3(data)
    # TODO: try to get shortest paths to *all three* END nodes.
    # return the minimum length of any of those that exist
    return 0


if __name__ == "__main__":
    print(f"Part 1 answer: {part1(q20_p1)}")
    print(f"Part 2 answer: {part2(q20_p2)}")
