"""Fixtures available to all tests."""
from typing import cast
from unittest import mock

import pytest
import requests

from easy_aoc import client


@pytest.fixture
def aoc_client_mock() -> mock.MagicMock:
    """Return a mocked AocClient."""
    return cast(
        mock.MagicMock,
        mock.create_autospec(client.IAocClient, spec_set=True, instance=True),
    )


@pytest.fixture
def response_mock() -> mock.MagicMock:
    """Return a mocked response.

    Note: `spec_set` isn't set as most attributes are not visible to the
    mock.
    """
    return cast(mock.MagicMock, mock.create_autospec(requests.Response, instance=True))
