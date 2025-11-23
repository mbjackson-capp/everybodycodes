from input_data import q6_p1, q6_p2, q6_p3

from collections import Counter
from functools import cache
from tqdm import tqdm


@cache
def mentor_helper(subsection: str, mentee: str) -> int:
    """Count how many eligible mentors (matching upper-case letters) exist
    for the mentee (lower case letter) within this subsection of the input.
    Uses cache decorator for memoization to reduce runtime of part 3 from
    ~5 minutes to ~5 seconds."""
    assert (
        len(mentee) == 1 and mentee.islower()
    ), "Mentee should be a lower-case letter!"
    return Counter(subsection)[mentee.upper()]


def earlier_mentors(tents: str, mentee_category: str | None = None) -> int:
    if mentee_category:
        tents = "".join(
            [
                char
                for char in tents
                if char in (mentee_category.upper(), mentee_category.lower())
            ]
        )
    total_mentors = 0
    for i, char in enumerate(tents):
        if char.isupper():
            continue
        elif char.islower():
            earliers = tents[:i]
            total_mentors += mentor_helper(earliers, char)
    return total_mentors


def surrounding_mentors(tent_data: str, dist_limit: int = 10, repeats: int = 1):
    tents = tent_data * repeats
    total_mentors = 0
    print(
        f"Calculating mentor count for {len(tents)} tents..."
        "This could take a few seconds..."
    )
    for i, char in tqdm(enumerate(tents)):
        if char.isupper():
            continue
        elif char.islower():
            LEFT_BOUND = max(0, i - dist_limit)
            RIGHT_BOUND = min(len(tents), i + dist_limit)
            eligibles = tents[LEFT_BOUND : RIGHT_BOUND + 1]
            total_mentors += mentor_helper(eligibles, char)
    return total_mentors


if __name__ == "__main__":
    print(f"Part 1 answer: {earlier_mentors(q6_p1, mentee_category='a')}")
    print(f"Part 2 answer: {earlier_mentors(q6_p2)}")
    print(f"Part 3 answer: {surrounding_mentors(q6_p3, dist_limit=1000, repeats=1000)}")
