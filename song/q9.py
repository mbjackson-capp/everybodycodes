from input_data import q9_p1, q9_p2, q9_p3
from typing import Tuple, Optional
from itertools import combinations
import networkx as nx
from tqdm import tqdm


def parse_dnas(dna_data: str) -> dict:
    lines = dna_data.split("\n")
    dna = {}
    for line in lines:
        sn, seq = line.split(":")
        dna[int(sn)] = seq
    return dna


def find_parents(dnas: dict, child_sn: int) -> Optional[Tuple[int, int]]:
    """Assuming that a dragon with scale number child_sn is a child with two parents,
    find the id numbers of those two parents. Return None if two valid parents
    cannot be found."""
    possible_parent_pairs = list(
        combinations([k for k in dnas.keys() if k != child_sn], 2)
    )
    for pair in possible_parent_pairs:
        for i, char in enumerate(dnas[child_sn]):
            inheritables = {dnas[parent][i] for parent in pair}
            if char not in inheritables:
                break
            if i == len(dnas[child_sn]) - 1 and char in inheritables:
                return pair
    return None


def match_score(dna1: str, dna2: str) -> int:
    score = 0
    for i, char in enumerate(dna1):
        if char == dna2[i]:
            score += 1
    return score


def solve(data: str) -> Tuple[int, int]:
    """Find the parents of any child dragon with parents, then obtain
     the degree of similarity for each of those children (Part 1 and Part 2).

    In tandem, assemble a 'family forest' of nodes (where each dragon has a node
    labeled with its scale number and parent-child dyads are connected by an edge
    (Part 3).

    Returns:
        - the sum of all degrees of similarity (int)
        - the sum of all scale numbers for the family tree with the
        most dragons in it (int)
    """
    dnas = parse_dnas(data)
    children = {}
    G = nx.Graph()
    for sn in dnas.keys():
        G.add_node(sn)

    for sn in tqdm(dnas.keys()):
        if find_parents(dnas, sn) is None:
            continue
        parent_a, parent_b = find_parents(dnas, sn)
        G.add_edge(sn, parent_a)
        G.add_edge(sn, parent_b)
        child_dna = dnas[sn]
        children[sn] = {
            "parents": (parent_a, parent_b),
            "deg_similarity": match_score(child_dna, dnas[parent_a])
            * match_score(child_dna, dnas[parent_b]),
        }
    ans_1_2 = sum([c["deg_similarity"] for c in children.values()])

    max_family_size = 0
    max_family_scale_sum = 0
    family_forest = nx.connected_components(G)
    for family_tree in family_forest:
        family_size = len(family_tree)
        scale_sum = sum([dragon for dragon in family_tree])
        if family_size > max_family_size:
            max_family_size = family_size
            max_family_scale_sum = scale_sum

    return ans_1_2, max_family_scale_sum


if __name__ == "__main__":
    p1_ans, _ = solve(q9_p1)
    print(f"Part 1 answer: {p1_ans}")
    p2_ans, _ = solve(q9_p2)
    print(f"Part 2 answer: {p2_ans}")
    _, p3_ans = solve(q9_p3)
    print(f"Part 3 answer: {p3_ans}")
