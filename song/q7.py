from input_data import q7_p1, q7_p2


from typing import Tuple, List

test1 = """Oronris,Urakris,Oroneth,Uraketh

r > a,i,o
i > p,w
n > e,r
o > n,m
k > f,r
a > k
U > r
e > t
O > r
t > h"""


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


def part1(data: str) -> str:
    names, rules = parse_grammar(data)
    names = [i[1] for i in names]
    for name in names:
        for i, char in enumerate(name):
            if i == len(name) - 1:  # you reached the last letter
                return name
            nexts = rules[char]
            if name[i + 1] not in nexts:
                break
    return None


def part2(data: str) -> str:
    indexed_names, rules = parse_grammar(data)
    valids = []
    for indexed_name in indexed_names:
        index, name = indexed_name
        for i, char in enumerate(name):
            if i == len(name) - 1:  # you reached the last letter
                valids.append(index)
                break
            nexts = rules[char]
            if name[i + 1] not in nexts:
                break
    return sum(valids)



if __name__ == "__main__":
    print(f"Part 1 answer: {part1(q7_p1)}")
    print(f"Part 2 answer: {part2(q7_p2)}")
