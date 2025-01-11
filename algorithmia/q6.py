from collections import Counter
import networkx as nx
import re

from input_data import q6_input1, q6_input2, q6_input3


def parse_input(data: str) -> nx.DiGraph:
    """Create a graph representation of a tree."""
    G = nx.DiGraph()
    data = data.split("\n")
    fruit_id = 0
    for line in data:
        source, targets = line.split(":")
        targets = targets.split(",")
        # Instructions are somewhat unclear: You should entirely ignore any
        # line whose source *or* targets have BUG or ANT *anywhere* in them.
        if source in ("BUG", "ANT") or "BUG" in targets or "ANT" in targets:
            continue
        if source not in G.nodes:
            G.add_node(source)
        for target in targets:
            if target == "@":
                # Give each fruit a dummy suffix to disambiguate new nodes
                target += str(fruit_id)
                fruit_id += 1
            G.add_edge(source, target)
    return G


def most_powerful_fruit_path(G: nx.DiGraph, part=1) -> str:
    """Find the path to the most powerful fruit, i.e. the string representation
    of the path whose length, from node RR to a leaf marked @, is unique."""
    all_sps = nx.single_source_all_shortest_paths(G, source="RR")
    result = []
    for item in all_sps:
        _, path = item
        path = path[0]
        if part != 1:
            # preserve only first letter of each node
            path = [id[0] for id in path]
        path = "".join([char for char in path if char.isalpha() or "@" in char])
        if "@" in path:
            result.append(path)
    path_lens = {path: len(path) for path in result}
    len_ctr = Counter(path_lens.values())
    most_powerful_len = [k for k, v in len_ctr.items() if v == 1][0]
    ans = [k for k, v in path_lens.items() if v == most_powerful_len][0]
    # remove fruit id tags if any still present
    ans = re.sub(r"\d", "", ans)
    return ans


if __name__ == "__main__":
    G1 = parse_input(q6_input1)
    part1_solution = most_powerful_fruit_path(G1)
    print(f"Part 1 solution: {part1_solution}")
    G2 = parse_input(q6_input2)
    part2_solution = most_powerful_fruit_path(G2, part=2)
    print(f"Part 2 solution: {part2_solution}")
    G3 = parse_input(q6_input3)
    part3_solution = most_powerful_fruit_path(G3, part=3)
    print(f"Part 3 solution: {part3_solution}")
