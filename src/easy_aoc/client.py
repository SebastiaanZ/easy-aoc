"""A client to communicate with the Advent of Code website."""
import http
from typing import Protocol

import attrs
import requests
import yarl

from easy_aoc import exceptions


# pylint: disable-next=too-few-public-methods
class IAocClient(Protocol):
    """Protocol for an AocClient."""

    def get_puzzle_input(self, year: int, day: int) -> str:
        """Get a puzzle input."""


@attrs.define  # pylint: disable-next=too-few-public-methods
class AocClient:
    """A client class to query the Advent of Code website."""

    base_url: yarl.URL = attrs.field(converter=yarl.URL)
    session_key: str = attrs.field(repr=lambda key: "[hidden]")

    def get_puzzle_input(self, year: int, day: int) -> str:
        """Get a puzzle input from the Advent of Code website.

        :param year: The year of the puzzle
        :param day: The day of the puzzle
        :return: The raw string puzzle input
        """
        input_url = self._get_puzzle_url(year=year, day=day) / "input"
        response = requests.request(
            method="GET", url=str(input_url), timeout=(30.0, 30.0)
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            if exc.response.status_code == http.HTTPStatus.NOT_FOUND:
                raise exceptions.PuzzleInputUnavailable(year=year, day=day) from exc
            raise
        else:
            return response.text

    def _get_puzzle_url(self, year: int, day: int) -> yarl.URL:
        """Get the url for a specific puzzle.

        :param year: The year of the puzzle
        :param day: The day of hte puzzle
        :return: The URL for the puzzle
        """
        return self.base_url / str(year) / "day" / str(day)
