import numpy as np
from input_data import q5_input1, q5_input2, q5_input3


def process_input(arr):
    arr = [[int(i) for i in row.split(" ")] for row in arr.split("\n")]
    return np.array(arr).T.tolist()


def pprint(arr, v=False):
    """Print an array of clap dancers so that the rows, from bottom to top, are in the same
    arrangement as the columns in example input.
    TODO: Print a list of lists so that it looks like columns in the example rather than rows
    """
    if v:
        for row in arr[::-1]:
            print(row)


def printv(obj, v=False):
    if v:
        print(obj)


def clap_dance(arr, num_rounds=10, print_every_nth=1, v=False, save_state=False):
    """Simulate the clap dance."""
    shout_counter = {}
    max_shout = 0
    NUM_COLS = len(arr)
    states = set()
    # print("Round  Number  Shouts")
    rd = 0
    while True:
        state = "".join("".join([str(i) for i in arr]))
        if state in states:  # Part 3 end condition (first cycle detected!)
            # print(f"First cycle detected! Biggest shout: {max_shout}")
            return max_shout
        states.add(state)
        rd += 1
        cur_col = (rd - 1) % NUM_COLS
        cur_clapper = arr[cur_col].pop(0)
        on_left_side = True
        going_down = True
        printv(f"ROUND {rd}", v)
        printv(f"Current clapper from head of column {cur_col+1}: {cur_clapper}", v)
        target_col = (cur_col + 1) % NUM_COLS
        # printv(f"Target column is {target_col}", v)
        side_spot = -1
        # printv(f"Going {'left' if on_left_side else 'right'} of column {target_col+1}", v)
        # TODO: replace this entire for loop by skipping straight to clapper's closed-form final location
        for clap in range(1, cur_clapper + 1):
            printv(f"The dancers shout: '{clap}!'", v)
            if (
                side_spot == len(arr[target_col]) - 1 and going_down
            ):  # reached end of column
                # printv(f"Reached back of column {target_col+1} -- flipping to right side and going up", v)
                on_left_side = False
                going_down = False
            elif side_spot == 0 and not going_down:
                # Instructions are ambiguous but here's what happens:
                # clapper continues around SAME column down the left side if they reach the top,
                # repeating going down and flipping and going up and flipping until they have moved
                # as many steps as their number
                # printv(f"Reached front of column {target_col+1} -- flipping to left side and going back down", v)
                on_left_side = True
                going_down = True
            elif going_down:
                side_spot += 1
            else:
                side_spot -= 1
            printv(
                f"Clapper is {'left' if on_left_side else 'right'} of value {arr[target_col][side_spot]} at index {side_spot} in column {target_col+1}",
                v,
            )
            if clap == cur_clapper:
                break
        # printv("It's absorption time!", v)
        # printv(f"Clapper is on {'left' if on_left_side else 'right'} side so they absorb {'in front' if on_left_side else 'behind'} person at index {side_spot}", v)
        if on_left_side:
            arr[target_col].insert(side_spot, cur_clapper)
        else:
            arr[target_col].insert(side_spot + 1, cur_clapper)
        pprint(arr, v)
        shout = combine_shout(arr)
        if shout not in shout_counter:
            shout_counter[shout] = 0
        shout_counter[shout] += 1
        if shout > max_shout:
            max_shout = shout
        if print_every_nth is not None and rd % print_every_nth == 0:
            print(f"{rd} {shout} {shout_counter[shout]}")
        printv("\n", v)
        if shout_counter[shout] == 2024:  # Part 2 end condition
            break
        if rd >= num_rounds:
            break

    return rd, combine_shout(arr)


def combine_shout(arr: list[list[int]]):
    return int("".join([str(i[0]) for i in arr]))


if __name__ == "__main__":
    input1 = process_input(q5_input1)
    input2 = process_input(q5_input2)
    input3 = process_input(q5_input3)
    VERY_LARGE_NUM = 100000000000

    _, last_shout = clap_dance(input1, num_rounds=10, print_every_nth=None, v=False)
    print(f"Part 1 solution: {last_shout}")

    print("Now working on Part 2. This could take several minutes...")
    rd, last_shout = clap_dance(
        input2, num_rounds=VERY_LARGE_NUM, print_every_nth=None, v=False
    )
    print(f"Part 2 solution: {rd * last_shout}")

    print("Now working on Part 3. This could take several minutes...")
    biggest_shout = clap_dance(
        input3, num_rounds=VERY_LARGE_NUM, print_every_nth=None, save_state=True
    )
    print(f"Part 3 solution: {biggest_shout}")
