"""Repository for getting puzzle inputs."""
import pathlib
import shutil

from .. import aoc, client


class PuzzleInputRepository:
    """A repository for getting puzzle inputs."""

    def __init__(self, cache_dir: pathlib.Path, aoc_client: client.IAocClient) -> None:
        """Initialize an Input Repository.

        :param cache_dir: The cache directory
        """
        self.input_cache_dir = cache_dir / "cached_inputs"
        self.aoc_client = aoc_client

    def get(self, year: int, day: int) -> aoc.PuzzleInput:
        """Get an Advent of Code puzzle input.

        Puzzle inputs are fetched from the Advent of Code website only
        if they do not exist in the local cache to prevent querying the
        Advent of Code website unnecessarily.

        :param year: The year of the puzzle
        :param day: The day of the puzzle
        :return: An instance of :cls:`PuzzleInput`
        """
        if (cached_input := self._get_from_cache(year, day)) is None:
            return self._fetch_and_cache(year=year, day=day)

        return cached_input

    def clear_cache(self) -> None:
        """Clear the puzzle input cache."""
        shutil.rmtree(self.input_cache_dir)

    def _set(self, year: int, day: int, raw_input: str) -> None:
        """Set the puzzle input in the puzzle cache.

        Note: This method should not be called manually.

        :param year: The year of the puzzle
        :param day: The day of the puzzle
        :param raw_input: The raw puzzle input as a string
        """
        cache_path = self._get_year_cache_path(year) / f"{day}.txt"
        cache_path.write_text(raw_input, encoding="utf-8")

    def _get_from_cache(self, year: int, day: int) -> aoc.PuzzleInput | None:
        """Get a puzzle input for a puzzle.

        :param year: The year of puzzle
        :param day: The day of the puzzle
        :return: The puzzle input, if it were found in the cache; None
          otherwise
        """
        cached_input_path = self.input_cache_dir / str(year) / f"{day}.txt"
        if not cached_input_path.exists():
            return None
        cached_input = cached_input_path.read_text(encoding="utf-8")
        return aoc.PuzzleInput(year=year, day=day, input=cached_input)

    def _fetch_and_cache(self, year: int, day: int) -> aoc.PuzzleInput:
        """Fetch the puzzle input from the website and cache it.

        :param year: The year of the puzzle
        :param day: The day of the puzzle
        :return: The puzzle input as a string
        """
        raw_input = self.aoc_client.get_puzzle_input(year=year, day=day)
        self._set(year=year, day=day, raw_input=raw_input)
        return aoc.PuzzleInput(year=year, day=day, input=raw_input)

    def _get_year_cache_path(self, year: int) -> pathlib.Path:
        """Get the cache directory path for a specific year.

        If no such directory exists, it is created.

        :return: A pathlib.Path to the cache directory for a year
        """
        year_path = self.input_cache_dir / str(year)
        year_path.mkdir(parents=True, exist_ok=True)
        return year_path
