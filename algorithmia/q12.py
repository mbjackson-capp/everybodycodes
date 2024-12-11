import numpy as np
from math import inf
from input_data import q12_input1, q12_input2, q12_input3

np.set_printoptions(linewidth=10000)


### PARTS 1 AND 2 #############################################################

segment_number = {"A": 1, "B": 2, "C": 3}

# invert vertically to preserve intuition of height 0 == ground in numpy indexing


def shoot(start: tuple[int, int], shooting_power: int):
    """Get the full trajectory of a projectile launch of a given shooting
    power from its starting point, assuming it does not hit anything before
    it reaches the ground."""
    trajectory = [start]
    row, col = start
    for _ in range(shooting_power):  # go diagonal upward
        row += 1
        col += 1
        trajectory.append((row, col))
    for _ in range(shooting_power):  # go horizontal
        col += 1
        trajectory.append((row, col))
    while row > 0:  # go diagonal downward until hit ground
        row -= 1
        col += 1
        trajectory.append((row, col))
    return trajectory


def fire_at_ground(start: str, segments: dict, target: tuple[int, int]):
    """Attempt to fire at a designated target by repeatedly incrementing the
    shooting power of the cannon until target is hit or there is obviously
    no shooting power that would hit the desired target.
    Returns:
        - what got hit (tuple[int,int] or None): The index of a target hit by
        this cannon, if any
        - ranking (int or None): the ranking (shooting power * segment value)
        of a successful shot at target, if any
    TODO: change to closed-form calculation to reduce loops and speed up runtime"""
    if start not in segments.keys():
        raise ValueError("Did not choose a valid segment name!")
    start_pt = segments[start]
    shooting_power = 1
    while True:
        traj = set(shoot(start_pt, shooting_power))
        if (
            target in traj
        ):  # set lookup is faster than iterating trajectory point by point
            ranking = shooting_power * segment_number[start]
            return target, ranking
        else:  # check if the cannonball ever went over the target
            overshoots = len(
                {pt for pt in traj if pt[1] > target[1] and pt[0] > target[0]}
            )
            if overshoots:
                return None, inf
            else:
                shooting_power += 1
                continue


def starting_scene(map: np.array) -> dict:
    segments = {}
    targets = set()
    hard_targets = set()
    for i, row in enumerate(map):
        for j, _ in enumerate(row):
            val = str(map[i][j])
            if val in ["A", "B", "C"]:
                segments[val] = (i, j)
            elif val == "T":
                targets.add((i, j))
            elif val == "H":
                hard_targets.add((i, j))
    return segments, targets, hard_targets


def run(map_obj: np.array):
    """
    Note: For parts 1 and 2, problem text says 'It is also advisable to start from the
    top blocks of the target structure to prevent any unpredictable fall.' As far as I can
    tell, this is unnecessary and misleading; the correct answer does not are about the order
    in which blocks are destroyed, and there is no process or rule by which blocks "fall" if
    blocks above them are destroyed. Regardless, to play it safe, I sort by targets' height
    and ensure that higher targets are destroyed before lower ones.
    """
    segments, targets, hard_targets = starting_scene(map_obj)
    # Just include each hard target on the targets list twice lol
    targets_lst = sorted(
        list(targets) + list(hard_targets) * 2, key=lambda x: (x[0], x[1]), reverse=True
    )
    solution = 0
    for target in targets_lst:
        any_of_them_hit = False
        results_of_shots = {}
        for segment in segments.keys():
            what_got_hit, result = fire_at_ground(segment, segments, target)
            if what_got_hit == target:
                any_of_them_hit = True
                results_of_shots[segment] = result
            else:
                results_of_shots[segment] = result
        if any_of_them_hit:
            solution += min(
                results_of_shots.values()
            )  # lowest finite ranking among three shots
            any_of_them_hit = False
        else:
            raise Exception(
                f"Somehow, none of the cannons could hit target {target}. Check your input."
            )
    return solution


def generate_meteor_shower(input):
    """Turn a text list of coordinates into a list of integer tuples representing the position of
    meteors relative to cannon A.
    To keep consistency with numpy indexing from previous parts, I swap the left and right
    values, e.g. an input of "6 5", representing an input six columns ahead and five
    rows up from cannon A, becomes [(5, 6)]."""
    meteors = []
    for line in input.split("\n"):
        meteors.append(tuple(int(num) for num in line.split(" ")[::-1]))
    return meteors


### PART 3 ####################################################################


p3_segments = {"A": (0, 0), "B": (1, 0), "C": (2, 0)}


def check_for_hit_at_time(segment: str, meteor_origin: tuple[int, int], shot_time: int):
    """
    Adjust initial position of meteor to account for delay in firing cannon, then
    check all reasonable values of shooting power to see if the cannon can hit
    meteor when starting at this time.
    This approach allows us to do our intersection checks 'as though' starting time were
    0, simplifying the helper function.
    Returns:
        - altitude (int): altitude of hit if there is one, or -1 otherwise
        - ranking (int): ranking of hit if there is one, or inf otherwise
        - break_flag (bool): inform function above whether it is worth continuing
        to test for hits. True if no other hit is possible beyond this point;
        False otherwise.
    """
    x_0, y_0 = meteor_origin
    delayed_meteor_origin = (x_0 - shot_time, y_0 - shot_time)
    # TODO: figure out max shooting power to check from meteor origin and cannon
    # and just stop there
    BIG_NUMBER = 10000
    for pwr in range(1, BIG_NUMBER):
        alt, rank, break_flag = check_for_hit_at_power(
            segment, delayed_meteor_origin, pwr
        )
        if (alt != -1 and rank != inf) or break_flag:
            return alt, rank, break_flag
    # no hits
    return -1, inf, False


def get_x_at_time(t, shooting_power, cannon_height):
    """Get the x-value (height) of a flying cannonball at time t (at which its
    y-value (distance ahead of cannon) is guaranteed to be t). Used to make
    code in part3() neater."""
    if t <= shooting_power:  # Cannonball on upward path
        return cannon_height + t
    elif t <= (2 * shooting_power):  # Cannonball in flat path
        return cannon_height + shooting_power  #
    else:  # Cannonball on downward path; goes negative if trajectory has ended
        return cannon_height + (3 * shooting_power) - t


# The order of these helper functions may have to change
def check_for_hit_at_power(
    segment: str, meteor_origin: tuple[int, int], shooting_power: int
):
    """Helper function to be called each time shooting power or time delay is incremented.
    Runs calculations for one shot of the cannon and one meteor, at an assumed/normalized
    start time of t=0.
    Returns:
        - altitude (int): altitude of hit if there is one, or -1 otherwise
        - ranking (int): ranking of hit if there is one, or inf otherwise
        - break_flag (bool): inform function above whether it is worth continuing
        to test for hits. True if no other hit is possible beyond this point;
        False otherwise.
    """
    cannon_height = segment_number[segment] - 1
    x_0, y_0 = meteor_origin
    horiz_intercept = y_0 - x_0
    vert_intercept = x_0 - y_0
    # Case 1: meteor falls to the left of entire trajectory. No shot at any
    # angle will intersect with meteor's path
    if horiz_intercept < -cannon_height:
        return -1, inf, True
    start, up_end, flat_end, end = quick_shot_stats(segment, shooting_power)
    # TODO: This can go negative. This should probably never go negative.
    fall_dist_to_flatline = x_0 - up_end[0]  # == time steps for meteor to fall there

    # UPWARD PATH
    # Case 2: meteor falls exactly along upward path
    if horiz_intercept == -cannon_height:
        # Case 2a: meteor won't fall in time to get hit on upward trajectory
        if fall_dist_to_flatline > shooting_power:
            return -1, inf, False
        else:
            # find the altitude at which collision occurs
            # since cannonball advances by 1 at each time step and meteor falls by 1 at each time step,
            # it must be the case that...
            start_dist_to_meteor = x_0 - cannon_height
            # Case 2b: meteor falls in time and gets hit at discrete time
            # e.g.: cannon (0,0) meteor (4,4) -> (1,1) and (3,3) -> hit at (2,2)
            if start_dist_to_meteor % 2 == 0:
                altitude = (start_dist_to_meteor // 2) + cannon_height
                ranking = shooting_power * segment_number[segment]
                return altitude, ranking, True
            # Case 2c: projectile and meteor miss each other because time steps are discrete
            # e.g. cannon (0,0) meteor (5,5) -> (1,1) and (4,4) -> (2,2) and (3,3) -> (3,3) and (2,2)
            else:
                return -1, inf, False

    # FLAT PATH
    y_at_flatline = y_0 - fall_dist_to_flatline
    x_at_flatline = x_0 - fall_dist_to_flatline
    # Case 3: Meteor fall path intersects with flat part of cannon trajectory
    # if shooting_power <= y_at_flatline <= (2 * shooting_power):
    # we need to know not just that y_at_flatline is within the right horizontal range,
    # but also that the cannonball got to the same spot at the exact same time.

    # Luckily for us, fall_dist_to_flatline is also the exact amount of time
    # that has passed.

    # Also, fall_dist_to_flatline has to equal the y value of the cannonball at,
    # putative intersection time, since y_cannonball starts at 0 and updates by 1
    # in each time step.
    x_cannonball = get_x_at_time(fall_dist_to_flatline, shooting_power, cannon_height)
    if (x_cannonball, fall_dist_to_flatline) == (x_at_flatline, y_at_flatline):
        altitude = shooting_power + cannon_height  # weknowdis
        ranking = shooting_power * segment_number[segment]
        return altitude, ranking, True

    # DOWNWARD PATH
    # Case 4: meteor fall path intersects with downward part of cannon trajectory
    """
    Solve the equation.
    # Downward line: x = -y + end[1]
    # [remember, vertical_intercept = (x_0 - y_0)]
    # Meteor fall path: x = y + (x_0 - y_0)
    # so they intersect when -y + end[1] = y + (x_0 - y_0)
    # end[1] = 2y + vert_intercept
    # rearrange to get:
    """
    y_intersection = (end[1] - vert_intercept) / 2
    fall_dist_to_intersection = y_0 - y_intersection
    x_intersection = x_0 - fall_dist_to_intersection
    # Note that you run into discreteness issues again here!!! because of the divide by 2,
    # nominal intersection could happen at a decimal time
    # Case 4a: intersection does not occur on discrete time interval
    if y_intersection != int(y_intersection):
        return -1, inf, False
    elif (
        x_intersection >= shooting_power + cannon_height
    ):  # projectile never gets that high
        return -1, inf, False
    # Case 4b: intersection hits downward path
    elif (flat_end[1] <= y_intersection <= end[1]) and (x_intersection >= 0):
        x_cannonball = get_x_at_time(
            fall_dist_to_intersection, shooting_power, cannon_height
        )
        if (x_cannonball, fall_dist_to_intersection) == (
            x_intersection,
            y_intersection,
        ):

            ranking = shooting_power * segment_number[segment]
            return x_intersection, ranking, True

    # Case 5: meteor fall path too far right to intersect with any part of trajectory.
    # Repeat the process above with a higher shooting power.
    return -1, inf, False


def quick_shot_stats(segment: str, shooting_power: int) -> tuple[tuple[int, int]]:
    """Get all relevant information necessary to reconstruct full trajectory
    of a projectile launch of a given shooting power from its starting point,
    assuming it does not hit anything before it reaches the ground.
    We don't need to calculate time because it's always exactly equal to y, assuming
    that the shot time is 'normalized' to 0 (which it will be in function
    that calls this)"""
    if segment in p3_segments:
        start = p3_segments[segment]
        start_x, start_y = start
        upward_part_end = (start_x + shooting_power, start_y + shooting_power)
        flat_part_end = (start_x + shooting_power, start_y + (2 * shooting_power))
        end = (0, start_x + (3 * shooting_power))
    return start, upward_part_end, flat_part_end, end


def part3(shower: list[tuple[int, int]]) -> int:
    """Get the highest-altitude, lowest-ranking score for shooting down each meteor
    in input, as described in problem description.
    Note: Much as Parts 1 and 2"""
    solution = 0
    for meteor in shower:
        results = {}
        for segment in ["A", "B", "C"]:
            t = 0
            while True:
                # TODO: figure out max t you need to test given this meteor and cannon
                # in lieu of that, use x value (height) of meteor for now
                max_t_to_test = meteor[0]
                # check ALL possible shooting powers from 1 to max for this segment at this time
                # underlying procedure should break once it finds a hit or return (-1, inf) as
                # indication that it failed to find
                # TODO: figure out more intelligently whether incrementing of shooting_power
                # can be stopped early
                alt, rank, break_flag = check_for_hit_at_time(segment, meteor, t)
                if break_flag == True:  # No hits possible at times later than t
                    results[segment] = {"altitude": alt, "ranking": rank}
                    break
                if alt != -1 and rank != inf:
                    results[segment] = {"altitude": alt, "ranking": rank}
                    break
                # No hit found at time t
                if t >= max_t_to_test:
                    results[segment] = {"altitude": -1, "ranking": inf}
                    break
                else:
                    t += 1
        # Built-in tests for example data since this is complicated!
        if meteor == (5, 6):
            assert (
                results["A"] == {"altitude": 2, "ranking": 2}
                and results["B"] == {"altitude": -1, "ranking": inf}
                and results["C"] == {"altitude": 2, "ranking": 3}
            ), "results for (5,6) should be: 'A': 2, 2; 'B': -1, inf; 'C': 2, 3"
        elif meteor == (7, 6):
            assert (
                results["A"] == {"altitude": -1, "ranking": inf}
                and results["B"] == {"altitude": 4, "ranking": 6}
                and results["C"] == {"altitude": 4, "ranking": 6}
            ), "results for (7,6) should be: 'A': -1, inf; 'B': 4, 6; 'C': 4, 6"
        elif meteor == (5, 10):
            assert (
                results["A"] == {"altitude": -1, "ranking": inf}
                and results["B"] == {"altitude": -1, "ranking": inf}
                and results["C"] == {"altitude": 0, "ranking": 3}
            ), "results for (5, 10) should be: 'A': -1, inf; 'B': -1, inf; 'C': 0, 3"

        # get the lowest-ranking option among high-altitude hits
        best_ranking = min(
            [
                results[segment]["ranking"]
                for segment in results
                if results[segment]["altitude"]
                == max([results[segment]["altitude"] for segment in results])
            ]
        )
        solution += best_ranking
    # after all meteors computed:
    return solution


if __name__ == "__main__":
    map1 = np.array([[char for char in row] for row in q12_input1.split("\n")][::-1])
    print(f"Now running Part 1 and Part 2. This could take several seconds...")
    part1_solution = run(map1)
    print(f"Part 1 solution: {part1_solution}")

    map2 = np.array([[char for char in row] for row in q12_input2.split("\n")][::-1])
    part2_solution = run(map2)
    print(f"Part 2 solution: {part2_solution}")

    # Three meteors take super long for unclear reasons, but this solution works
    # if you wait for them!
    # 3600, 7198
    # 1989, 3976
    # 3601, 7200
    # TODO: find efficiency issue and fix it
    print(f"Now running Part 3. This could take several minutes...")
    meteors = generate_meteor_shower(q12_input3)
    part3_solution = part3(meteors)
    print(f"Part 3 solution: {part3_solution}")
