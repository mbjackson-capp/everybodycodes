from typing import List
from copy import deepcopy
import time

# Problem statement: https://everybody.codes/event/2025/quests/11

test1 = """9
1
1
4
9
6"""

q11_p1 = """2
1
3
17
18
7"""


def flockify(str) -> List[int]:
    return [int(i) for i in str.split("\n")]


def run_round(flock: List[int], phase: int = 1) -> List[int]:
    flock = deepcopy(flock)  # to prevent list reference shenanigans
    for i in range(1, len(flock)):
        this_col = flock[i - 1]
        next_col = flock[i]
        if phase == 1 and (next_col < this_col) and (this_col > 0):
            flock[i - 1] -= 1
            flock[i] += 1
        elif phase == 2 and (next_col > this_col) and (next_col > 0):
            flock[i] -= 1
            flock[i - 1] += 1
    return flock


def checksum(flock: List[int]) -> int:
    checksum = 0
    for ix, col_count in enumerate(flock):
        checksum += (ix + 1) * col_count
    return checksum


def run_simulation(flock: List[int], debug=False) -> dict:
    round = 0
    checksums = {0: checksum(flock)}

    def printv(x):
        if debug:
            print(x)

    while True:
        new_flock = run_round(flock, phase=1)
        if new_flock == flock:
            break
        else:
            round += 1
            flock = new_flock
            checksums[round] = checksum(flock)
            printv(f"After round {round}: {flock}, checksum: {checksums[round]}")
    printv("No more moves possible in phase 1! Going to phase 2...")
    while True:
        new_flock = run_round(flock, phase=2)
        if new_flock == flock:
            break
        else:
            round += 1
            flock = new_flock
            checksums[round] = checksum(flock)
            printv(f"After round {round}: {flock}, checksum: {checksums[round]}")
    printv(f"No more moves possible! Simulation over")
    return checksums


test2 = flockify(
    """805
706
179
48
158
150
232
885
598
524
423"""
)

q11_p2 = flockify(
    """720918
771199
836592
163412
212382
619736
914190
418025
201425
9447
444750
937834
129729
105428
92173
7839
382701
3860
817110
644156
689130
852948
957788
973254
743040
732818
935123
925401
1487
491786
7679
286091
2624
8566
383402
281570
833453
431528
417026
528275
939883
87139
3256
835637
2635
688394
720081
323936
573956
983574
713526
730946
605894
486300
380178
3641
868500
634416
65400
946733"""
)

test1 = flockify(test1)
q11_p1 = flockify(q11_p1)
# post_r1 = run_round(test1)
# print(test1)
# print(post_r1)
# print(checksum([9, 1, 1, 4, 9, 6]))
# print(checksum([8, 1, 2, 4, 8, 7]))

if __name__ == "__main__":
    sim1 = run_simulation(q11_p1)
    print(f"Part 1 answer: {sim1[10]}")
    # simtest2 = run_simulation(test2, debug=True)
    sim2 = run_simulation(q11_p2, debug=True)
