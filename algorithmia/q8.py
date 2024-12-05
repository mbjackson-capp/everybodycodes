def part1(blocks: int):
    blocks_left = blocks - 1
    blocks_in_pyramid = 1
    layer = 1
    while blocks_left > 0:
        layer += 1
        width = (2 * layer) - 1
        blocks_left -= width
        blocks_in_pyramid += width
    # you needed {-blocks_left} blocks you didn't have!
    return -blocks_left * width


def part2(blocks: int, num_priests=375, num_acolytes=1111):
    blocks_left = blocks - 1
    blocks_in_pyramid = 1
    layer = 1
    thickness = 1
    while blocks_left > 0:
        layer += 1
        width = (2 * layer) - 1
        thickness = (thickness * num_priests) % num_acolytes
        new_blocks_needed = width * thickness
        blocks_left -= new_blocks_needed
        blocks_in_pyramid += new_blocks_needed
    return -blocks_left * width


PART1_SUPPLY = 4098012
part1_solution = part1(PART1_SUPPLY)
print(f"Part 1 solution: {part1_solution}")

PART2_SUPPLY = 20240000
PART2_PRIESTS = 375
PART2_ACOLYTES = 1111
part2_solution = part2(
    PART2_SUPPLY, num_priests=PART2_PRIESTS, num_acolytes=PART2_ACOLYTES
)
print(f"Part 2 solution: {part2_solution}")

# TODO: Part 3

PART3_SUPPLY = 202400000
PART3_PRIESTS = 931087
PART3_ACOLYTES = 10
