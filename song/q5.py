from input_data import q5_p1, q5_p2, q5_p3

from dataclasses import dataclass


# Problem statement: https://everybody.codes/event/2025/quests/5


@dataclass
class FishboneSegment:
    spine: int
    left: int | None = None
    right: int | None = None

    def __repr__(self):
        repr = ""
        if self.left is not None:
            repr += f"{self.left}-"
        repr += f"{self.spine}"
        if self.right is not None:
            repr += f"-{self.right}"
        return repr

    @property
    def is_valid(self):
        if self.left is not None and self.right is not None:
            return self.left < self.spine < self.right
        elif self.left is not None:
            return self.left < self.spine
        elif self.right is not None:
            return self.spine < self.right
        else:
            return True

    @property
    def level_number(self):
        level_strs = [
            "" if s is None else str(s) for s in (self.left, self.spine, self.right)
        ]
        return int("".join(level_strs))

    def place(self, num: int):
        if num < self.spine and self.left is None:
            self.left = num
        elif num > self.spine and self.right is None:
            self.right = num
        else:
            raise ValueError(f"Could not place number {num} on spine {self}")


class Sword:
    """
    id: int
    fishbone: List[FishboneSegment]
    """

    def __init__(self, sword_str):
        id, num_lst = sword_str.split(":")

        self.id = int(id)
        self.fishbone = []

        num_list = [int(i) for i in num_lst.split(",")]
        while len(num_list) > 0:
            num = num_list.pop(0)
            for seg in self.fishbone:
                try:
                    seg.place(num)
                    num = None
                    break
                except ValueError:
                    continue
            if num:
                new_seg = FishboneSegment(num)
                self.fishbone.append(new_seg)

    def __repr__(self):
        # TODO: pad left and right spacing to match width of numbers
        return "\n |  \n".join([str(i) for i in self.fishbone])

    @property
    def quality(self):
        seg_quality = "".join([str(seg.spine) for seg in self.fishbone])
        return int(seg_quality)

    @property
    def levels(self):
        return [seg.level_number for seg in self.fishbone]

    def __lt__(self, other):
        """Determine whether this Sword is 'worse' than another.
        Used to define sort order for sorted() for part 3.
        See: https://docs.python.org/3/howto/sorting.html#odds-and-ends"""
        # First: compare quality
        if self.quality < other.quality:
            return True
        elif self.quality > other.quality:
            return False
        else:
            # Next: Compare the level numbers at level i in both swords until one differs
            i = 0
            while True:
                try:
                    if self.levels[i] < other.levels[i]:
                        return True
                    elif self.levels[i] > other.levels[i]:
                        return False
                    else:
                        i += 1
                        continue
                except IndexError:
                    # Edge case: both swords are equal up to level i, but one has more levels
                    # Will this ever happen?
                    break
            if len(self.levels) < len(other.levels):
                return True
            else:
                # Edge case: if swords are otherwise equal, a higher id is better
                return self.id < other.id


def part2(swords_data: str) -> int:
    qual_dict = {}
    sword_strs = swords_data.split("\n")
    for sword_str in sword_strs:
        new_sword = Sword(sword_str)
        qual_dict[new_sword.id] = new_sword.quality
    return max(qual_dict.values()) - min(qual_dict.values())


def part3(swords_data: str, debug=False) -> int:
    sword_strs = swords_data.split("\n")
    swords = [Sword(sword_str) for sword_str in sword_strs]
    # Use Sword.__lt__() dunder method as key for sorting.
    # sort order must be made DEscending to get best-to-worst quality order
    swords = sorted(swords, reverse=True)
    checksum = 0
    for i, sword in enumerate(swords):
        check_value = sword.id * (i + 1)  # problem specifies 1-based indexing
        if debug:
            print(f"{i+1} * {sword.id} + ")
        checksum += check_value
    return checksum


if __name__ == "__main__":
    swd1 = Sword(q5_p1)
    print(f"Part 1 answer: {swd1.quality}")
    print(f"Part 2 answer: {part2(q5_p2)}")
    print(f"Part 3 answer: {part3(q5_p3)}")
