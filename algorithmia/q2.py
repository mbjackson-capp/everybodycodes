import re
from input_data import q2_words1, q2_helmet1, q2_words2, q2_shield2

### PART 1


def count_runic_words(words: list[str], helmet: str):
    count = 0
    for ix, char in enumerate(helmet):
        possible_words = [w for w in words if w[0] == char]
        for pword in possible_words:
            try:
                if helmet[ix : ix + len(pword)] == pword:
                    count += 1
            except IndexError:
                continue
    return count


print(f"Part 1 solution: {count_runic_words(q2_words1, q2_helmet1)}")

### PART 2


def count_runic_symbols(words: list[int], line: str) -> int:
    symbol_indices = []
    sdrow = [word[::-1] for word in words]
    words = words + sdrow
    for ix, char in enumerate(line):
        possible_words = [w for w in words if w[0] == char]
        for pword in possible_words:
            try:
                if line[ix : ix + len(pword)] == pword:
                    symbol_indices = symbol_indices + list(range(ix, ix + len(pword)))
            except IndexError:
                continue
    return len(set(symbol_indices))


def count_full_shield(words: list[int], shield: list[str]) -> int:
    total = 0
    for line in shield:
        line_count = count_runic_symbols(words, line)
        total += line_count
    return total


print(f"Part 2 solution: {count_full_shield(q2_words2, q2_shield2)}")

### TODO: PART 3
