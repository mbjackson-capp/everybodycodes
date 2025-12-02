from song.q10 import to_alphanum, to_loc, part3, DragonChessGame


def test_to_alphanum():
    assert to_alphanum((0, 0)) == "A1", f"Expected 'A1', got {to_alphanum((0, 0))}"
    assert to_alphanum((4, 6)) == "G5", f"Expected 'G5', got {to_alphanum((4, 6))}"


def test_to_loc():
    assert to_loc("A1") == (0, 0), f"Expected (0,0), got {to_loc("A1")}"
    assert to_loc("G5") == (4, 6), f"Expected (4,6), got {to_loc("G5")}"


b3a = """SSS
..#
#.#
#D."""

b3b = """SSS
..#
..#
.##
.D#"""

b3c = """..S..
.....
..#..
.....
..D.."""

b3d = """.SS.S
#...#
...#.
##..#
.####
##D.#"""
b3e = """SSS.S
.....
#.#.#
.#.#.
#.D.#"""


def test_3a():
    result_3a = part3(b3a)
    assert result_3a == 15


def test_3b():
    result_3b = part3(b3b)
    assert result_3b == 8


def test_3c():
    result_3c = part3(b3c)
    assert result_3c == 44


def test_3d():
    result_3d = part3(b3d)
    assert result_3d == 4406


def test_3e():
    result_3e = part3(b3e)
    assert result_3e == 13_033_988_838


def mock_game():
    game = DragonChessGame(b3a)
    print(game, "\n", game.legal_moves)
    # turn cycle 1
    game.do_move("S>A2")
    print(game, "\n", game.legal_moves)

    game.do_move("D>A2")
    print(game, "\n", game.legal_moves)
    assert len(game.sheeps) == 2
    # turn cycle 2
    game.do_move("S>B2")
    print(game, "\n", game.legal_moves)

    game.do_move("D>C1")
    print(game, "\n", game.legal_moves)
    assert len(game.sheeps) == 1

    # turn cycle 3
    game.do_move("S>B3")
    print(game, "\n", game.legal_moves)

    game.do_move("D>B3")
    print(game, "\n", game.legal_moves)
    assert game.winner == "dragon"

    return game


def test_game_copy():
    game_3a = DragonChessGame(test_3a)
    game_3a_2 = game_3a.copy()
    game_3a_3 = mock_game()
    game_3a_4 = game_3a_3.copy()
    assert game_3a == game_3a_2
    assert game_3a is not game_3a_2
    assert game_3a_3 == game_3a_4
    assert game_3a_3 is not game_3a_4
