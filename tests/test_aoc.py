"""Tests for the main easy_aoc namespace."""
import easy_aoc


def test_puzzle_has_useful_repr() -> None:
    """The REPR should list the year and the day."""
    # GIVEN a puzzle
    puzzle = easy_aoc.Puzzle(2022, 1)

    # WHEN the repr of that puzzle is computed
    repr_puzzle = repr(puzzle)

    # THEN the repr contains the year and the day
    assert repr_puzzle == "Puzzle(year=2022, day=1)"
