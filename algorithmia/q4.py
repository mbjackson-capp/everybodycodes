from statistics import median
from input_data import q4_input1, q4_input2, q4_input3

# Note: in input_data file, each multi-line string has been converted into a list of integers
# using: [int(i) for i in INPUT.split('\n')]


def hammer(nail_heights: list[int]) -> int:
    level = min(nail_heights)
    return sum([ht - level for ht in nail_heights])


def hammer_p3(nail_heights: list[int]) -> int:
    # The optimal height to minimize absolute value error is the height of the median nail.
    # See https://math.stackexchange.com/questions/113270/the-median-minimizes-the-sum-of-absolute-deviations-the-ell-1-norm
    nail_heights = sorted(nail_heights)
    mdn = median(nail_heights)
    m_sum = sum([abs(ht - mdn) for ht in nail_heights])
    return int(m_sum)


if __name__ == "__main__":
    print(f"Part 1 solution: {hammer(q4_input1)}")
    print(f"Part 2 solution: {hammer(q4_input2)}")
    print(f"Part 3 solution: {hammer_p3(q4_input3)}")
