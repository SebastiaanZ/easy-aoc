"""Tests for the input repository."""
import itertools
import pathlib
from unittest import mock

from easy_aoc import aoc, repository


def test_input_repository_gets_cached_input(
    tmp_path: pathlib.Path, aoc_client_mock: mock.MagicMock
) -> None:
    """The repository gets inputs from a cache."""
    # GIVEN a temporary input cache directory for a year
    cached_inputs_year_path = tmp_path / "cached_inputs" / "2022"
    cached_inputs_year_path.mkdir(parents=True)
    # AND a cached input for a specific day
    cached_input_path = cached_inputs_year_path / "1.txt"
    cached_input_path.write_text("cached input\n", encoding="utf-8")
    # AND an input repository
    input_repository = repository.PuzzleInputRepository(
        cache_dir=tmp_path, aoc_client=aoc_client_mock
    )

    # WHEN the repository gets the input
    returned_puzzle_input = input_repository.get(2022, 1)

    # THEN the returned puzzle input is equal to the cached puzzle input
    assert returned_puzzle_input == aoc.PuzzleInput(
        year=2022, day=1, input="cached input\n"
    )


def test_input_repository_gets_non_cached_input_from_website(
    tmp_path: pathlib.Path, aoc_client_mock: mock.MagicMock
) -> None:
    """Get non-cached inputs from the website and cache them."""
    # GIVEN a puzzle input
    puzzle_input_raw = "Some input\n"
    # AND an `AocClient.get_input` that returns that input
    aoc_client_mock.get_puzzle_input.return_value = puzzle_input_raw
    # AND a puzzle input repository that uses the mocked client
    input_repository = repository.PuzzleInputRepository(
        cache_dir=tmp_path, aoc_client=aoc_client_mock
    )

    # WHEN the input is retrieved from the repository
    puzzle_input = input_repository.get(2022, 1)

    # THEN the repository used the client to fetch the input
    aoc_client_mock.get_puzzle_input.assert_called_once_with(year=2022, day=1)
    # AND the puzzle input returned is as expected
    assert puzzle_input == aoc.PuzzleInput(year=2022, day=1, input=puzzle_input_raw)
    # AND the puzzle input is added to the cache
    cache_path = tmp_path / "cached_inputs" / "2022" / "1.txt"
    assert cache_path.exists() and cache_path.is_file()
    assert cache_path.read_text(encoding="utf-8") == puzzle_input_raw


def test_clear_clears_all_cache_files(
    tmp_path: pathlib.Path, aoc_client_mock: mock.MagicMock
) -> None:
    """The repository may clear the cache."""
    # GIVEN a filled input cache
    input_cache_path = tmp_path / "cached_inputs"
    for year, day in itertools.product(range(2015, 2023), range(1, 26)):
        year_path = input_cache_path / str(year)
        year_path.mkdir(parents=True, exist_ok=True)
        day_path = year_path / f"{day}.txt"
        day_path.write_text(f"Input for day {day}\n", encoding="utf-8")
    # AND a puzzle input repository using that cache
    input_repo = repository.PuzzleInputRepository(
        cache_dir=tmp_path, aoc_client=aoc_client_mock
    )

    # WHEN the clear_cache is called on the repo
    input_repo.clear_cache()

    # THEN the cache is cleared
    assert not input_cache_path.exists()
