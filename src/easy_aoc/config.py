"""Main configuration class for easy-aoc."""
from __future__ import annotations

import attrs


@attrs.define(frozen=True)  # pylint: disable-next=too-few-public-methods
class Configuration:
    """Class with configuration for the easy-aoc tools."""

    session_key: str = attrs.field(repr=lambda key: "[hidden]")
