from input_data import q6_p1, q6_p2, q6_p3

from collections import Counter
from tqdm import tqdm


def count_mentors(tents: str) -> int:
    total_mentors = 0
    for i, char in enumerate(tents):
        if char.isupper():
            continue
        elif char.islower():
            earliers = tents[:i]
            mentor_count = Counter(earliers)[char.upper()]
            total_mentors += mentor_count
    return total_mentors


def part1(tents: str, cat="a") -> int:
    fighters = "".join([char for char in tents if char in (cat.upper(), cat.lower())])
    return count_mentors(fighters)


def part3(tent_data: str, dist_limit: int = 10, repeats: int = 1):
    tents = tent_data * repeats
    total_mentors = 0
    print(len(tents))
    for i, char in tqdm(enumerate(tents)):
        if char.isupper():
            continue
        elif char.islower():
            LEFT_BOUND = max(0, i - dist_limit)
            RIGHT_BOUND = min(len(tents), i + dist_limit)
            eligibles = tents[LEFT_BOUND : RIGHT_BOUND + 1]
            mentor_count = Counter(eligibles)[char.upper()]
            total_mentors += mentor_count
    return total_mentors


print(f"Part 1 answer: {part1(q6_p1)}")
print(f"Part 2 answer: {count_mentors(q6_p2)}")
print(f"Part 3 answer: {part3(q6_p3, dist_limit=1000, repeats=1000)}")
