from input_data import q7_p1, q7_p2, q7_p3

from functools import reduce
from typing import Tuple, List, Set

# Problem statement: https://everybody.codes/event/2025/quests/7


def parse_grammar(data: str) -> Tuple[List[str], dict]:
    names, rules = data.split("\n\n")
    names = names.split(",")
    names = [(i + 1, name) for i, name in enumerate(names)]
    rule_lst = rules.split("\n")
    rules = {}
    for rule in rule_lst:
        letter, next_options = rule.split(" > ")
        next_options = set(next_options.split(","))
        rules[letter] = next_options
    return names, rules


def can_be_created(name: str, rules: dict) -> bool:
    """Determine whether this name can be created using this set of rules."""
    if name[0] not in rules.keys():
        return False
    for i, char in enumerate(name):
        if i == len(name) - 1:  # you reached the last letter
            return True
        else:
            nexts = rules[char]
            if name[i + 1] not in nexts:
                return False


def part1(data: str) -> str:
    names, rules = parse_grammar(data)
    names = [i[1] for i in names]
    for name in names:
        if can_be_created(name, rules):
            return name
    return None


def part2(data: str) -> str:
    indexed_names, rules = parse_grammar(data)
    index_sum = 0
    for indexed_name in indexed_names:
        index, name = indexed_name
        if can_be_created(name, rules):
            index_sum += index
    return index_sum


def part3(data: str) -> int:
    indexed_names, rules = parse_grammar(data)
    names = [i[1] for i in indexed_names]
    all_creatable_names = set()
    for name in names:
        new_creatables = part3_helper(name, rules)
        all_creatable_names = all_creatable_names | new_creatables
    return len(all_creatable_names)


def part3_helper(
    name: str, rules: dict, lower_bound: int = 7, upper_bound: int = 11
) -> Set[str]:
    # Base case: this name is not valid
    if not can_be_created(name, rules):
        return set()
    # Base case: this name is too long
    if len(name) > upper_bound:
        return set()
    # Base case: no more valid names can be created after this one
    if name[-1] not in rules:
        return {name}
    else:
        # Recursive step: call this function again on each name you *can* create
        # by adding exactly one valid character to this name. Union the results
        # together to get all possible names of valid lengths longer than input
        nexts = rules[name[-1]]
        options = [name + char for char in nexts]
        result = reduce(set.union, [part3_helper(option, rules) for option in options])
        # Preserve input as a valid name option only if it's long enough
        if len(name) >= lower_bound:
            result.add(name)
        return result


if __name__ == "__main__":
    print(f"Part 1 answer: {part1(q7_p1)}")
    print(f"Part 2 answer: {part2(q7_p2)}")
    print(
        f"Now doing part 3...This will take a few seconds because it doesn't cache..."
    )
    print(f"Part 3 answer: {part3(q7_p3)}")
