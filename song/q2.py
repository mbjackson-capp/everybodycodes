from dataclasses import dataclass
from math import trunc
from tqdm import tqdm

# Problem statement: https://everybody.codes/event/2025/quests/2


@dataclass
class ComplexNumber:
    """Implementation of a 'complex' number as defined in quest 2.
    Makes use of Pyton's arithmetic 'dunder' methods. See:
    https://realpython.com/python-magic-methods/#arithmetic-operators"""

    x: int = 0
    y: int = 0

    def __repr__(self):
        return f"[{self.x},{self.y}]"

    def __add__(self, other):
        return ComplexNumber(x=self.x + other.x, y=self.y + other.y)

    def __mul__(self, other):
        return ComplexNumber(
            x=(self.x * other.x) - (self.y * other.y),
            y=(self.x * other.y) + (self.y * other.x),
        )

    def __truediv__(self, other):
        return ComplexNumber(x=trunc(self.x / other.x), y=trunc(self.y / other.y))

    @property
    def is_in_bounds(self):
        LOWER_BOUND = -1_000_000
        UPPER_BOUND = 1_000_000
        return (
            self.x >= LOWER_BOUND
            and self.x <= UPPER_BOUND
            and self.y >= LOWER_BOUND
            and self.y <= UPPER_BOUND
        )


def test_regression_complex_numbers():
    # addition
    assert ComplexNumber(1, 1) + ComplexNumber(2, 2) == ComplexNumber(3, 3)
    assert ComplexNumber(2, 5) + ComplexNumber(3, 7) == ComplexNumber(5, 12)
    assert ComplexNumber(-2, 5) + ComplexNumber(10, -1) == ComplexNumber(8, 4)
    assert ComplexNumber(-1, -2) + ComplexNumber(-3, -4) == ComplexNumber(-4, -6)
    # multiplication
    assert ComplexNumber(1, 1) * ComplexNumber(2, 2) == ComplexNumber(0, 4)
    assert ComplexNumber(2, 5) * ComplexNumber(3, 7) == ComplexNumber(-29, 29)
    assert ComplexNumber(-2, 5) * ComplexNumber(10, -1) == ComplexNumber(-15, 52)
    assert ComplexNumber(-1, -2) * ComplexNumber(-3, -4) == ComplexNumber(-5, 10)
    # division
    assert ComplexNumber(10, 12) / ComplexNumber(2, 2) == ComplexNumber(5, 6)
    assert ComplexNumber(11, 12) / ComplexNumber(3, 5) == ComplexNumber(3, 2)
    assert ComplexNumber(-10, -12) / ComplexNumber(2, 2) == ComplexNumber(-5, -6)
    assert ComplexNumber(-11, -12) / ComplexNumber(3, 5) == ComplexNumber(-3, -2)


def part1(
    sample_number: ComplexNumber, divisor: int = 10, cycles: int = 3
) -> ComplexNumber:
    result = ComplexNumber(0, 0)
    for cycle in range(cycles):
        result *= result
        result /= ComplexNumber(divisor, divisor)
        result += sample_number
        if not result.is_in_bounds:
            break
    return result


def count_engraved_points(start: ComplexNumber, is_part3: bool = False) -> int:
    to_engrave = []
    PLATE_SIZE = 1000
    STEP_SIZE = 1 if is_part3 else 10
    # check all the points
    for x in tqdm(range(start.x, start.x + PLATE_SIZE + 1, STEP_SIZE)):
        for y in range(start.y, start.y + PLATE_SIZE + 1, STEP_SIZE):
            point = ComplexNumber(x, y)
            # should this point be engraved?
            result = part1(point, divisor=100_000, cycles=100)
            if result.is_in_bounds:
                to_engrave.append(point)
    return len(to_engrave)


# TODO: write a function that parses the string input
A_test = ComplexNumber(25, 9)
A_p1 = ComplexNumber(162, 60)
GRID_SIZE = ComplexNumber(1000, 1000)
A_test2 = ComplexNumber(35300, -64910)
A_p2 = ComplexNumber(-79017, -15068)


if __name__ == "__main__":
    test_regression_complex_numbers()
    print(f"Part 1 answer: {part1(A_p1)}")
    print("Now calculating part 2 answer...")
    print(f"Part 2 answer: {count_engraved_points(A_p2)}")
    print(f"Now calculating part 3 answer...this could take a few minutes...")
    print(f"Part 3 answer: {count_engraved_points(A_p2, is_part3=True)}")
