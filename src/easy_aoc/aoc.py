"""The main Advent of Code module."""
import attrs
from attrs import validators


@attrs.define  # pylint: disable-next=too-few-public-methods
class Puzzle:
    """An Advent of Code puzzle."""

    year: int = attrs.field(validator=validators.ge(2015))
    day: int = attrs.field(validator=[validators.ge(1), validators.le(25)])


@attrs.define(frozen=True)  # pylint: disable-next=too-few-public-methods
class PuzzleInput:
    """An input for a specific puzzle."""

    year: int
    day: int
    input: str
