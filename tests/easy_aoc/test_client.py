"""Tests for the AocClient."""
from unittest import mock

import pytest
import requests
import yarl

from easy_aoc import client, exceptions


def test_client_fetches_puzzle_input(response_mock: mock.MagicMock) -> None:
    """Client uses the expected input URL for a puzzle."""
    # GIVEN a valid Advent of Code year
    year = 2022
    # AND a valid Advent of code day
    day = 1
    # AND an instance of the AocClient
    aoc_client = client.AocClient(
        base_url=yarl.URL("https://adventofcode.com"), session_key="foo"
    )
    # AND an expected puzzle input
    expected_puzzle_input = f"puzzle input for {year}-{day}\n"
    # AND an expected URL of the input
    expected_input_url = yarl.URL("https://adventofcode.com/2022/day/1/input")
    # AND a mocked response
    response_mock.text = expected_puzzle_input

    # WHEN the puzzle input for that year and day is requested
    with mock.patch.object(requests, "request") as request_mock:
        request_mock.return_value = response_mock
        raw_input = aoc_client.get_puzzle_input(year=year, day=day)

    # THEN the client requested the expected url
    requested_url = request_mock.call_args.kwargs.get("url")
    assert yarl.URL(requested_url) == expected_input_url
    # AND the returned raw_input matches the expected input
    assert raw_input == expected_puzzle_input


def test_client_raises_exception_for_unavailable_puzzle_input(
    response_mock: mock.MagicMock,
) -> None:
    """Non-existent puzzle inputs raise an informative exception."""
    # GIVEN a prepared 404 response
    response_mock.status_code = 404
    # AND a raise_for_status that raises a HTTPError with that response
    http_error_exc = requests.HTTPError(response=response_mock)
    response_mock.raise_for_status.side_effect = http_error_exc
    # AND an aoc client
    aoc_client = client.AocClient(
        base_url=yarl.URL("https://adventofcode.com"), session_key="foo"
    )

    # WHEN the puzzle input for that year and day is requested
    # THEN the appropriate exception is raised
    with mock.patch.object(requests, "request") as request_mock:
        request_mock.return_value = response_mock

        with pytest.raises(exceptions.PuzzleInputUnavailable) as exc_info:
            aoc_client.get_puzzle_input(year=2022, day=1)

    # AND the exception value is the expected message
    assert exc_info.value.msg == "Puzzle input not available"
    # AND the exception contains the year
    assert exc_info.value.year == 2022
    # AND the exception contains the day
    assert exc_info.value.day == 1
