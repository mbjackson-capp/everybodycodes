import numpy as np
from input_data import q3_input1, q3_input2, q3_input3


def neighbors(
    gridmap: np.array,
    index: tuple[int, int],
    include_diags=False,
    include_offgrid=False,
):
    x, y = index
    max_x, max_y = gridmap.shape
    candidates = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    if include_diags:
        diags = [(x - 1, y - 1), (x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1)]
        candidates += diags
    neighbor_vals = set()
    for candidate in candidates:
        this_x, this_y = candidate
        if (0 <= this_x < max_x) and (0 <= this_y < max_y):
            neighbor_vals.add(gridmap[this_x][this_y])
        elif include_offgrid:
            neighbor_vals.add(0)
    return neighbor_vals


def all_neighbors_at_height(
    gridmap: np.array,
    index: tuple[int, int],
    hgt: int,
    diag: bool = False,
    offgrid: bool = False,
) -> bool:
    neighbor_vals = neighbors(
        gridmap, index, include_diags=diag, include_offgrid=offgrid
    )
    return (len(neighbor_vals) == 1) and (hgt in neighbor_vals)


def survey(note, diag=False, offgrid=False):
    note = note.replace(".", "0")
    note = note.replace("#", "1")
    grid_map = np.array([[int(char) for char in row] for row in note.split("\n")])
    max_x, max_y = grid_map.shape
    depth = 0
    while True:
        depth += 1
        to_update = []
        for i in range(max_x):
            for j in range(max_y):
                if grid_map[i][j] == depth and all_neighbors_at_height(
                    grid_map, (i, j), depth, diag=diag, offgrid=offgrid
                ):
                    to_update.append((i, j))
        if len(to_update) == 0:  # maximum possible depth reached
            break
        for spot in to_update:
            x, y = spot
            grid_map[x][y] = depth + 1
    return sum(grid_map.flatten())


if __name__ == "__main__":
    p1 = survey(q3_input1)
    print(f"Part 1 solution: {p1}")
    p2 = survey(q3_input2)
    print(f"Part 2 solution: {p2}")
    p3 = survey(q3_input3, diag=True, offgrid=True)
    print(f"Part 3 solution: {p3}")
