from song.q11 import (
    flockify,
    find_donors_and_recipients,
    run_full_simulation,
    run_fast_simulation,
    advance_fast_simulation,
    num_rounds_to_skip,
)


def test_num_rounds_to_skip():
    assert num_rounds_to_skip([50, 2, 40, 90, 60]) == 15
    assert num_rounds_to_skip([35, 17, 40, 75, 75]) == 9
    assert num_rounds_to_skip([75, 75, 40, 26, 26]) == 1
    assert num_rounds_to_skip([5, 5, 5, 5, 5]) == 0
    assert num_rounds_to_skip([5, 4]) == 1
    assert num_rounds_to_skip([8, 2]) == 3
    assert num_rounds_to_skip([90, 87, 2]) == 3


def test_find_donors_and_recipients():
    assert find_donors_and_recipients([50, 2, 40, 90, 60]) == ([0, 3], [1, 4])


def test_advance_fast_simiulation():
    assert advance_fast_simulation(0, [50, 2, 40, 90, 60]) == (15, [35, 17, 40, 75, 75])


def test_simulation_speed_equivalence():
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
    simtest2 = run_full_simulation(test2)
    simtest2_fast = run_fast_simulation(test2)
    assert simtest2 == simtest2_fast == 1579, f"Expected 1579, got {simtest2}"
