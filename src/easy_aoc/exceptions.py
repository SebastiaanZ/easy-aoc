"""Exceptions for easy-aoc.

All exceptions derive from EasyAocException.
"""


class EasyAocException(Exception):
    """Base class for easy-aoc exceptions."""


class PuzzleException(EasyAocException):
    """Base class for puzzle-related exceptions."""

    def __init__(self, year: int, day: int, msg: str) -> None:
        super().__init__(msg)
        self.year = year
        self.day = day
        self.msg = msg

    def __repr__(self) -> str:
        """Get the representation of a PuzzleException."""
        cls_name = type(self).__name__
        return f"{cls_name}(year={self.year!r}, day={self.day!r}, msg={self.msg!r})"

    def __str__(self) -> str:
        """Get a user-friendly representation for a PuzzleException."""
        return f"Error with puzzle <year={self.year}, day={self.day}>: {self.msg}"


class PuzzleInputUnavailable(PuzzleException):
    """Raised when a puzzle input is not available."""

    def __init__(self, year: int, day: int) -> None:
        super().__init__(year=year, day=day, msg="Puzzle input not available")
