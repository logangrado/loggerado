#!/usr/bin/env python3

import pytest


@pytest.fixture(autouse=True)
def _print():
    """
    Print a newline between each test
    """
    print()
