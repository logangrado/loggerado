#!/usr/bin/env python3

import os
import pytest


@pytest.fixture(autouse=True)
def use_utc():
    os.environ["TZ"] = "UTC"


@pytest.fixture(autouse=True)
def _print():
    """
    Print a newline between each test
    """
    print()
