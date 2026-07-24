"""
Ensures that the build has been run.
"""

import logging
from pathlib import Path

from manage import do_build


def test_build(caplog):
    caplog.set_level(logging.INFO)  # silence connectionpool.py DEBUG messages

    with (Path(__file__).resolve().parent.parent / "build" / "extensions.json").open() as f:
        actual = f.read()

    assert actual == do_build()
